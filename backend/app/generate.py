import sqlite3
import json
import pandas
from flask import Blueprint
import app.operations
from app.db import get_impacts_db

blueprint = Blueprint("generate", __name__, url_prefix="/generate")


@blueprint.cli.command("counties-json")
def generate_counties_json():
    for row in app.operations.get_all_counties().itertuples():
        df = pandas.read_sql(
            "select * from county where geoid=:geoid",
            get_impacts_db(),
            params={"geoid": row.geoid},
        )
        print(row.geoid)
        fname = f"counties/US{row.geoid}.pqt"
        df.to_parquet(fname)


@blueprint.cli.command("zipcodes")
def generate_zipcodes():
    with sqlite3.connect("impacts.sqlite3") as con:
        for row in app.operations.get_all_zipcodes().itertuples():
            try:
                print(row)
                df = app.operations.compute_direct_industry_impacts_by_zipcode(
                    zipcode=row.zipcode
                )
                if df is None:
                    continue
                df["zipcode"] = row.zipcode
                df.to_sql("zipcode", con, if_exists="append", index_label="zipcode")
            except ValueError:
                print("Failed for zipcode:", row.zipcode)


@blueprint.cli.command("counties")
def generate_counties():
    with sqlite3.connect("impacts.sqlite3") as con:
        for row in app.operations.get_all_counties().itertuples():
            try:
                print(row)
                df = app.operations.compute_direct_industry_impacts_by_county(
                    statefp=row.statefp, countyfp=row.countyfp
                )
                if df is None:
                    continue
                df["countyfp"] = row.countyfp
                df["statefp"] = row.statefp
                df["geoid"] = row.geoid
                df.to_sql(
                    "county",
                    con,
                    if_exists="append",
                    index=False,
                )
            except ValueError as e:
                print(
                    f"Failed for state/{row.statefp}/county/{row.countyfp}",
                )
                print(e)


@blueprint.cli.command("states")
def generate_states():
    with sqlite3.connect("impacts.sqlite3") as con:
        for row in app.operations.get_all_states().itertuples():
            try:
                print(row)
                df = app.operations.compute_direct_industry_impacts_by_state(
                    statefp=row.statefp, sample_size=50
                )
                if df is None:
                    continue
                df["statefp"] = row.statefp
                df.to_sql("state", con, if_exists="append", index_label="statefp")
            except ValueError:
                print(f"Failed for state/{row.statefp}")
