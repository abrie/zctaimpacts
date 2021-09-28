import requests
import pandas


def urljoin(parts):
    return "/".join(part.strip("/") for part in parts)


# https://api.census.gov/data/2019/cbp/variables.html
def get_naics_by_zipcode(*, base_url, api_key, zipcode):
    data = requests.get(
        urljoin([base_url, "2019", "cbp"]),
        params={
            "get": ",".join(["NAICS2017"]),
            "for": f"zipcode:{zipcode}",
            "key": api_key,
        },
    ).json()

    results = []
    for d in data:
        code = d[0]
        if len(code) == 6:
            results.append(code)

    return results


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
    return df[df["NAICS2017"].str.len() == 6]
