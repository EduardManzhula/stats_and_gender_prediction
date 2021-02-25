from flask import Flask, jsonify
from flask_restful import Api, Resource
from flask_restful import reqparse
import sqlalchemy
import configparser
from joblib import load
from functools import lru_cache
import pandas as pd


class Stats(Resource):
    def get(self, session_id):
        parser = reqparse.RequestParser()
        parser.add_argument('format', type=str)
        args = parser.parse_args()
        formats = args['format']
        if not formats:
            formats = 'absolute'
        response = {'views_a': 0,
                    'views_b': 0,
                    'views_c': 0,
                    'views_d': 0
                    }
        answer = get_views(session_id, formats)
        response.update(answer)
        return jsonify(response)


def get_views(session_id, formats):
    engine = init_engine()

    query = f"""WITH 
    stats as (
        SELECT session_id,
               COUNT(DISTINCT category_a) as views_a,
               COUNT(DISTINCT category_b) as views_b,
               COUNT(DISTINCT category_c) as views_c,
               COUNT(DISTINCT category_d) as views_d
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
    AND     session.session_id ='{session_id}'"""

    with engine.connect() as connection:
        df = pd.read_sql_query(query, connection)

    if not formats == 'absolute':
        pass

    response = {}
    line = df.iloc[0]
    for col in df.columns:
        response[col] = str(line[col])

    return response


class Gender_prediction(Resource):
    def get(self, session_id):
        result = predict_gender(session_id)
        response = {'gender': result}
        return jsonify(response)


@lru_cache
def init_model():
    return load('../models/model.joblib')


def get_data(session_id):
    engine = init_engine()
    query = f"""WITH 
    stats as (
        SELECT session_id,
               COUNT(DISTINCT category_d) as views
        FROM product
        GROUP BY session_id
    ),
    stats_a as(
        SELECT category_a as most_a,
               session_id,
               row_number() OVER (PARTITION BY session_id
                            ORDER BY COUNT(category_a) DESC) as rank
        FROM   product
        GROUP  BY 1, 2
    ),
    stats_b as(
        SELECT category_b as most_b,
               session_id,
               row_number() OVER (PARTITION BY session_id
                            ORDER BY COUNT(category_b) DESC) as rank
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
    AND     session.session_id ='{session_id}'"""

    with engine.connect() as connection:
        df = pd.read_sql_query(query, connection)
    return df


def predict_gender(session_id):
    clf = init_model()
    features = get_data(session_id)
    prediction = clf.predict(features)
    result = {0: 'male', 1: 'female'}[prediction[0]]
    return result


@lru_cache
def init_engine():
    config = configparser.ConfigParser()
    config.read("../configs/credentials.ini")
    eng = config['connection']['engine']
    hst = config['connection']['hostname']
    prt = config['connection']['port']
    usr = config['connection']['username']
    pwd = config['connection']['password']
    scm = config['connection']['schema']
    db_url = f'{eng}://{usr}:{pwd}@{hst}:{prt}/{scm}'
    engine = sqlalchemy.create_engine(db_url)
    return engine


def feature_extractor(data):
    result = data.copy()
    st = result['start_time']
    et = result['end_time']
    result['weekday'] = pd.DatetimeIndex(st).weekday
    result['duration'] = (et - st) // pd.Timedelta(minutes=1)
    result['hour'] = pd.DatetimeIndex(st).hour
    result.drop(['session_id', 'start_time', 'end_time'], axis=1, inplace=True)
    return result


app = Flask(__name__)
api = Api(app)
# http://127.0.0.1:5000/stats/u17882
api.add_resource(Stats, '/stats/<string:session_id>')
# http://127.0.0.1:5000/gender-prediction/u17882
api.add_resource(Gender_prediction, '/gender-prediction/<string:session_id>')


if __name__ == '__main__':
    app.run(debug=True)
