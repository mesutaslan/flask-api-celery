from flask import request
from flask_restful import Resource
from myapp.emails.models import Email
from myapp.emails.serializers import EmailSchema
from myapp.exceptions import AppError

emails_schema = EmailSchema(many=True)
email_schema = EmailSchema()


class EmailResource(Resource):

    def get(self):
        emails = Email.query.all()
        emails = emails_schema.dump(emails).data
        return {'status': 'success', 'data': emails}, 200

    def post(self):
        json_data = request.get_json(force=True)
        if not json_data:
            raise AppError.no_input_data_provided()
        data, errors = email_schema.load(json_data)
        if errors:
            return errors, 422
        email = Email.query.filter_by(email=data['email']).first()
        if email:
            raise AppError.email_already_exist()
        email = Email(
            email=json_data['email'],
            contact_id=json_data['contact_id']
        )
        email.save()

        result = email_schema.dump(email).data
        return {"status": 'success', 'data': result}, 201


class EmailItemResource(Resource):

    def get(self, email_id):
        email = Email.query.filter_by(id=email_id).first()
        if not email:
            raise AppError.email_not_found()
        result = email_schema.dump(email).data
        return {'status': 'success', 'data': result}, 200

    def put(self, email_id):
        json_data = request.get_json(force=True)
        if not json_data:
            raise AppError.no_input_data_provided()
        data, errors = email_schema.load(json_data)
        if errors:
            return errors, 422
        email = Email.query.filter_by(id=email_id).first()
        if not email:
            raise AppError.email_not_found()
        email.email = data['email']
        email.update()

        result = email_schema.dump(email).data
        return {"status": 'success', 'data': result}, 204

    def delete(self, email_id):
        json_data = request.get_json(force=True)
        if not json_data:
            raise AppError.no_input_data_provided()
        data, errors = email_schema.load(json_data)
        if errors:
            return errors, 422
        email = Email.query.filter_by(id=email_id).delete()
        email.delete()

        result = email_schema.dump(email).data
        return {"status": 'success', 'data': result}, 204

