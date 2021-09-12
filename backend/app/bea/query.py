from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


def get_naics2017_concordance(db, params):
    naics2017_code = params["naics2017_code"]
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
        print("More than one hit.")
        return None
    else:
        return results[0]


def get_beacode_from_naics2017(db, params):
    concordance = get_naics2017_concordance(db, params)
    hits = get_beacode_from_naics2007(db, concordance)

    if len(hits) <= 1:
        return hits

    tgt_string = concordance["naics2007_title"]
    string_list = [hit["bea_title"] for hit in hits]

    tfidf_vectorizer = TfidfVectorizer()
    sparse_matrix = tfidf_vectorizer.fit_transform(string_list)
    doc_term_matrix = sparse_matrix.toarray()

    tgt_transform = tfidf_vectorizer.transform([tgt_string]).toarray()
    tgt_cosine = cosine_similarity(doc_term_matrix, tgt_transform)
    idx = np.argmax(tgt_cosine)
    print(idx)

    return hits[idx]


def get_beacode_from_naics2007(db, params):
    results = []
    naics2007_code = params["naics2007_code"]
    while len(results) == 0 and len(naics2007_code) >= 2:
        rows = db.execute(
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
            {"naics2007_code": naics2007_code},
        ).fetchall()

        results = [
            {
                "bea_code": row["BEA_CODE"],
                "bea_title": row["BEA_TITLE"],
                "naics2007_code": row["NAICS2007_CODE"],
            }
            for row in rows
        ]

        naics2007_code = naics2007_code[:-1]

    return results
