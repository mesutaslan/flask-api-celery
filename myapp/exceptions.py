from flask import jsonify


def template(data, code=500):
    return {'message': {'errors': {'body': data}}, 'status_code': code}


CONTACT_NOT_FOUND = template(['Contact not found'], code=404)
CONTACT_ALREADY_EXIST = template(['Contact already exist'], code=422)
UNKNOWN_ERROR = template([], code=500)
EMAIL_ALREADY_EXIST = template(['Email already exist'], code=422)


class InvalidUsage(Exception):
    status_code = 500

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_json(self):
        rv = self.message
        return jsonify(rv)

    @classmethod
    def contact_not_found(cls):
        return cls(**CONTACT_NOT_FOUND)

    @classmethod
    def contact_already_exist(cls):
        return cls(**CONTACT_ALREADY_EXIST)

    @classmethod
    def unknown_error(cls):
        return cls(**UNKNOWN_ERROR)

    @classmethod
    def email_not_owned(cls):
        return cls(**EMAIL_ALREADY_EXIST)