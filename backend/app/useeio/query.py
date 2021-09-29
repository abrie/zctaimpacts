import json
import pandas

from .endpoint import Endpoint
from .matrices import get_matrices


def dump(j):
    print(json.dumps(j, indent=4, sort_keys=True))


def get_all_sectors(*, base_url, api_key):
    endpoint = Endpoint(base_url, api_key)
    model = endpoint.get_models()[0]
    sectors = endpoint.get_sectors(model)
    df = pandas.DataFrame(sectors)
    return df


def get_matricies():
    print(get_matrices())
