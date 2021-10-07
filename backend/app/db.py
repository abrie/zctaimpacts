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


def get_cbp_db():
    if "cbp_db" not in g:
        g.cbp_db = sqlite3.connect(
            current_app.config["CBP_DATABASE"], detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.cbp_db.text_factory = lambda b: b.decode(errors="ignore")
        g.cbp_db.row_factory = sqlite3.Row

    return g.cbp_db


def get_impacts_db():
    if "impacts_db" not in g:
        g.impacts_db = sqlite3.connect(
            current_app.config["IMPACTS_DATABASE"], detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.impacts_db.text_factory = lambda b: b.decode(errors="ignore")
        g.impacts_db.row_factory = sqlite3.Row

    return g.impacts_db


def close_dbs():
    db = g.pop("db", None)

    if db is not None:
        db.close()

    cbp_db = g.pop("cbp_db", None)

    if cbp_db is not None:
        cbp_db.close()

    impacts_db = g.pop("impacts_db", None)

    if impacts_db is not None:
        impacts_db.close()


def init_app(app):
    app.teardown_appcontext(close_dbs)
