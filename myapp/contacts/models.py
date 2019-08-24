from marshmallow import fields, validate
from myapp.extentions import db


class Contact(db.Model):
    __tablename__ = 'contacts'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)
    updated_at = db.Column(db.TIMESTAMP, onupdate=db.func.current_timestamp())
    is_active = db.Column(db.Boolean, default=True)

    def __init__(self, username, first_name, last_name):
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
