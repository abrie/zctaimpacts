import sqlite3
import spatialite

from flask import current_app, g


def get_spatial_db():
    if "spatial_db" not in g:
        g.spatial_db = spatialite.connect(
            current_app.config["SPATIAL_DATABASE"], detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.spatial_db.text_factory = lambda b: b.decode(errors="ignore")
        g.spatial_db.row_factory = sqlite3.Row

    return g.spatial_db


def close_spatial_db():
    db = g.pop("spatial_db", None)

    if db is not None:
        db.close()


def init_app(app):
    app.teardown_appcontext(close_spatial_db)
