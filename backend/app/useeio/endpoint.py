import requests


def urljoin(parts):
    return "/".join(part.strip("/") for part in parts)


class Endpoint:
    # https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6192422/
    # Footnote 2
    dqi_names = [
        "Data Reliability",
        "Temporal Correlation",
        "Geographic Correlation",
        "Technological Correlation",
        "Data Collection Methods",
    ]

    def __init__(self, base_url, api_key):
        self.base_url = base_url
        self.headers = {"x-api-key": api_key}

    def get_models(self):
        response = requests.get(
            urljoin([self.base_url, "models"]), headers=self.headers
        )
        return response.json()

    def get_sectors(self, model):
        response = requests.get(
            urljoin([self.base_url, model["id"], "sectors"]), headers=self.headers
        )
        return response.json()

    def get_direct_requirements(self, model, sector):
        # May be referred to as the 'Technology' or 'A' matrix
        response = requests.get(
            urljoin([self.base_url, model["id"], "matrix", "A"]),
            params={"col": sector["index"]},
            headers=self.headers,
        )
        return response.json()

    def get_total_requirements(self, model, sector):
        response = requests.get(
            urljoin([self.base_url, model["id"], "matrix", "L"]),
            params={"col": sector["index"]},
            headers=self.headers,
        )
        return response.json()

    def get_elementary_flows(self, model):
        response = requests.get(
            urljoin([self.base_url, model["id"], "flows"]), headers=self.headers
        )
        return response.json()

    def get_resource_use(self, model, elementary_flow):
        # B is the SATELLITE TABLE matrix for RESOURCE USE
        # This provides the resource use or emission intensities for all sectors for
        # an elementary flow in the model.
        response = requests.get(
            urljoin([self.base_url, model["id"], "matrix", "B"]),
            params={"row": elementary_flow["index"]},
            headers=self.headers,
        )
        return response.json()

    def get_resource_use_dqi(self, model, elementary_flow):
        response = requests.get(
            urljoin([self.base_url, model["id"], "matrix", "B_dqi"]),
            params={"row": elementary_flow["index"]},
            headers=self.headers,
        )
        try:
            return response.json()
        except:
            return None

    def get_indicators(self, model):
        response = requests.get(
            urljoin([self.base_url, model["id"], "indicators"]), headers=self.headers
        )
        return response.json()

    def get_characterization_factors(self, model, indicator):
        response = requests.get(
            urljoin([self.base_url, model["id"], "matrix", "C"]),
            params={"row": indicator["index"]},
            headers=self.headers,
        )
        return response.json()

    def get_direct_impacts(self, model, indicator):
        response = requests.get(
            urljoin([self.base_url, model["id"], "matrix", "D"]),
            params={"row": indicator["index"]},
            headers=self.headers,
        )
        return response.json()

    def get_direct_impacts_dqi(self, model, indicator):
        response = requests.get(
            urljoin([self.base_url, model["id"], "matrix", "D_dqi"]),
            params={"row": indicator["index"]},
            headers=self.headers,
        )
        try:
            return response.json()
        except:
            return None

    def get_lifecycle_impacts_per_dollar(self, model, indicator):
        response = requests.get(
            urljoin([self.base_url, model["id"], "matrix", "U"]),
            params={"row": indicator["index"]},
            headers=self.headers,
        )
        return response.json()

    def get_lifecycle_impacts_per_dollar_dqi(self, model, indicator):
        response = requests.get(
            urljoin([self.base_url, model["id"], "matrix", "U_dqi"]),
            params={"row": indicator["index"]},
            headers=self.headers,
        )
        try:
            return response.json()
        except:
            return None

    def get_demands(self, model):
        response = requests.get(
            urljoin([self.base_url, model["id"], "demands"]), headers=self.headers
        )
        return response.json()

    def get_demand_vector(self, model, demand):
        response = requests.get(
            urljoin([self.base_url, model["id"], "demands", demand["id"]]),
            headers=self.headers,
        )
        return response.json()
