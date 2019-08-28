import json, os

from myapp.extentions import db
from myapp.app import create_app
from myapp.settings import Config
from unittest import TestCase


class TestContacts(TestCase):
    def setUp(self):
        self.app = create_app(Config)
        db.create_all(app=self.app)
        self.client = self.app.test_client()
        db.create_all(app=self.app)

    def tearDown(self):
        db.session.remove()
        db.drop_all(app=self.app)

    def test_contact_successed(self):
        data = dict(username='mesuttest', first_name='Mesut', last_name='Aslan', enabled=True)
        response = self.client.post('/api/contacts', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 201)

        response = self.client.get('/api/contacts/1', content_type='application/json')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/api/contacts/Mesut', content_type='application/json')
        self.assertEqual(response.status_code, 200)

        data = dict(username='mesuttest2', first_name='Mesut2', last_name='Aslan2', enabled=True)
        response = self.client.put('/api/contacts/1', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 204)

    def test_contact_failed(self):
        data = dict(username='mesu', first_name='Mesut', last_name='Aslan', enabled=True)
        response = self.client.post('/api/contacts', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 422)

        response = self.client.get('/api/contacts/1', content_type='application/json')
        self.assertEqual(response.status_code, 404)

        response = self.client.get('/api/contacts/Mesut', content_type='application/json')
        self.assertEqual(response.status_code, 404)

        data = dict(username='mesuttest2', first_name='Mesut2', last_name='Aslan2', enabled=True)
        response = self.client.put('/api/contacts/1', content_type='application/json')
        self.assertEqual(response.status_code, 400)
