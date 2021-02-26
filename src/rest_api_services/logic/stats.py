from db.stats import get_views


def get_stats(session_id, formats):
    df = get_views(session_id)
    response = {}
    line = df.iloc[0]
    total = line.sum()
    for col in df.columns:
        if formats == 'percents':
            views = f'{line[col]/total:.1%}'
        else:
            views = str(line[col])
        response[col] = views
    return response
