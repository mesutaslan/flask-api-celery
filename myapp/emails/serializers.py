from marshmallow import fields
from myapp.extentions import ma


class EmailSchema(ma.Schema):
    id = fields.Integer()
    email = fields.Email(required=True)
    contact_id = fields.Integer()
    created_at = fields.Time()
    updated_at = fields.Time()
    is_active = fields.Boolean()
