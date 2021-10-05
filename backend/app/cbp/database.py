import pandas
from typing import Union


# https://api.census.gov/data/2019/cbp/variables.html
def get_industries_by_zipcode(*, db, zipcode) -> Union[pandas.DataFrame, None]:
    df = pandas.read_sql(
        "SELECT naics, est FROM zipcode where zip=:zipcode",
        con=db,
        params={"zipcode": zipcode},
    )

    if df is None:
        return None

    df = df.rename(columns={"est": "establishments"})
    df = df.astype({"establishments": "int32"})
    df = df[df["naics"].str.contains(r"\d{6,6}")]
    return df


def get_industries_by_county(*, db, statefp, countyfp) -> Union[pandas.DataFrame, None]:
    df = pandas.read_sql(
        "SELECT naics, est FROM county WHERE fipstate=:statefp and fipscty=:countyfp",
        con=db,
        params={"statefp": statefp, "countyfp": countyfp},
    )

    if df is None:
        return None

    df = df.rename(columns={"est": "establishments"})
    df = df.astype({"establishments": "int32"})
    df = df[df["naics"].str.contains(r"\d{6,6}")]
    return df


def get_industries_by_state(*, db, statefp) -> Union[pandas.DataFrame, None]:
    df = pandas.read_sql(
        "SELECT naics, est FROM state WHERE fipstate=:statefp",
        con=db,
        params={"statefp": statefp},
    )

    if df is None:
        return None

    df = df.rename(columns={"est": "establishments"})
    df = df.astype({"establishments": "int32"})
    df = df[df["naics"].str.contains(r"\d{6,6}")]
    return df
