import requests
from collections import defaultdict


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
