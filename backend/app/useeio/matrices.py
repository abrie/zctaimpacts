import pandas
import importlib.resources as pkg_resources

matrices = None


def load_matrices() -> dict:
    from . import resources

    with pkg_resources.path(resources, "USEEIOv2.0.xlsx") as filepath:
        with pandas.ExcelFile(filepath) as xls:
            return {
                # "A": pandas.read_excel(xls, "A", header=0, index_col=0),
                # "B": pandas.read_excel(xls, "B", header=0, index_col=0),
                # "C": pandas.read_excel(xls, "C", header=0, index_col=0),
                "D": pandas.read_excel(xls, "D", header=0, index_col=0),
                "SectorCrosswalk": pandas.read_excel(xls, "SectorCrosswalk", header=0)
                # "L": pandas.read_excel(xls, "L", header=0, index_col=0),
                # "LCI": pandas.read_excel(xls, "LCI", header=0, index_col=0),
                # "U": pandas.read_excel(xls, "U", header=0, index_col=0),
            }


def get_matrices() -> dict:
    global matrices

    if matrices is None:
        matrices = load_matrices()

    return matrices
