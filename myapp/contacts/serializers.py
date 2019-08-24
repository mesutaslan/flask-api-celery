from marshmallow import fields, validate
from myapp.extentions import ma

class ContactSchema(ma.Schema):
    id = fields.Integer()
    username = fields.String(required=True, validate=validate.Length(6))
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    created_at = fields.Time()
    updated_at = fields.Time()
    is_active = fields.Boolean()
