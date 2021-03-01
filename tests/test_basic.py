from pytest import raises

from api.logic.gender_prediction import predict_gender
from api.logic.stats import get_stats
from api.resources.errors import InvalidFormat, InvalidSessionID, SessionNotFound


def test_stats():
    answer_abs = {"views_a": "1", "views_b": "1", "views_c": "1", "views_d": "2"}
    answer_per = {
        "views_a": "20%",
        "views_b": "20%",
        "views_c": "20%",
        "views_d": "40%",
    }
    assert get_stats("u17882", "absolute") == answer_abs
    assert get_stats("u17882", "percentage") == answer_per
    with raises(SessionNotFound):
        get_stats("u97882", "absolute")
    with raises(InvalidFormat):
        get_stats("u17882", "perrсentage")
    with raises(InvalidSessionID):
        get_stats("uf7882", "absolute")


def test_gender_prediction():
    assert predict_gender("u17882") == "female"
    assert predict_gender("u10001") == "male"
    with raises(SessionNotFound):
        predict_gender("u97882")
    with raises(InvalidSessionID):
        predict_gender("uf7882")


if __name__ == "__main__":
    test_stats()
    test_gender_prediction()
