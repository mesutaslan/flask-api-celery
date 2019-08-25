from flask import Flask
from celery import Celery
from myapp.settings import DevConfig


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
celery = make_celery(app)


@celery.task()
def create_contact_with_random_data():
    print('create_contact_with_random_data')


@celery.task()
def remove_older_one_mn_contacts():
    print('remove_older_one_mn_contacts')