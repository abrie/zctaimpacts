import requests
import pandas


def urljoin(parts):
    return "/".join(part.strip("/") for part in parts)


# https://api.census.gov/data/2019/cbp/variables.html
def get_industries_by_zipcode(*, base_url, api_key, zipcode):
    response = requests.get(
        urljoin([base_url, "2019", "cbp"]),
        params={
            "get": ",".join(["NAICS2017", "EMP", "ESTAB"]),
            "for": f"zipcode:{zipcode}",
            "key": api_key,
        },
    )

    try:
        data = response.json()
    except ValueError:
        print("Unable to parse county response as json. Returning empty DataFrame.")
        return pandas.DataFrame()

    df = pandas.DataFrame.from_records(data[1:], columns=data[0])
    df = df.astype({"ESTAB": "int32", "EMP": "int32"})
    df = df[df["NAICS2017"].str.len() == 6]

    return df


def get_industries_by_county(*, base_url, api_key, statefp, countyfp):
    response = requests.get(
        urljoin([base_url, "2019", "cbp"]),
        params={
            "get": ",".join(["NAICS2017", "EMP", "ESTAB"]),
            "for": f"county:{countyfp:03d}",
            "in": f"state:{statefp:02d}",
            "key": api_key,
        },
    )

    try:
        data = response.json()
    except ValueError:
        print("Unable to parse county response as json. Returning empty DataFrame.")
        return pandas.DataFrame()

    df = pandas.DataFrame.from_records(data[1:], columns=data[0])
    df = df.astype({"ESTAB": "int32", "EMP": "int32"})
    df = df[df["NAICS2017"].str.len() == 6]

    return df


def get_industries_by_state(*, base_url, api_key, statefp):
    response = requests.get(
        urljoin([base_url, "2019", "cbp"]),
        params={
            "get": ",".join(["NAICS2017", "EMP", "ESTAB"]),
            "for": f"state:{statefp:02d}",
            "key": api_key,
        },
    )

    try:
        data = response.json()
    except ValueError:
        print("Unable to parse state response as json. Returning empty DataFrame.")
        return pandas.DataFrame()

    df = pandas.DataFrame.from_records(data[1:], columns=data[0])
    df = df.astype({"ESTAB": "int32", "EMP": "int32"})
    df = df[df["NAICS2017"].str.len() == 6]

    return df
