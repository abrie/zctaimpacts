from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pandas


def get_naics2017_concordance(*, db, naics2017_code):
    rows = db.execute(
        """
        SELECT
            NAICS2017_CODE,
            NAICS2017_TITLE,
            NAICS2017_NAICS2012.NAICS2012_CODE as NAICS2012_CODE,
            NAICS2017_NAICS2012.NAICS2012_TITLE as NAICS2012_TITLE,
            NAICS2007_NAICS2012.NAICS2007_CODE as NAICS2007_CODE,
            NAICS2007_NAICS2012.NAICS2007_TITLE as NAICS2007_TITLE
        FROM
            NAICS2017_NAICS2012
        INNER JOIN
            NAICS2007_NAICS2012 ON NAICS2007_NAICS2012.NAICS2012_CODE = NAICS2017_NAICS2012.NAICS2012_CODE
        WHERE
            NAICS2017_NAICS2012.NAICS2017_CODE=:naics2017_code
        """,
        {"naics2017_code": naics2017_code},
    ).fetchall()

    results = [
        {
            "naics2017_code": row["NAICS2017_CODE"],
            "naics2017_title": row["NAICS2017_TITLE"],
            "naics2012_code": row["NAICS2012_CODE"],
            "naics2012_title": row["NAICS2012_TITLE"],
            "naics2007_code": row["NAICS2007_CODE"],
            "naics2007_title": row["NAICS2007_TITLE"],
        }
        for row in rows
    ]

    if len(results) > 1:
        print("Warning: More than one hit for naics2017 code:", naics2017_code)

    return results[0]


def get_beacode_from_naics2017(*, db, naics2017_code):
    concordance = get_naics2017_concordance(db=db, naics2017_code=naics2017_code)
    df = get_beacode_from_naics2007(db=db, naics2007_code=concordance["naics2007_code"])

    if df.empty:
        title = concordance["naics2017_title"]
        return f"no hits for {naics2017_code} '{title}'"

    tgt_string = concordance["naics2007_title"]

    tfidf_vectorizer = TfidfVectorizer()

    tgt_cosine = cosine_similarity(
        tfidf_vectorizer.fit_transform(df["BEA_TITLE"]).toarray(),  # type: ignore
        tfidf_vectorizer.transform([tgt_string]).toarray(),  # type: ignore
    )

    df["COSINE"] = tgt_cosine.flatten().tolist()

    match = df.iloc[df["COSINE"].idxmax()]  # type: ignore
    return match.to_dict()


def get_beacode_from_naics2007(*, db, naics2007_code):
    df = pandas.DataFrame()
    while df.empty and len(naics2007_code) >= 2:
        df = pandas.read_sql(
            """
            SELECT
                BEA_CODE,
                BEA_TITLE,
                NAICS2007_CODE
            FROM
                BEA_NAICS2007
            WHERE
                NAICS2007_CODE=:naics2007_code
            """,
            db,
            params={"naics2007_code": naics2007_code},
        )

        naics2007_code = naics2007_code[:-1]

    return df
