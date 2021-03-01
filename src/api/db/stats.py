from pandas import read_sql_query

from api.db.db_connection import init_engine


def get_views(session_id):
    engine = init_engine()
    query = f"""
    WITH
    stats AS (
        SELECT session_id,
               COUNT(DISTINCT category_a) AS views_a,
               COUNT(DISTINCT category_b) AS views_b,
               COUNT(DISTINCT category_c) AS views_c,
               COUNT(DISTINCT category_d) AS views_d
        FROM product
        GROUP BY session_id
    )
    SELECT  views_a,
            views_b,
            views_c,
            views_d
    FROM    session
    JOIN    stats
    ON      stats.session_id = session.session_id
    WHERE   session.gender is not NULL
    AND     session.session_id ='{session_id}'
    """
    with engine.connect() as connection:
        df = read_sql_query(query, connection)
    return df
