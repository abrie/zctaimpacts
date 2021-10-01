import json
import pandas


def get_zctas_intersecting_mbr(*, db, mbr):
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

    rows = db.execute(sql, mbr).fetchall()

    return {
        "results": [
            {"zipcode": row["ZCTA5CE20"], "geometry": json.loads(row["geometry"])}
            for row in rows
        ]
    }


def get_counties_intersecting_mbr(*, db, mbr):
    sql = """
    SELECT
      cast(county_geojson.STATEFP as INTEGER) as STATEFP,
      cast(county_geojson.COUNTYFP as INTEGER) as COUNTYFP,
      cast(county_geojson.GEOID as INTEGER) as GEOID,
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
    rows = db.execute(sql, mbr).fetchall()

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


def get_all_zipcodes(*, db):
    sql = """
    SELECT
        ZCTA5CE20 as zipcode,
        GEOID20 as geoid
    FROM
        zcta_geojson
      """

    df = pandas.read_sql_query(sql, db)
    df.columns = df.columns.str.lower()

    return df


def get_counties_by_state(*, db, statefp):
    sql = """
    SELECT
      cast(county_geojson.STATEFP as INTEGER) as STATEFP,
      cast(county_geojson.COUNTYFP as INTEGER) as COUNTYFP,
      cast(county_geojson.GEOID as INTEGER) as GEOID,
      county_geojson.NAME,
      county_fips.county_name,
      county_fips.state_name
    FROM
      county_geojson
      INNER JOIN county_fips ON county_fips.fips = county_geojson.GEOID
    WHERE
        STATEFP = :statefp
      """

    df = pandas.read_sql_query(sql, db, params={"statefp": statefp})
    df.columns = df.columns.str.lower()

    return df


def get_all_counties(*, db):
    sql = """
    SELECT
      cast(county_geojson.STATEFP as INTEGER) as STATEFP,
      cast(county_geojson.COUNTYFP as INTEGER) as COUNTYFP,
      cast(county_geojson.GEOID as INTEGER) as GEOID,
      county_geojson.NAME,
      county_fips.county_name,
      county_fips.state_name
    FROM
      county_geojson
      INNER JOIN county_fips ON county_fips.fips = county_geojson.GEOID
      """

    df = pandas.read_sql_query(sql, db)
    df.columns = df.columns.str.lower()

    return df


def get_all_states(*, db):
    sql = """
    SELECT
      cast(state_geojson.STATEFP as INTEGER) as STATEFP,
      cast(state_geojson.GEOID as INTEGER) as GEOID,
      state_geojson.NAME
    FROM
      state_geojson
      """

    df = pandas.read_sql_query(sql, db)
    df.columns = df.columns.str.lower()

    return df
