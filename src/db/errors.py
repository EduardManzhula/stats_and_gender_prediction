from db.db_connection import init_engine


def get_session_id(session_id):
    engine = init_engine()
    query = f"""
    SELECT * 
    FROM session
    WHERE session_id = '{session_id}'
    """
    with engine.connect() as connection:
        result = connection.execute(query)
    return result
