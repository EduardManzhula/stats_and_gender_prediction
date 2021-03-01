from api.db.stats import get_views
from api.logic.errors import check_format, check_session_id


def get_stats(session_id, formats):
    check_session_id(session_id)
    check_format(formats)
    df = get_views(session_id)
    response = {}
    line = df.iloc[0]
    total = line.sum()
    for col in df.columns:
        if formats == "percentage":
            views = f"{line[col]/total:.0%}"
        else:
            views = str(line[col])
        response[col] = views
    return response
