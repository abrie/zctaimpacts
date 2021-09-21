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
      cast(county_geojson.STATEFP as INTEGER) as STATEFP,
      cast(county_geojson.COUNTYFP as INTEGER) as COUNTYFP,
      county_geojson.GEOID,
      county_geojson.NAME,
      county_geojson.geometry,
      county_fips.county_name,
      county_fips.state_name
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
      INNER JOIN county_fips ON county_fips.fips = county_geojson.GEOID
    """
    rows = spatial_db.execute(sql, mbr).fetchall()

    return {
        "results": [
            {
                "statefp": row["STATEFP"],
                "countyfp": row["COUNTYFP"],
                "county_name": row["county_name"],
                "state_name": row["state_name"],
                "geoid": row["GEOID"],
                "name": row["NAME"],
                "geometry": json.loads(row["geometry"]),
            }
            for row in rows
        ]
    }
