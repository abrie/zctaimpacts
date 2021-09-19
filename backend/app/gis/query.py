import json


def get_zctas_intersecting_mbr(*, spatial_db, mbr):
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

    rows = spatial_db.execute(sql, mbr).fetchall()

    return {
        "results": [
            {"zipcode": row["ZCTA5CE20"], "geometry": json.loads(row["geometry"])}
            for row in rows
        ]
    }


def get_counties_intersecting_mbr(*, spatial_db, mbr):
    sql = """
    SELECT
      county_geojson.STATEFP,
      county_geojson.COUNTYFP,
      county_geojson.GEOID,
      county_geojson.geometry
    FROM
      county_geojson
      INNER JOIN (
        SELECT
          STATEFP,
          COUNTYFP,
          GEOID
        FROM
          county_shp
        WHERE
          MBRIntersects(BuildMBR(:x1,:y1,:x2,:y2, 4326), "geometry")
      ) AS county_shp ON county_geojson.GEOID = county_shp.GEOID
    """
    rows = spatial_db.execute(sql, mbr).fetchall()

    return {
        "results": [
            {
                "statefp": row["STATEFP"],
                "countyfp": row["COUNTYFP"],
                "geoid": row["GEOID"],
                "geometry": json.loads(row["geometry"]),
            }
            for row in rows
        ]
    }
