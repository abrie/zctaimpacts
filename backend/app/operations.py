import statistics
import random
import pandas
from typing import Union

from flask import current_app
import app.useeio.matrices
import app.gis.query
import app.cbp.query
import app.cbp.database
from app.db import get_db, get_cbp_db


def get_sector_crosswalk():
    matrices = app.useeio.matrices.get_matrices()
    return matrices["SectorCrosswalk"]


def get_indicators_matrix():
    matrices = app.useeio.matrices.get_matrices()
    return matrices["indicators"]


def get_direct_impacts_matrix():
    matrices = app.useeio.matrices.get_matrices()
    D = matrices["D"]
    D.columns = D.columns.str.rstrip("/US")
    return D


def get_all_counties():
    return app.gis.query.get_all_counties(db=get_db())


def get_all_states():
    return app.gis.query.get_all_states(db=get_db())


def get_counties_by_state(statefp):
    return app.gis.query.get_counties_by_state(db=get_db(), statefp=statefp)


def get_all_zipcodes():
    return app.gis.query.get_all_zipcodes(db=get_db())


def industries_by_zipcode(*, zipcode) -> Union[pandas.DataFrame, None]:
    def use_database():
        return app.cbp.database.get_industries_by_zipcode(
            db=get_cbp_db(), zipcode=zipcode
        )

    def use_api():
        return app.cbp.query.get_industries_by_zipcode(
            base_url=current_app.config["CENSUS_BASE_URL"],
            api_key=current_app.config["CENSUS_API_KEY"],
            zipcode=zipcode,
        )

    return use_database()


def industries_by_county(*, statefp, countyfp) -> Union[pandas.DataFrame, None]:
    def use_database():
        return app.cbp.database.get_industries_by_county(
            db=get_cbp_db(), statefp=statefp, countyfp=countyfp
        )

    def use_api():
        return app.cbp.query.get_industries_by_county(
            base_url=current_app.config["CENSUS_BASE_URL"],
            api_key=current_app.config["CENSUS_API_KEY"],
            statefp=statefp,
            countyfp=countyfp,
        )

    return use_database()


def industries_by_state(*, statefp) -> Union[pandas.DataFrame, None]:
    def use_database():
        return app.cbp.database.get_industries_by_state(
            db=get_cbp_db(), statefp=statefp
        )

    def use_api():
        return app.cbp.query.get_industries_by_state(
            base_url=current_app.config["CENSUS_BASE_URL"],
            api_key=current_app.config["CENSUS_API_KEY"],
            statefp=statefp,
        )

    return use_database()


def compute_direct_industry_impacts(industries) -> Union[pandas.DataFrame, None]:
    if industries.shape[0] == 0:
        return None

    crosswalk = get_sector_crosswalk()
    industries = industries.merge(crosswalk, left_on="naics", right_on="NAICS")
    industries = industries.drop(["NAICS"], axis=1)
    impacts = get_direct_impacts_matrix().transpose()
    industries = industries.merge(impacts, left_on="BEA_Detail", right_index=True)
    grouped = industries.groupby("naics", as_index=False)

    aggregate_default = {x: "first" for x in industries.columns}
    aggregate_impacts = {x: "mean" for x in impacts.columns}
    aggregated = grouped.agg(aggregate_default | aggregate_impacts)

    return aggregated


def compute_direct_industry_impacts_by_zipcode(*, zipcode):
    current_app.logger.info(
        f"Computing direct industry impact data for zipcode/{zipcode}"
    )
    return compute_direct_industry_impacts(industries_by_zipcode(zipcode=zipcode))


def compute_direct_industry_impacts_by_county(statefp, countyfp, sample_size):
    current_app.logger.info(
        f"Computing direct industry impact data for state/{statefp}/county/{countyfp}"
    )
    return compute_direct_industry_impacts(
        industries_by_county(statefp=int(statefp), countyfp=int(countyfp))
    )


def compute_direct_industry_impacts_by_state(statefp, sample_size):
    current_app.logger.info(
        f"Computing direct industry impact data for state/{statefp}"
    )
    return compute_direct_industry_impacts(industries_by_state(statefp=int(statefp)))
