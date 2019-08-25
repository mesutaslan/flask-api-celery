from marshmallow import fields, validate
from myapp.extentions import ma


class ContactSchema(ma.Schema):
    id = fields.Integer()
    username = fields.String(required=True, validate=validate.Length(6))
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    emails = fields.Method('getEmail')
    created_at = fields.Time()
    updated_at = fields.Time()
    is_active = fields.Boolean()

    def getEmail(self, contact):
        email_obj = []
        for email in contact.emails:
            email_obj.append({
                'id': email.id,
                'email': email.email
            })
        return email_obj
