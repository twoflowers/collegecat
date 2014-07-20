class Error(Exception):
    status_code = 400
    default_message = "General Error"
    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = self.default_message + " : " + message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


class InvalidUsage(Error):
    status_code = 400
    default_message = "Invalid Usage"

class Permission(Error):
    status_code = 403
    default_message = "Not Permitted"

class SystemError(Error):
    status_code = 500
    default_message = "System Error"