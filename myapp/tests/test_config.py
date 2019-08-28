import json, os

from myapp.extentions import db
from myapp.app import create_app
from myapp.settings import TestConfig, DevConfig, ProdConfig, Config
from unittest import TestCase


class TestConfigs(TestCase):
    def setUp(self):
        self.app_config = create_app(Config)
        self.app_test = create_app(TestConfig)
        self.app_dev = create_app(DevConfig)
        self.app_prod = create_app(ProdConfig)
        self.client = self.app_test.test_client()
        db.create_all(app=self.app_test)

    def tearDown(self):
        db.session.remove()
        db.drop_all(app=self.app_test)

    def test_config(self):
        self.assertEqual(self.app_config.config['SQLALCHEMY_ECHO'], False)
        self.assertEqual(self.app_config.config['APP_DIR'], os.path.join(os.path.abspath(os.curdir), 'myapp'))
        self.assertEqual(self.app_config.config['PROJECT_ROOT'], os.path.abspath(os.path.join(self.app_test.config['APP_DIR'], os.pardir)))
        self.assertEqual(self.app_config.config['DEBUG_TB_INTERCEPT_REDIRECTS'], False)
        self.assertEqual(self.app_config.config['CACHE_TYPE'], 'simple')
        self.assertEqual(self.app_config.config['SQLALCHEMY_TRACK_MODIFICATIONS'], False)
        self.assertEqual(self.app_config.config['CONTACT_ENDPOINT_URL'], 'http://127.0.0.1:5000/api/contacts')
        self.assertEqual(self.app_config.config['CELERY_BROKER_URL'], 'redis://localhost:6379/0')
        self.assertEqual(self.app_config.config['CELERY_RESULT_BACKEND'], 'redis://localhost:6379/0')


    def test_config_dev(self):
        self.assertEqual(self.app_dev.config['BCRYPT_LOG_ROUNDS'], 13)
        self.assertEqual(self.app_dev.config['ENV'], 'dev')
        self.assertEqual(self.app_dev.config['DB_NAME'], 'dev.db')
        self.assertEqual(self.app_dev.config['DB_PATH'], os.path.join(os.path.abspath(os.path.join(self.app_test.config['APP_DIR'], os.pardir)), 'dev.db'))
        self.assertEqual(self.app_dev.config['SQLALCHEMY_DATABASE_URI'], 'sqlite:///{0}'.format(os.path.join(os.path.abspath(os.path.join(self.app_test.config['APP_DIR'], os.pardir)), 'dev.db')))

    def test_config_test(self):
        self.assertEqual(self.app_test.config['BCRYPT_LOG_ROUNDS'], 4)
        self.assertEqual(self.app_test.config['TESTING'], True)
        self.assertEqual(self.app_test.config['DEBUG'], True)
        self.assertEqual(self.app_test.config['ENV'], 'test')
        self.assertEqual(self.app_test.config['DB_NAME'], 'test.db')
        self.assertEqual(self.app_test.config['DB_PATH'], os.path.join(os.path.abspath(os.path.join(self.app_test.config['APP_DIR'], os.pardir)), 'test.db'))
        self.assertEqual(self.app_test.config['SQLALCHEMY_DATABASE_URI'], 'sqlite:///{0}'.format(os.path.join(os.path.abspath(os.path.join(self.app_test.config['APP_DIR'], os.pardir)), 'test.db')))
