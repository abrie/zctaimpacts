import statistics
import random
import pandas

from flask import current_app
import app.useeio.query
import app.gis.query
import app.cbp.query
from app.db import get_spatial_db


def get_sector_crosswalk():
    matrices = app.useeio.query.get_matrices()
    return matrices["SectorCrosswalk"]


def get_indicators_matrix():
    matrices = app.useeio.query.get_matrices()
    return matrices["indicators"]


def get_direct_impacts_matrix():
    matrices = app.useeio.query.get_matrices()
    D = matrices["D"]
    D.columns = D.columns.str.rstrip("/US")
    return D


def get_all_counties():
    return app.gis.query.get_all_counties(spatial_db=get_spatial_db())


def get_all_states():
    return app.gis.query.get_all_states(spatial_db=get_spatial_db())


def get_counties_by_state(statefp):
    return app.gis.query.get_counties_by_state(
        spatial_db=get_spatial_db(), statefp=statefp
    )


def get_all_zipcodes():
    return app.gis.query.get_all_zipcodes(spatial_db=get_spatial_db())


def industries_by_zipcode(*, zipcode):
    return app.cbp.query.get_industries_by_zipcode(
        base_url=current_app.config["CENSUS_BASE_URL"],
        api_key=current_app.config["CENSUS_API_KEY"],
        zipcode=zipcode,
    )


def industries_by_county(*, statefp, countyfp):
    return app.cbp.query.get_industries_by_county(
        base_url=current_app.config["CENSUS_BASE_URL"],
        api_key=current_app.config["CENSUS_API_KEY"],
        statefp=statefp,
        countyfp=countyfp,
    )


def industries_by_state(*, statefp):
    return app.cbp.query.get_industries_by_state(
        base_url=current_app.config["CENSUS_BASE_URL"],
        api_key=current_app.config["CENSUS_API_KEY"],
        statefp=statefp,
    )


def direct_industry_impacts(industries, sample_size) -> pandas.DataFrame:
    crosswalk = get_sector_crosswalk()
    industries = industries.merge(crosswalk, left_on="NAICS2017", right_on="NAICS")
    impacts = get_direct_impacts_matrix().transpose()
    industries = industries.merge(impacts, left_on="BEA_Detail", right_index=True)
    grouped = industries.groupby("NAICS2017", as_index=False)

    aggregate_default = {x: "first" for x in industries.columns}
    aggregate_as_set = {x: lambda ser: set(ser) for x in impacts.columns}
    aggregation_operations = aggregate_default | aggregate_as_set
    aggregation_operations["BEA_Detail"] = lambda ser: list(set(ser))  # type: ignore
    aggregated = grouped.agg(aggregation_operations)

    def sample(row, col):
        population = list(row[col])
        if len(population) == 1:
            return population[0]

        k = row["ESTAB"]
        samples = [sum(random.choices(population, k=k)) for _ in range(0, sample_size)]
        return statistics.mean(samples)

    for impact in impacts.columns:
        aggregated[impact] = aggregated.apply(lambda row: sample(row, impact), axis=1)

    return aggregated


def direct_industry_impacts_by_zipcode(*, zipcode, sample_size):
    current_app.logger.info(
        f"Collecting direct industry impact data for zipcode/{zipcode}"
    )
    return direct_industry_impacts(
        industries_by_zipcode(zipcode=zipcode), sample_size=sample_size
    )


def direct_industry_impacts_by_county(state, county, sample_size):
    current_app.logger.info(
        f"Collecting direct industry impact data for state/{state}/county/{county}"
    )
    return direct_industry_impacts(
        industries_by_county(statefp=int(state), countyfp=int(county)),
        sample_size=sample_size,
    )


def direct_industry_impacts_by_state(state, sample_size):
    current_app.logger.info(f"Collecting direct industry impact data for state/{state}")
    return direct_industry_impacts(
        industries_by_state(statefp=int(state)),
        sample_size=sample_size,
    )
