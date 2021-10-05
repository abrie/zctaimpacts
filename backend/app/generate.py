import sqlite3
import pandas
from flask import Blueprint

import app.operations

blueprint = Blueprint("generate", __name__, url_prefix="/generate")


@blueprint.cli.command("zipcodes")
def generate_zipcodes():
    con = sqlite3.connect("zipcodes.sqlite3")
    for row in app.operations.get_all_zipcodes().itertuples():
        print(row.zipcode)
        df = app.operations.direct_industry_impacts_by_zipcode(
            zipcode=row.zipcode, sample_size=50
        )
        if df is None:
            print("No data for:", row.zipcode)
            continue
        df = df.drop(["BEA_Detail"], axis=1)
        df.to_sql("zipcode", con, if_exists="append")
    con.close()
