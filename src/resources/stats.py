from flask_restful import Resource, reqparse
from logic.stats import get_stats
from logic.errors import check_session_id
from logic.errors import check_format


class Stats(Resource):
    # noinspection PyMethodMayBeStatic
    def get(self, session_id):
        check_session_id(session_id)
        parser = reqparse.RequestParser()
        parser.add_argument('format', type=str, default='absolute')
        args = parser.parse_args()
        formats = args['format']
        check_format(formats)
        response = get_stats(session_id, formats)
        return response
