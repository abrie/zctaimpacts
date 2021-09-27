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
            "get": ",".join(["NAICS2017", "PAYANN", "EMP", "ESTAB"]),
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

    rows = [
        pandas.DataFrame(
            data={
                "NAICS2017_CODE": [d[0]],
                "PAYANN": [int(d[1])],
                "EMP": [int(d[2])],
                "ESTAB": [int(d[3])],
            }
        )
        for d in data
        if len(d[0]) == 6
    ]

    return pandas.concat(rows)
