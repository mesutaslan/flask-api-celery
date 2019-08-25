from myapp.extentions import db


class Email(db.Model):
    __tablename__ = 'emails'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False)
    contact_id = db.Column(db.Integer, db.ForeignKey('contacts.id', ondelete='CASCADE'), nullable=False)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)
    updated_at = db.Column(db.TIMESTAMP, onupdate=db.func.current_timestamp())
    is_active = db.Column(db.Boolean, default=True)

    def __init__(self, email, contact_id):
        self.contact_id = contact_id
        self.email = email
