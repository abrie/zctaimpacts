import requests
import json
import pandas


def load_secrets(f):
    return json.load(f)


def urljoin(parts):
    return "/".join(part.strip("/") for part in parts)


def run(args):
    base_url = "https://api.edap-cluster.com/useeio/api/"
    secrets = load_secrets(args.secrets)
    headers = {}
    headers["x-api-key"] = secrets["apiKey"]

    models_response = requests.get(urljoin([base_url, "models"]), headers=headers)
    models = models_response.json()
    model = models[0]

    sectors_response = requests.get(
        urljoin([base_url, model["id"], "sectors"]), headers=headers
    )
    sectors = sectors_response.json()

    A0_response = requests.get(
        urljoin([base_url, model["id"], "matrix", "A"]),
        params={"col": 0},
        headers=headers,
    )

    A0 = A0_response.json()
    A0_df = pandas.DataFrame(A0, index=[sector["id"] for sector in sectors])
    print(A0_df)
