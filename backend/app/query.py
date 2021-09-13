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
    json_data = request.get_json()
    mbr = {
        "x1": json_data["x1"],
        "y1": json_data["y1"],
        "x2": json_data["x2"],
        "y2": json_data["y2"],
    }

    return app.gis.query.get_zctas_intersecting_mbr(
        spatial_db=get_spatial_db(), mbr=mbr
    )


@blueprint.route("/zipcode", methods=["POST"])
def zipcode():
    json_data = request.get_json()

    codes = app.cbp.query.get_naics_by_zipcode(
        base_url=current_app.config["CENSUS_BASE_URL"],
        api_key=current_app.config["CENSUS_API_KEY"],
        zipcode=json_data["zipcode"],
    )

    results = [
        app.bea.query.get_beacode_from_naics2017(get_db(), naics2017_code=code)
        for code in codes
    ]

    return {"results": results}


@blueprint.route("/naics", methods=["POST"])
def naics():
    json_data = request.get_json()
    results = app.cbp.query.get_naics_by_zipcode(
        base_url=current_app.config["CENSUS_BASE_URL"],
        api_key=current_app.config["CENSUS_API_KEY"],
        zipcode=json_data["zipcode"],
    )
    return {"results": results}


@blueprint.route("/bea/naics2007", methods=["POST"])
def bea_naics2007():
    json_data = request.get_json()

    results = app.bea.query.get_beacode_from_naics2007(
        db=get_db(), naics2007_code=json_data["naics2007_code"]
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
