import json

from .endpoint import Endpoint


def dump(j):
    print(json.dumps(j, indent=4, sort_keys=True))


def get_all_sectors(params):
    endpoint = Endpoint(params["base_url"], params["api_key"])
    model = endpoint.get_models()[0]
    return {"sectors": endpoint.get_sectors(model)}


"""
def run(args):
    base_url = "https://api.edap-cluster.com/useeio/api/"

    endpoint = Endpoint(base_url, secrets["apiKey"])
    models = endpoint.get_models()
    model = models[0]
    sectors = endpoint.get_sectors(model)
    sector = sectors[0]

    direct_requirements = endpoint.get_direct_requirements(model, sector)
    # Label the direct requirements valus with a sector id
    direct_requirements_df = pandas.DataFrame(
        direct_requirements, index=[sector["id"] for sector in sectors]
    )

    total_requirements = endpoint.get_total_requirements(model, sector)
    # Label the total requirements valus with a sector id
    total_requirements_df = pandas.DataFrame(
        total_requirements, index=[sector["id"] for sector in sectors]
    )

    elementary_flows = endpoint.get_elementary_flows(model)

    resource_use = endpoint.get_resource_use(model, elementary_flows[0])
    resource_use_dqi = endpoint.get_resource_use_dqi(model, elementary_flows[0])

    if resource_use_dqi == None:
        resource_use_dqi = [0] * len(resource_use)

    Bvaluename = "unit/$ gross output"
    dqname = "(Reliability,Time Corr,Geo Corr, Tech Corr, Data Collection)"

    B_df = pandas.DataFrame(
        {Bvaluename: resource_use, dqname: resource_use_dqi},
        index=[sector["id"] for sector in sectors],
    )

    indicators = endpoint.get_indicators(model)
    characterization_factors = endpoint.get_characterization_factors(
        model, indicators[0]
    )
    C_df = pandas.DataFrame(
        characterization_factors,
        index=[elementary_flow["id"] for elementary_flow in elementary_flows],
    )

    direct_impacts = endpoint.get_direct_impacts(model, indicators[0])
    direct_impacts_dqi = endpoint.get_direct_impacts_dqi(model, indicators[0])
    if direct_impacts_dqi == None:
        direct_impages_dqi = [0] * len(direct_impacts)

    D_df = pandas.DataFrame(
        {indicators[0]["id"]: direct_impacts, dqname: direct_impacts_dqi},
        index=[sector["id"] for sector in sectors],
    )

    lifecycle_impacts_per_dollar = endpoint.get_lifecycle_impacts_per_dollar(
        model, indicators[0]
    )
    lifecycle_impacts_per_dollar_dqi = endpoint.get_lifecycle_impacts_per_dollar_dqi(
        model, indicators[0]
    )

    U_df = pandas.DataFrame(
        {
            indicators[0]["id"]: lifecycle_impacts_per_dollar,
            dqname: lifecycle_impacts_per_dollar_dqi,
        },
        index=[sector["id"] for sector in sectors],
    )

    demands = endpoint.get_demands(model)
    demand_vector = endpoint.get_demand_vector(model, demands[0])
    dump(demand_vector)
"""
