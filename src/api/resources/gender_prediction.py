from flask_restful import Resource

from api.logic.gender_prediction import predict_gender


class Gender_prediction(Resource):
    # noinspection PyMethodMayBeStatic
    def get(self, session_id):
        result = predict_gender(session_id)
        response = {"gender": result}
        return response
