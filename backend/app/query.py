import pandas
import jsonschema
from flask import Blueprint, request, current_app

import app.gis.query
import app.cbp.query
import app.bea.query
import app.useeio.query
from app.db import get_spatial_db
from app.db import get_db


class InvalidAPIUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv["message"] = self.message
        return rv


blueprint = Blueprint("query", __name__, url_prefix="/query")


@blueprint.route("/zcta/mbr", methods=["POST"])
def zcta():
    mbr = request.get_json()
    if mbr is None:
        raise InvalidAPIUsage("No JSON body found.")

    schema = {
        "type": "object",
        "properties": {
            "x1": {"type": "number"},
            "y1": {"type": "number"},
            "x2": {"type": "number"},
            "y2": {"type": "number"},
        },
        "required": ["x1", "y1", "x2", "y2"],
    }

    jsonschema.validate(instance=mbr, schema=schema)

    return app.gis.query.get_zctas_intersecting_mbr(
        spatial_db=get_spatial_db(), mbr=mbr
    )


@blueprint.route("/county/mbr", methods=["POST"])
def county_mbr():
    mbr = request.get_json()
    if mbr is None:
        raise InvalidAPIUsage("No JSON body found.")

    schema = {
        "type": "object",
        "properties": {
            "x1": {"type": "number"},
            "y1": {"type": "number"},
            "x2": {"type": "number"},
            "y2": {"type": "number"},
        },
        "required": ["x1", "y1", "x2", "y2"],
    }

    jsonschema.validate(instance=mbr, schema=schema)

    return app.gis.query.get_counties_intersecting_mbr(
        spatial_db=get_spatial_db(), mbr=mbr
    )


def get_beacodes_by_zipcode(zipcode) -> pandas.DataFrame:
    codes = app.cbp.query.get_naics_by_zipcode(
        base_url=current_app.config["CENSUS_BASE_URL"],
        api_key=current_app.config["CENSUS_API_KEY"],
        zipcode=zipcode,
    )

    df = pandas.DataFrame(
        [
            app.bea.query.get_beacode_from_naics2017(db=get_db(), naics2017_code=code)
            for code in codes
        ]
    )

    df["COUNT"] = df.groupby(["BEA_CODE"])["BEA_CODE"].transform("size")
    df.drop_duplicates("BEA_CODE", inplace=True)
    return df

def get_industries_by_county(*, statefp,countyfp) -> pandas.DataFrame:
    industries = app.cbp.query.get_industries_by_county(
        base_url=current_app.config["CENSUS_BASE_URL"],
        api_key=current_app.config["CENSUS_API_KEY"],
        statefp=statefp,
        countyfp=countyfp
    )

    industries["BEA_CODE"] = industries.apply(
        lambda row: app.bea.query.get_beacode_from_naics2017(
            db=get_db(),
            naics2017_code=row["NAICS2017_CODE"]), axis=1)

    industries["REVENUE"] = industries.apply(
        lambda row: row["EMP"] * 1e5, axis=1)

    sectors = app.useeio.query.get_all_sectors(
        base_url=current_app.config["USEEIO_BASE_URL"],
        api_key=current_app.config["USEEIO_API_KEY"],
    )

    industries = industries.merge(right=sectors, left_on="BEA_CODE", right_on="code")

    industries['TOTAL_PAYROLL'] = industries.groupby(['id'])['PAYANN'].transform('sum')
    industries['TOTAL_REVENUE'] = industries.groupby(['id'])['REVENUE'].transform('sum')
    industries['TOTAL_EMPLOYEES'] = industries.groupby(['id'])['EMP'].transform('sum')
    industries['TOTAL_ESTABLISHMENTS'] = industries.groupby(['id'])['id'].transform('count')
    industries = industries.drop(columns=["NAICS2017_CODE","PAYANN","EMP","REVENUE", "code","location","index","description"])
    if industries is None:
        raise AssertionError("Unexpectedly removed all columns!")
    industries = industries.drop_duplicates()
    if industries is None:
        raise AssertionError("Unexpectedly dropped everything as duplicates.")

    D_transposed = app.useeio.query.get_matrices()["D"].transpose()
    industries = industries.merge(D_transposed, left_on="id", right_index=True)

    return industries


@blueprint.route("/useeio/matrices", methods=["POST"])
def matrices():
    json_data = request.get_json()
    if json_data is None:
        raise InvalidAPIUsage("No JSON body found.")
    schema = {
        "type": "object",
        "properties": {},
        "required": [],
    }

    jsonschema.validate(instance=json_data, schema=schema)

    dfs = app.useeio.query.get_matrices()
    return {}


@blueprint.route("/zipcode", methods=["POST"])
def zipcode():
    json_data = request.get_json()
    if json_data is None:
        raise InvalidAPIUsage("No JSON body found.")

    schema = {
        "type": "object",
        "properties": {
            "zipcode": {"type": "string"},
            "name": {"type": "string"},
        },
        "required": ["zipcode"],
    }

    jsonschema.validate(instance=json_data, schema=schema)

    df_1 = get_beacodes_by_zipcode(json_data["zipcode"])

    df_2 = app.useeio.query.get_all_sectors(
        base_url=current_app.config["USEEIO_BASE_URL"],
        api_key=current_app.config["USEEIO_API_KEY"],
    )

    df = pandas.merge(left=df_1, right=df_2, left_on="BEA_CODE", right_on="code")
    matrices = app.useeio.query.get_matrices()
    filtered = matrices["D"].filter(items=df["id"], axis="columns")
    return {"results": filtered.to_dict("records")}

@blueprint.route("/county", methods=["POST"])
def county():
    json_data = request.get_json()
    if json_data is None:
        raise InvalidAPIUsage("No JSON body found.")

    schema = {
        "type": "object",
        "properties": {
            "statefp": {"type": "string"},
            "countyfp": {"type": "string"},
        },
        "required": ["statefp","countyfp"],
    }

    jsonschema.validate(instance=json_data, schema=schema)

    industries = get_industries_by_county(statefp=json_data["statefp"],countyfp=json_data["countyfp"])

    matrices = app.useeio.query.get_matrices()
    filtered = matrices["D"].filter(items=industries["id"], axis="columns")
    return {"results": industries.to_dict("records")}


@blueprint.route("/naics", methods=["POST"])
def naics():
    json_data = request.get_json()
    if json_data is None:
        raise InvalidAPIUsage("No JSON body found.")

    schema = {
        "type": "object",
        "properties": {
            "zipcode": {"type": "string"},
            "name": {"type": "string"},
        },
        "required": ["zipcode"],
    }

    jsonschema.validate(instance=json_data, schema=schema)

    results = app.cbp.query.get_naics_by_zipcode(
        base_url=current_app.config["CENSUS_BASE_URL"],
        api_key=current_app.config["CENSUS_API_KEY"],
        zipcode=json_data["zipcode"],
    )
    return {"results": results}


@blueprint.route("/bea/naics2007", methods=["POST"])
def bea_naics2007():
    json_data = request.get_json()
    if json_data is None:
        raise InvalidAPIUsage("No JSON body found.")

    schema = {
        "type": "object",
        "properties": {
            "naics2007_code": {"type": "string"},
            "name": {"type": "string"},
        },
        "required": ["naics2007_code"],
    }

    jsonschema.validate(instance=json_data, schema=schema)

    results = app.bea.query.get_beacode_from_naics2007(
        db=get_db(), naics2007_code=json_data["naics2007_code"]
    )

    return {"results": results}


@blueprint.route("/bea/naics2017", methods=["POST"])
def bea_naics2017():
    json_data = request.get_json()
    if json_data is None:
        raise InvalidAPIUsage("No JSON body found.")

    schema = {
        "type": "object",
        "properties": {
            "naics2007_code": {"type": "string"},
            "name": {"type": "string"},
        },
        "required": ["naics2007_code"],
    }

    jsonschema.validate(instance=json_data, schema=schema)

    results = app.bea.query.get_beacode_from_naics2017(
        db=get_db(), naics2017_code=json_data["naics2017_code"]
    )

    return {"results": results}


@blueprint.route("/useeio/sectors", methods=["POST"])
def useeio():
    df = app.useeio.query.get_all_sectors(
        base_url=current_app.config["USEEIO_BASE_URL"],
        api_key=current_app.config["USEEIO_API_KEY"],
    )
    return {"results": df.to_dict("records")}
