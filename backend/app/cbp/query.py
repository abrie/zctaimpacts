import requests
from collections import defaultdict


def urljoin(parts):
    return "/".join(part.strip("/") for part in parts)


def bucket_by_zipcode(data):
    result = defaultdict(list)

    for i in data:
        if len(i[0]) >= 6:  # Look for full length NAICS codes
            result[i[1]].append(i[0])

    return result


# https://api.census.gov/data/2019/cbp/variables.html
def get_naics_by_zipcode(params):
    # state = "13"  # https://www.census.gov/library/reference/code-lists/ansi.html#par_textimage_3

    data = requests.get(
        urljoin([params["base_url"], "2019", "cbp"]),
        params={
            "get": ",".join(["NAICS2017"]),
            "for": f"zipcode:{params['zipcodes'][0]}",
            "key": params["api_key"],
        },
    ).json()

    return bucket_by_zipcode(data[1:])
