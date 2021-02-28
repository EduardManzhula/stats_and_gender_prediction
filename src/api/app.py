from flask import Flask
from flask_restful import Api
from api.resources.stats import Stats
from api.resources.gender_prediction import Gender_prediction
from api.resources import errors


app = Flask(__name__)
api = Api(app, errors=errors)
api.add_resource(Stats, '/stats/<string:session_id>')
api.add_resource(Gender_prediction, '/gender-prediction/<string:session_id>')

if __name__ == '__main__':
    app.run(debug=False)
