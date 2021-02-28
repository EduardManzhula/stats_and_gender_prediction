class InternalServerError(Exception):
    pass


class InvalidSessionID(Exception):
    pass


class InvalidFormat(Exception):
    pass


class SessionNotFound(Exception):
    pass


errors = {
    "InternalServerError": {
        "message": "Internal Server Error",
        "status": 500
    },
    "InvalidSessionID": {
        "message": "Invalid session id",
        "status": 400
    },
    "InvalidFormat": {
        "message": "format is not supported",
        "status": 400
    },
    "SessionNotFound": {
        "message": "Session is not found",
        "status": 406
    }
}
