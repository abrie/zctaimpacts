import json
import spatialite


def run(args):
    print("Opening database", (args.db))
    with spatialite.connect(args.db) as db:
        db.execute(
            """SELECT zcta_geojson.ZCTA5CE20, zcta_geojson.geometry from zcta_geojson inner join (select ZCTA5CE20 from zcta_shp where MBRContains(BuildMBR(?,?,?,?, 4326), "geometry")) as zcta_shp ON zcta_geojson.ZCTA5CE20 = zcta_shp.ZCTA5CE20""",
            (-85.605165, 30.357851, -80.839729, 35.000659),
        )
