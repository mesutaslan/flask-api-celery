import datetime
import json
import random
import re
import string

import httplib2
from celery import Celery
from flask import Flask

from myapp.contacts.models import Contact
from myapp.contacts.serializers import ContactSchema
from myapp.extentions import db
from myapp.settings import DevConfig

contacts_schema = ContactSchema(many=True)
contact_schema = ContactSchema()


def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


app = Flask(__name__)
app.config.from_object(DevConfig)
db.init_app(app)
http = httplib2.Http()
celery = make_celery(app)


@celery.task()
def create_contact_with_random_data():
    contact_data = {
        "username": random_string(),
        "first_name": str_camel_case(random_string(15)),
        "last_name": str_camel_case(random_string(15)),
    }
    print("Posting %s" % contact_data)
    response, content = http.request(
        app.config.get('CONTACT_ENDPOINT_URL'),
        'POST',
        json.dumps(contact_data),
        headers={'Content-Type': "application/json"}
    )
    if response.status == 201:
        print('Contact created with random data: %s' % content)


@celery.task()
def remove_older_one_mn_contacts():
    current_time = datetime.datetime.utcnow()
    one_minute_ago = current_time - datetime.timedelta(seconds=1)
    contacts = Contact.query.filter(Contact.created_at < one_minute_ago)
    contacts = contacts_schema.dump(contacts).data
    url = app.config.get('CONTACT_ENDPOINT_URL') + str('/')
    for contact in contacts:
        response, content = http.request(
            url + str(contact['id']),
            'DELETE',
            None,
            headers={'Content-Type': "application/json"}
        )
        if response.status == 200:
            print('Contact deleted: %s' % contact['id'])


def random_string(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))


def str_camel_case(string_value):
    return re.sub(r'\w+', lambda m: m.group(0).capitalize(), string_value)
