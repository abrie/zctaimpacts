import os
import pandas as pd
import sqlite3


def NAICS2017_NAICS2012(db):
    df = pd.read_excel(
        os.path.join("raw", "2017_to_2012_NAICS.xlsx"),
        dtype=str,
        skiprows=2,
        usecols="A:D",
        index_col=None,
    )

    df.columns = [
        "NAICS2017_CODE",
        "NAICS2017_TITLE",
        "NAICS2012_CODE",
        "NAICS2012_TITLE",
    ]

    df.to_csv(
        os.path.join("out", "NAICS2017_NAICS2012.csv"),
        sep="|",
        encoding="utf-8",
        index=False,
    )

    df.to_sql("NAICS2017_NAICS2012", db, if_exists="replace", index=False)


def NAICS2007_NAICS2012(db):
    df = pd.read_excel(
        os.path.join("raw", "2007_to_2012_NAICS.xls"),
        dtype=str,
        skiprows=2,
        usecols="A:D",
        index_col=None,
    )

    df.columns = [
        "NAICS2007_CODE",
        "NAICS2007_TITLE",
        "NAICS2012_CODE",
        "NAICS2012_TITLE",
    ]

    df.to_csv(
        os.path.join("out", "NAICS2007_NAICS2012.csv"),
        sep="|",
        encoding="utf-8",
        index=False,
        header=[
            "NAICS2007_CODE",
            "NAICS2007_TITLE",
            "NAICS2012_CODE",
            "NAICS2012_TITLE",
        ],
    )

    df.to_sql("NAICS2007_NAICS2012", db, if_exists="replace", index=False)


def BEA_NAICS2007(db):
    df = pd.read_excel(
        os.path.join("raw", "GDPbyInd_GO_NAICS_1997-2016.xlsx"),
        sheet_name="NAICS codes",
        dtype=str,
        skiprows=[0, 1, 2, 3, 4, 5, 6],
        usecols="C,D,F",
    )
    df.columns = ["BEA_CODE", "BEA_TITLE", "NAICS2007_CODE"]
    df = df[df["BEA_CODE"].notna()]
    df = df[df["NAICS2007_CODE"].notna()]

    # In some cases there are mutiple comma-delimited NAICS codes,
    # so we 'explode' them into seperate rows.
    df = df.assign(NAICS2007_CODE=df["NAICS2007_CODE"].str.split(",")).explode(
        "NAICS2007_CODE"
    )

    # Ensure there is no extra whitespace.
    df = df.assign(NAICS2007_CODE=df["NAICS2007_CODE"].str.strip())

    # Some of the NAICS codes have hyphens with an extra number. This indicates a range,
    # so we need to generate a list and explode into additional rows.
    def range_to_list(x):
        parts = x.split("-")
        if len(parts) == 1:
            return x
        else:
            a = int(parts[0])
            b = int(parts[0][:-1] + parts[1])
            return [str(n) for n in range(a, b + 1)]

    df["NAICS2007_CODE"] = df["NAICS2007_CODE"].apply(range_to_list)
    df = df.explode("NAICS2007_CODE")

    df.to_csv(
        os.path.join("out", "GDPbyInd_GO_NAICS_1997-2016.csv"),
        sep="|",
        encoding="utf-8",
        index=False,
    )

    df.to_sql("BEA_NAICS2007", db, if_exists="replace", index=False)


if __name__ == "__main__":
    db = sqlite3.connect(os.path.join("out", "db.sqlite3"))

    NAICS2017_NAICS2012(db)
    NAICS2007_NAICS2012(db)
    BEA_NAICS2007(db)

    db.close()
