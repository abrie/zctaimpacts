import sqlite3
import spatialite

from flask import current_app, g


def get_db():
    if "db" not in g:
        g.db = spatialite.connect(
            current_app.config["DATABASE"], detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.text_factory = lambda b: b.decode(errors="ignore")
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db():
    db = g.pop("db", None)

    if db is not None:
        db.close()


def init_app(app):
    app.teardown_appcontext(close_db)
