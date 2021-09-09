import json
from flask import Blueprint, request

from app.db import get_db

blueprint = Blueprint("gis", __name__, url_prefix="/gis")


def buildQueryParams(json_data):
    return {
        "x1": json_data["x1"],
        "y1": json_data["y1"],
        "x2": json_data["x2"],
        "y2": json_data["y2"],
    }


sql = """
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
      MBRIntersects(BuildMBR(:x1,:y1,:x2,:y2, 4326), "geometry")
  ) AS zcta_shp ON zcta_geojson.ZCTA5CE20 = zcta_shp.ZCTA5CE20
"""


@blueprint.route("/zcta", methods=["POST"])
def zcta():
    rows = (
        get_db()
        .execute(
            sql,
            buildQueryParams(request.get_json()),
        )
        .fetchall()
    )

    return {
        "results": [
            {"zipcode": row["ZCTA5CE20"], "geometry": json.loads(row["geometry"])}
            for row in rows
        ]
    }
