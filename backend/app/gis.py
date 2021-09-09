import json
from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from werkzeug.exceptions import abort

from app.db import get_db

blueprint = Blueprint("gis", __name__, url_prefix="/gis")


@blueprint.route("/zcta", methods=["POST"])
def zcta():
    db = get_db()
    json_data = request.get_json()

    rows = db.execute(
        """
        SELECT
          zcta_geojson.ZCTA5CE20,
          zcta_geojson.geometry
        FROM
          zcta_geojson
          INNER JOIN (
            SELECT
              ZCTA5CE20
            FROM
              zcta_shp
            WHERE
              MBRIntersects(BuildMBR(?, ?, ?, ?, 4326), "geometry")
          ) AS zcta_shp ON zcta_geojson.ZCTA5CE20 = zcta_shp.ZCTA5CE20
        """,
        (json_data["x1"], json_data["y1"], json_data["x2"], json_data["y2"]),
    ).fetchall()

    return {
        "results": [
            {"zipcode": row["ZCTA5CE20"], "geometry": json.loads(row["geometry"])}
            for row in rows
        ]
    }
