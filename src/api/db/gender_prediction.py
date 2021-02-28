from api.db.db_connection import init_engine
from pandas import read_sql_query


def get_data(session_id):
    engine = init_engine()
    query = f"""
    WITH 
    stats AS (
        SELECT session_id,
               COUNT(DISTINCT category_d) AS views
        FROM product
        GROUP BY session_id
    ),
    stats_a AS (
        SELECT category_a AS most_a,
               session_id,
               row_number() OVER (PARTITION BY session_id
                            ORDER BY COUNT(category_a) DESC) AS rank
        FROM   product
        GROUP  BY 1, 2
    ),
    stats_b as(
        SELECT category_b AS most_b,
               session_id,
               row_number() OVER (PARTITION BY session_id
                            ORDER BY COUNT(category_b) DESC) AS rank
        FROM   product
        GROUP  BY 1, 2
    )
    SELECT  session.session_id,
            start_time,
            end_time,
            views,
            most_a,
            most_b
    FROM    session
    JOIN    stats
    ON      stats.session_id = session.session_id
    JOIN    stats_a
    ON      stats_a.session_id = session.session_id
    AND     stats_a.rank = 1
    JOIN    stats_b
    ON      stats_b.session_id = session.session_id
    AND     stats_b.rank = 1
    WHERE   session.gender is not NULL
    AND     session.session_id ='{session_id}'
    """

    with engine.connect() as connection:
        df = read_sql_query(query, connection)

    return df
