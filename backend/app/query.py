import app.gis.query
import app.cbp.query
from flask import Blueprint, request, current_app

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
        get_db(), buildQueryParams(request.get_json())
    )


@blueprint.route("/naics", methods=["POST"])
def naics():
    def buildQueryParams(json_data):
        return {
            "api_key": current_app.config["CENSUS_API_KEY"],
            "zipcodes": json_data["zipcodes"],
        }

    return app.cbp.query.get_naics_by_zipcode(buildQueryParams(request.get_json()))
