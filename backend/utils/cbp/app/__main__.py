import os
import pandas
import sqlite3
from typing import cast


def load_raw_csv(filename, encoding="UTF-8") -> pandas.DataFrame:
    result = pandas.read_csv(os.path.join("raw", filename), encoding=encoding)
    return cast(pandas.DataFrame, result)


def county(db):
    df: pandas.DataFrame = load_raw_csv("cbp19co.txt")
    df.to_sql("county", db, if_exists="replace", index=False)


def state(db):
    df: pandas.DataFrame = load_raw_csv("cbp19st.txt")
    df.to_sql("state", db, if_exists="replace", index=False)


def zipcode(db):
    df: pandas.DataFrame = load_raw_csv("zbp19detail.txt", encoding="ISO-8859-1")
    df.to_sql("zipcode", db, if_exists="replace", index=False)


if __name__ == "__main__":
    db = sqlite3.connect(os.path.join("out", "db.sqlite3"))
    print("Loading counties...")
    county(db)
    print("Loading States...")
    state(db)
    print("Loading Zipcodes...")
    zipcode(db)
    print("Done.")

    db.close()
