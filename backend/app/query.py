import click
import pandas
import jsonschema
import json
from flask import Blueprint, request, current_app
from itertools import combinations_with_replacement
import statistics


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


def get_sector_crosswalk():
    matrices = app.useeio.query.get_matrices()
    return matrices["SectorCrosswalk"]


def get_direct_impacts_matrix():
    matrices = app.useeio.query.get_matrices()
    D = matrices["D"]
    D.columns = D.columns.str.rstrip("/US")
    return D


def get_all_counties():
    return app.gis.query.get_all_counties(spatial_db=get_spatial_db())


def industries_by_county(*, statefp, countyfp):
    return app.cbp.query.get_industries_by_county(
        base_url=current_app.config["CENSUS_BASE_URL"],
        api_key=current_app.config["CENSUS_API_KEY"],
        statefp=statefp,
        countyfp=countyfp,
    )


def direct_industry_impacts_by_county(state, county):
    industries = industries_by_county(statefp=int(state), countyfp=int(county))
    crosswalk = get_sector_crosswalk()
    industries = industries.merge(crosswalk, left_on="NAICS2017", right_on="NAICS")
    impacts = get_direct_impacts_matrix().transpose()
    industries = industries.merge(impacts, left_on="BEA_Detail", right_index=True)
    grouped = industries.groupby("NAICS2017", as_index=False)

    aggregate_default = {x: "first" for x in industries.columns}
    aggregate_as_set = {x: lambda ser: set(ser) for x in impacts.columns}
    aggregation_operations = aggregate_default | aggregate_as_set
    aggregation_operations["BEA_Detail"] = lambda ser:list(set(ser)) #type: ignore
    aggregated = grouped.agg(aggregation_operations)

    def mean_of_combinations(row, col):
        return statistics.mean(
            [
                sum(list(x))
                for x in combinations_with_replacement(row[col], int(row["ESTAB"]))
            ]
        )

    for impact in impacts.columns:
        aggregated[impact] = aggregated.apply(
            lambda row: mean_of_combinations(row, impact), axis=1
        )

    return aggregated


@blueprint.cli.command("industries_by_county")
@click.argument("state")
@click.argument("county")
def print_industries_by_county(state, county):
    industries = industries_by_county(statefp=int(state), countyfp=int(county))
    print(industries.to_html())


@blueprint.cli.command("direct_impacts_matrix")
def print_direct_impacts_matrix():
    print(get_direct_impacts_matrix().transpose())


@blueprint.cli.command("direct_industry_impacts_by_county")
@click.argument("state")
@click.argument("county")
def print_direct_industry_impacts_by_county(state, county):
    print(direct_industry_impacts_by_county(state, county).to_html())


@blueprint.cli.command("sector_crosswalk")
# @click.argument('name')
def print_sector_crosswalk():
    print(json.dumps(get_sector_crosswalk().to_dict("records")))


@blueprint.cli.command("all_counties")
def print_all_counties():
    print(json.dumps(get_all_counties().to_dict("records")))


@blueprint.route("/county/all", methods=["GET"])
def serve_get_all_counties():
    current_app.logger.info("Request for all counties.")
    return {"results": get_all_counties().to_dict("records")}


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

    result = app.gis.query.get_counties_intersecting_mbr(
        spatial_db=get_spatial_db(), mbr=mbr
    )

    return result


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


@blueprint.route("/county/impacts", methods=["POST"])
def serve_industry_impacts_by_county():
    params = request.get_json()
    if params is None:
        raise InvalidAPIUsage("No JSON body found.")

    schema = {
        "type": "object",
        "properties": {
            "statefp": {"type": "number"},
            "countyfp": {"type": "number"},
        },
        "required": ["statefp", "countyfp"],
    }

    jsonschema.validate(instance=params, schema=schema)

    current_app.logger.info(
        f"Request impact data for {params['statefp']} {params['countyfp']}"
    )

    return {
        "direct_impacts": direct_industry_impacts_by_county(
            params["statefp"], params["countyfp"]
        ).to_dict("records"),
    }


def compute_total_emissions(industries):
    columns = app.useeio.query.get_matrices()["D"].index.to_list()
    data = industries[columns].sum()
    return pandas.DataFrame(data=[data], columns=columns)


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
