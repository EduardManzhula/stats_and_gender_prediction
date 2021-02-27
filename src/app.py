from flask import Flask
from flask_restful import Api
from resources.stats import Stats
from resources.gender_prediction import Gender_prediction
from resources.errors import errors
# Используется моделью
# noinspection PyUnresolvedReferences
from logic.gender_prediction import feature_extractor

app = Flask(__name__)
api = Api(app, errors=errors)
api.add_resource(Stats, '/stats/<string:session_id>')
api.add_resource(Gender_prediction, '/gender-prediction/<string:session_id>')

if __name__ == '__main__':
    app.run(debug=False)
