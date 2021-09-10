import json

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


def get_zctas_intersecting_mbr(db, mbr):
    rows = db.execute(sql, mbr).fetchall()

    return {
        "results": [
            {"zipcode": row["ZCTA5CE20"], "geometry": json.loads(row["geometry"])}
            for row in rows
        ]
    }
