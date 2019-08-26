from flask import request
from flask_restful import Resource
from myapp.contacts.models import Contact
from myapp.contacts.serializers import ContactSchema
from myapp.extentions import db
from myapp.exceptions import AppError

contacts_schema = ContactSchema(many=True)
contact_schema = ContactSchema()


class ContactResource(Resource):

    def get(self):
        cont = Contact.query.all()
        contact = contacts_schema.dump(cont).data
        return {'status': 'success', 'data': contact}, 200

    def post(self):
        json_data = request.get_json(force=True)
        if not json_data:
            raise AppError.no_input_data_provided()
        data, errors = contact_schema.load(json_data)
        if errors:
            return errors, 422
        contact = Contact.query.filter_by(username=data['username']).first()
        if contact:
            raise AppError.contact_already_exist()
        contact = Contact(
            username=json_data['username'],
            first_name=json_data['first_name'],
            last_name=json_data['last_name']
        )
        contact.save()

        result = contact_schema.dump(contact).data
        return {"status": 'success', 'data': result}, 201


class ContactItemResource(Resource):

    def get(self, contact_id):
        contact = Contact.query.filter_by(id=contact_id).first()
        if not contact:
            raise AppError.contact_not_found()
        contact = contact_schema.dump(contact).data
        return {'status': 'success', 'data': contact}, 200

    def put(self, contact_id):
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input data provided'}, 400
        data, errors = contact_schema.load(json_data)
        if errors:
            return errors, 422
        contact = Contact.query.filter_by(id=contact_id).first()
        if not contact:
            raise AppError.contact_not_found()
        contact.username = data['username']
        contact.first_name = data['first_name']
        contact.last_name = data['last_name']
        contact.update()

        result = contact_schema.dump(contact).data
        return {"status": 'success', 'data': result}, 204

    def delete(self, contact_id):
        contact = Contact.query.filter_by(id=contact_id).first()
        if not contact:
            raise AppError.contact_not_found()
        contact.delete()
        return {"status": 'success', 'data': contact.id}, 200


class ContactByUsernameResource(Resource):

    def get(self, username):
        search = "%{}%".format(username)
        contact = Contact.query.filter(Contact.username.like(search)).all()
        if not contact:
            raise AppError.contact_not_found()
        result = contacts_schema.dump(contact).data
        return {'status': 'success', 'data': result}, 200
