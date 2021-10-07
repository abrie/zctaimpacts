import click
import jsonschema
import json
from flask import Blueprint, request, current_app

import app.operations
import app.gis.query
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


@blueprint.cli.command("indicators")
def print_indicators():
    print(app.operations.get_indicators_matrix().to_html())


@blueprint.route("/indicators", methods=["GET"])
def serve_indicators():
    return {"indicators": app.operations.get_indicators_matrix().to_dict("records")}


@blueprint.cli.command("industries_by_county")
@click.argument("state", type=int)
@click.argument("county", type=int)
def print_industries_by_county(state, county):
    print(app.operations.industries_by_county(statefp=state, countyfp=county).to_html())


@blueprint.cli.command("industries_by_state")
@click.argument("state", type=int)
def print_industries_by_state(state):
    print(app.operations.industries_by_state(statefp=state).to_html())


@blueprint.cli.command("industries_by_zipcode")
@click.argument("zipcode", type=int)
def print_industries_by_zipcode(zipcode):
    print(app.operations.industries_by_zipcode(zipcode=zipcode).to_html())


@blueprint.cli.command("direct_impacts_matrix")
def print_direct_impacts_matrix():
    print(app.operations.get_direct_impacts_matrix().transpose())


@blueprint.cli.command("direct_industry_impacts_by_zipcode")
@click.argument("zipcode", type=int)
def print_direct_industry_impacts_by_zipcode(zipcode):
    print(
        app.operations.get_direct_industry_impacts_by_zipcode(zipcode=zipcode).to_html()
    )


@blueprint.cli.command("direct_industry_impacts_by_county")
@click.argument("state", type=int)
@click.argument("county", type=int)
def print_direct_industry_impacts_by_county(state, county):
    print(app.operations.get_direct_industry_impacts_by_county(state, county).to_html())


@blueprint.cli.command("direct_industry_impacts_by_state")
@click.argument("state", type=int)
def print_direct_industry_impacts_by_state(state):
    print(app.operations.get_direct_industry_impacts_by_state(state).to_html())


@blueprint.cli.command("sector_crosswalk")
def print_sector_crosswalk():
    print(json.dumps(app.operations.get_sector_crosswalk().to_dict("records")))


@blueprint.cli.command("all_counties")
def print_all_counties():
    print(json.dumps(app.operations.get_all_counties().to_dict("records")))


@blueprint.cli.command("counties_by_state")
@click.argument("statefp", type=int)
def print_counties_by_state(statefp):
    print(
        json.dumps(
            app.operations.get_counties_by_state(statefp=statefp).to_dict("records")
        )
    )


@blueprint.cli.command("all_zipcodes")
def print_all_zipcodes():
    print(json.dumps(app.operations.get_all_zipcodes().to_dict("records")))


@blueprint.cli.command("all_states")
def print_all_states():
    print(json.dumps(app.operations.get_all_states().to_dict("records")))


@blueprint.route("/zipcode/all", methods=["GET"])
def serve_get_all_zipcodes():
    current_app.logger.info("Request for all zipcodes.")
    return {"results": app.operations.get_all_zipcodes().to_dict("records")}


@blueprint.route("/county/all", methods=["GET"])
def serve_get_all_counties():
    current_app.logger.info("Request for all counties.")
    return {"results": app.operations.get_all_counties().to_dict("records")}


@blueprint.route("/state/all", methods=["GET"])
def serve_get_all_states():
    current_app.logger.info("Request for all states.")
    return {"results": app.operations.get_all_states().to_dict("records")}


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

    return app.gis.query.get_zctas_intersecting_mbr(db=get_db(), mbr=mbr)


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

    result = app.gis.query.get_counties_intersecting_mbr(db=get_db(), mbr=mbr)

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
        },
        "required": ["zipcode"],
    }

    jsonschema.validate(instance=params, schema=schema)

    current_app.logger.info(
        f"Processing request for impact data for zipcode {params['zipcode']}"
    )

    industries = app.operations.get_direct_industry_impacts_by_zipcode(
        zipcode=params["zipcode"]
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
        },
        "required": ["statefp", "countyfp"],
    }

    jsonschema.validate(instance=params, schema=schema)

    current_app.logger.info(
        f"Processing request for impact data for {params['statefp']} {params['countyfp']}"
    )

    industries = app.operations.get_direct_industry_impacts_by_county(
        params["statefp"], params["countyfp"]
    )

    current_app.logger.info(
        f"Computed impact data for {params['statefp']} {params['countyfp']}"
    )

    return {
        "industries": industries.to_dict("records"),
    }


@blueprint.route("/state/impacts", methods=["POST"])
def serve_direct_industry_impacts_by_state():
    params = request.get_json()
    if params is None:
        raise InvalidAPIUsage("No JSON body found.")

    schema = {
        "type": "object",
        "properties": {
            "statefp": {"type": "number"},
        },
        "required": ["statefp"],
    }

    jsonschema.validate(instance=params, schema=schema)

    current_app.logger.info(
        f"Processing request for impact data for state/{params['statefp']}"
    )

    industries = app.operations.get_direct_industry_impacts_by_state(params["statefp"])

    current_app.logger.info(f"Computed impact data for state/{params['statefp']}")

    return {
        "industries": industries.to_dict("records"),
    }
