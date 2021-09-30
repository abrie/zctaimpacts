import click
import random
import jsonschema
import json
from flask import Blueprint, request, current_app
import statistics


import app.gis.query
import app.cbp.query
import app.useeio.query
from app.db import get_spatial_db


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


def get_indicators_matrix():
    matrices = app.useeio.query.get_matrices()
    return matrices["indicators"]


def get_direct_impacts_matrix():
    matrices = app.useeio.query.get_matrices()
    D = matrices["D"]
    D.columns = D.columns.str.rstrip("/US")
    return D


def get_all_counties():
    return app.gis.query.get_all_counties(spatial_db=get_spatial_db())


def get_all_zipcodes():
    return app.gis.query.get_all_zipcodes(spatial_db=get_spatial_db())


def industries_by_county(*, statefp, countyfp):
    return app.cbp.query.get_industries_by_county(
        base_url=current_app.config["CENSUS_BASE_URL"],
        api_key=current_app.config["CENSUS_API_KEY"],
        statefp=statefp,
        countyfp=countyfp,
    )


def industries_by_zipcode(*, zipcode):
    return app.cbp.query.get_industries_by_zipcode(
        base_url=current_app.config["CENSUS_BASE_URL"],
        api_key=current_app.config["CENSUS_API_KEY"],
        zipcode=zipcode,
    )


def direct_industry_impacts_by_zipcode(*, zipcode, sample_size):
    current_app.logger.info(
        f"Collecting direct industry impact data for zipcode/{zipcode}"
    )
    industries = industries_by_zipcode(zipcode=zipcode)
    crosswalk = get_sector_crosswalk()
    industries = industries.merge(crosswalk, left_on="NAICS2017", right_on="NAICS")
    impacts = get_direct_impacts_matrix().transpose()
    industries = industries.merge(impacts, left_on="BEA_Detail", right_index=True)
    grouped = industries.groupby("NAICS2017", as_index=False)

    aggregate_default = {x: "first" for x in industries.columns}
    aggregate_as_set = {x: lambda ser: set(ser) for x in impacts.columns}
    aggregation_operations = aggregate_default | aggregate_as_set
    aggregation_operations["BEA_Detail"] = lambda ser: list(set(ser))  # type: ignore
    aggregated = grouped.agg(aggregation_operations)

    def mean_of_combinations(row, col):
        population = list(row[col])
        if len(population) == 1:
            return population[0]

        k = row["ESTAB"]
        samples = [sum(random.choices(population, k=k)) for _ in range(0, sample_size)]
        return statistics.mean(samples)

    for impact in impacts.columns:
        aggregated[impact] = aggregated.apply(
            lambda row: mean_of_combinations(row, impact), axis=1
        )

    current_app.logger.info(f"Done zipcode/{zipcode}")

    return aggregated


def direct_industry_impacts_by_county(state, county, sample_size):
    current_app.logger.info(
        f"Collecting direct industry impact data for state/{state}/county/{county}"
    )
    industries = industries_by_county(statefp=int(state), countyfp=int(county))
    crosswalk = get_sector_crosswalk()
    industries = industries.merge(crosswalk, left_on="NAICS2017", right_on="NAICS")
    impacts = get_direct_impacts_matrix().transpose()
    industries = industries.merge(impacts, left_on="BEA_Detail", right_index=True)
    grouped = industries.groupby("NAICS2017", as_index=False)

    aggregate_default = {x: "first" for x in industries.columns}
    aggregate_as_set = {x: lambda ser: set(ser) for x in impacts.columns}
    aggregation_operations = aggregate_default | aggregate_as_set
    aggregation_operations["BEA_Detail"] = lambda ser: list(set(ser))  # type: ignore
    aggregated = grouped.agg(aggregation_operations)

    def mean_of_combinations(row, col):
        population = list(row[col])
        if len(population) == 1:
            return population[0]

        k = row["ESTAB"]
        samples = [sum(random.choices(population, k=k)) for _ in range(0, sample_size)]
        return statistics.mean(samples)

    for impact in impacts.columns:
        aggregated[impact] = aggregated.apply(
            lambda row: mean_of_combinations(row, impact), axis=1
        )

    current_app.logger.info(f"Done {state} {county}")

    return aggregated


@blueprint.cli.command("indicators")
def print_indicators():
    indicators = get_indicators_matrix()
    print(indicators.to_html())


@blueprint.route("/indicators", methods=["GET"])
def serve_indicators():
    indicators = get_indicators_matrix()
    return {"indicators": indicators.to_dict("records")}


@blueprint.cli.command("industries_by_county")
@click.argument("state")
@click.argument("county")
def print_industries_by_county(state, county):
    industries = industries_by_county(statefp=int(state), countyfp=int(county))
    print(industries.to_html())


@blueprint.cli.command("industries_by_zipcode")
@click.argument("zipcode")
def print_industries_by_zipcode(zipcode):
    industries = industries_by_zipcode(zipcode=zipcode)
    print(industries.to_html())


@blueprint.cli.command("direct_impacts_matrix")
def print_direct_impacts_matrix():
    print(get_direct_impacts_matrix().transpose())


@blueprint.cli.command("direct_industry_impacts_by_county")
@click.argument("state")
@click.argument("county")
@click.option("--sample_size", default=100)
def print_direct_industry_impacts_by_county(state, county, sample_size):
    print(direct_industry_impacts_by_county(state, county, sample_size).to_html())


@blueprint.cli.command("direct_industry_impacts_by_zipcode")
@click.argument("zipcode")
@click.option("--sample_size", default=100)
def print_direct_industry_impacts_by_zipcode(zipcode, sample_size):
    print(
        direct_industry_impacts_by_zipcode(
            zipcode=zipcode, sample_size=sample_size
        ).to_html()
    )


@blueprint.cli.command("sector_crosswalk")
# @click.argument('name')
def print_sector_crosswalk():
    print(json.dumps(get_sector_crosswalk().to_dict("records")))


@blueprint.cli.command("all_counties")
def print_all_counties():
    print(json.dumps(get_all_counties().to_dict("records")))


@blueprint.cli.command("all_zipcodes")
def print_all_zipcodes():
    print(json.dumps(get_all_zipcodes().to_dict("records")))


@blueprint.route("/zipcode/all", methods=["GET"])
def serve_get_all_zipcodes():
    current_app.logger.info("Request for all zipcodes.")
    return {"results": get_all_zipcodes().to_dict("records")}


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


@blueprint.route("/zipcode/impacts", methods=["POST"])
def serve_direct_industry_impacts_by_zipcode():
    params = request.get_json()
    if params is None:
        raise InvalidAPIUsage("No JSON body found.")

    schema = {
        "type": "object",
        "properties": {
            "zipcode": {"type": "string"},
            "sampleSize": {"type": "number"},
        },
        "required": ["zipcode", "sampleSize"],
    }

    jsonschema.validate(instance=params, schema=schema)

    current_app.logger.info(
        f"Processing request for impact data for zipcode {params['zipcode']}"
    )

    industries = direct_industry_impacts_by_zipcode(
        zipcode=params["zipcode"], sample_size=params["sampleSize"]
    )

    current_app.logger.info(f"Computed impact data for zipcode {params['zipcode']}")

    return {
        "industries": industries.to_dict("records"),
    }


@blueprint.route("/county/impacts", methods=["POST"])
def serve_direct_industry_impacts_by_county():
    params = request.get_json()
    if params is None:
        raise InvalidAPIUsage("No JSON body found.")

    schema = {
        "type": "object",
        "properties": {
            "statefp": {"type": "number"},
            "countyfp": {"type": "number"},
            "sampleSize": {"type": "number"},
        },
        "required": ["statefp", "countyfp", "sampleSize"],
    }

    jsonschema.validate(instance=params, schema=schema)

    current_app.logger.info(
        f"Processing request for impact data for {params['statefp']} {params['countyfp']}"
    )

    industries = direct_industry_impacts_by_county(
        params["statefp"], params["countyfp"], params["sampleSize"]
    )

    current_app.logger.info(
        f"Computed impact data for {params['statefp']} {params['countyfp']}"
    )

    return {
        "industries": industries.to_dict("records"),
    }
