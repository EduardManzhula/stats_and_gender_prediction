from re import match
from resources.errors import InvalidSessionID
from resources.errors import InvalidFormat
from resources.errors import SessionNotFound
from db.errors import get_session_id


def check_session_id(session_id):
    pattern = r"u\d{5}"
    if not match(pattern, session_id):
        raise InvalidSessionID
    result = get_session_id(session_id)
    if not result.fetchone():
        raise SessionNotFound


def check_format(formats):
    valid = ['absolute', 'percentage']
    if formats not in valid:
        raise InvalidFormat
