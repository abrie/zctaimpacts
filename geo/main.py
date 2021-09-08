import json
import spatialite


def values(geojson):
    for feature in geojson["features"]:
        yield (
            json.dumps(feature["geometry"]),
            feature["properties"]["ZCTA5CE20"],
        )


print("Opening database.")
with spatialite.connect("db.sqlite3") as db:
    db.execute("""ALTER TABLE zcta ADD COLUMN geojson TEXT""")
    db.execute("""PRAGMA synchronous = EXTRA""")
    db.execute("""PRAGMA journal_mode = WAL""")
    print("Opening Geojson file.")
    with open("geo.json", "rb") as f:
        print("Decoding JSON")
        geojson = json.load(f)
        print("Building statements.")
        db.executemany(
            """UPDATE zcta set geojson=? WHERE ZCTA5CE20=?""", values(geojson)
        )
        print("Committing data.")
        db.commit()

print("Done.")
