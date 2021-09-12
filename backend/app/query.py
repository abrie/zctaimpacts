import app.gis.query
import app.cbp.query
import app.bea.query
import app.useeio.query
from flask import Blueprint, request, current_app

from app.db import get_spatial_db
from app.db import get_db

blueprint = Blueprint("query", __name__, url_prefix="/query")


@blueprint.route("/zcta", methods=["POST"])
def zcta():
    def buildQueryParams(json_data):
        return {
            "x1": json_data["x1"],
            "y1": json_data["y1"],
            "x2": json_data["x2"],
            "y2": json_data["y2"],
        }

    return app.gis.query.get_zctas_intersecting_mbr(
        get_spatial_db(), buildQueryParams(request.get_json())
    )


@blueprint.route("/naics", methods=["POST"])
def naics():
    def buildQueryParams(json_data):
        return {
            "base_url": current_app.config["CENSUS_BASE_URL"],
            "api_key": current_app.config["CENSUS_API_KEY"],
            "zipcodes": json_data["zipcodes"],
        }

    return app.cbp.query.get_naics_by_zipcode(buildQueryParams(request.get_json()))


@blueprint.route("/bea/naics2007", methods=["POST"])
def bea_naics2007():
    def buildQueryparams(json_data):
        return {"naics2007_code": json_data["naics2007_code"]}

    results = app.bea.query.get_beacode_from_naics2007(
        get_db(), buildQueryparams(request.get_json())
    )

    return {"results": results}


@blueprint.route("/bea/naics2017", methods=["POST"])
def bea_naics2017():
    def buildQueryparams(json_data):
        return {"naics2017_code": json_data["naics2017_code"]}

    results = app.bea.query.get_beacode_from_naics2017(
        get_db(), buildQueryparams(request.get_json())
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
