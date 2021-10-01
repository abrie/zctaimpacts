import pandas
import importlib.resources as pkg_resources

matrices = None


def load_matrices() -> dict:
    from . import resources

    with pkg_resources.path(resources, "USEEIOv2.0.xlsx") as filepath:
        with pandas.ExcelFile(filepath) as xls:
            return {
                "D": pandas.read_excel(xls, "D", header=0, index_col=0),
                "SectorCrosswalk": pandas.read_excel(xls, "SectorCrosswalk", header=0),
                "indicators": pandas.read_excel(
                    xls, "indicators", header=0, index_col=0
                ),
            }


def get_matrices() -> dict:
    global matrices

    if matrices is None:
        matrices = load_matrices()

    return matrices
