import pandas as pd
from joblib import load
from functools import lru_cache
from db.gender_prediction import get_data
import configparser


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
    config = configparser.ConfigParser()
    config.read("configs/model.ini")
    load_path = config['model']['load_path']
    return load(load_path)


def predict_gender(session_id):
    clf = init_model()
    features = get_data(session_id)
    prediction = clf.predict(features)
    result = {0: 'male', 1: 'female'}[prediction[0]]
    return result
