import sqlite3
from flask import Blueprint
import app.operations

blueprint = Blueprint("generate", __name__, url_prefix="/generate")


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
                    statefp=row.statefp, countyfp=row.countyfp, sample_size=50
                )
                if df is None:
                    continue
                df["countyfp"] = row.countyfp
                df["statefp"] = row.statefp
                df.to_sql(
                    "county",
                    con,
                    if_exists="append",
                    index_label=["statefp", "countyfp"],
                )
            except ValueError:
                print(
                    f"Failed for state/{row.statefp}/county/{row.countyfp}",
                )


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
