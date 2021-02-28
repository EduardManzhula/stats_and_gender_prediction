import pandas as pd
from joblib import load
from functools import lru_cache
from api.db.gender_prediction import get_data
from api.logic.errors import check_session_id
import pathlib


def feature_extractor(data):
    """
    Функция используется моделью для обработки данных
    """
    result = data.copy()
    st = result['start_time']
    et = result['end_time']
    result['weekday'] = pd.DatetimeIndex(st).weekday
    result['duration'] = (et - st) // pd.Timedelta(minutes=1)
    result['hour'] = pd.DatetimeIndex(st).hour
    result.drop(['session_id', 'start_time', 'end_time'], axis=1, inplace=True)
    return result


@lru_cache
def init_model():
    load_path = pathlib.Path(__file__).parent.parent / 'models' / 'model.joblib'
    model = load(load_path)
    return model


def predict_gender(session_id):
    check_session_id(session_id)
    clf = init_model()
    features = get_data(session_id)
    features = feature_extractor(features)
    prediction = clf.predict(features)
    result = {0: 'male', 1: 'female'}[prediction[0]]
    return result
