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


@blueprint.route("/zcta", methods=["POST"])
def zcta():
    json_data = request.get_json()
    if json_data is None:
        raise InvalidAPIUsage("No JSON body found.")

    schema = {
        "type": "object",
        "properties": {
            "x1": {"type": "number"},
            "y1": {"type": "number"},
            "x2": {"type": "number"},
            "y2": {"type": "number"},
            "name": {"type": "string"},
        },
        "required": ["x1", "y1", "x2", "y2"],
    }

    jsonschema.validate(instance=json_data, schema=schema)

    mbr = {
        "x1": json_data["x1"],
        "y1": json_data["y1"],
        "x2": json_data["x2"],
        "y2": json_data["y2"],
    }

    return app.gis.query.get_zctas_intersecting_mbr(
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
    df.drop_duplicates(inplace=True)
    return df


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

    df = get_beacodes_by_zipcode(json_data["zipcode"])
    return {"results": df.to_dict("records")}


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


@blueprint.route("/useeio", methods=["POST"])
def useeio():
    def buildQueryParams():
        return {
            "base_url": current_app.config["USEEIO_BASE_URL"],
            "api_key": current_app.config["USEEIO_API_KEY"],
        }

    return app.useeio.query.get_all_sectors(buildQueryParams())
