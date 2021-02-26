from flask import jsonify
from flask_restful import Resource, reqparse
from logic.stats import get_stats


class Stats(Resource):
    # noinspection PyMethodMayBeStatic
    def get(self, session_id):
        parser = reqparse.RequestParser()
        parser.add_argument('format', type=str, default='absolute')
        args = parser.parse_args()
        formats = args['format']
        answer = get_stats(session_id, formats)
        print(answer)
        return jsonify(answer)
