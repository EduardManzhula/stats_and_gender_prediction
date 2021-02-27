from flask_restful import Resource
from logic.gender_prediction import predict_gender
from logic.errors import check_session_id

class Gender_prediction(Resource):
    # noinspection PyMethodMayBeStatic
    def get(self, session_id):
        check_session_id(session_id)
        result = predict_gender(session_id)
        response = {'gender': result}
        return response
