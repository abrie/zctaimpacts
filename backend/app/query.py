import app.gis.query
from flask import Blueprint, request

from app.db import get_db

blueprint = Blueprint("query", __name__, url_prefix="/query")


def buildQueryParams(json_data):
    return {
        "x1": json_data["x1"],
        "y1": json_data["y1"],
        "x2": json_data["x2"],
        "y2": json_data["y2"],
    }


@blueprint.route("/zcta", methods=["POST"])
def zcta():
    return app.gis.query.get_zctas_intersecting_mbr(
        get_db(), buildQueryParams(request.get_json())
    )
