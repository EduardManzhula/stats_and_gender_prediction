from re import match

from api.db.errors import get_session_id
from api.resources.errors import InvalidFormat, InvalidSessionID, SessionNotFound


def check_session_id(session_id):
    pattern = r"u\d{5}"
    if not match(pattern, session_id):
        raise InvalidSessionID
    result = get_session_id(session_id)
    if not result.fetchone():
        raise SessionNotFound


def check_format(formats):
    valid = ["absolute", "percentage"]
    if formats not in valid:
        raise InvalidFormat
