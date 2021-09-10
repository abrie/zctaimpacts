import requests
from collections import defaultdict


def get_naics_by_zipcode(params):
    year = "2019"
    dsource = "cbp"
    cols = "NAICS2017"
    state = "13"  # https://www.census.gov/library/reference/code-lists/ansi.html#par_textimage_3
    api_key = params["api_key"]
    zipcodes = params["zipcodes"]

    base_url = f"https://api.census.gov/data/{year}/{dsource}"
    data_url = f"{base_url}?get={cols}&for=zipcode:{zipcodes[0]}&for=state:{state}&key={api_key}"

    data = requests.get(data_url).json()
    result = defaultdict(list)
    for i in data[1:]:
        result[i[1]].append(i[0])

    return result
