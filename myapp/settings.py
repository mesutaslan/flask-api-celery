# -*- coding: utf-8 -*-
"""Application configuration."""
import os
from datetime import timedelta

class Config(object):
    """Base configuration."""
    basedir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///devdata.db"
    CELERY_BROKER_URL = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND = "redis://localhost:6379/0"
    CELERYBEAT_SCHEDULE = {
        'run-every-15-second': {
            'task': 'tasks.cronjobs.create_contact_with_random_data',
            'schedule': timedelta(seconds=15)
        },
        'run-every-1-minute': {
            'task': 'tasks.cronjobs.remove_older_one_mn_contacts',
            'schedule': timedelta(seconds=60)
        }
    }

class ProdConfig(Config):
    """Production configuration."""

    ENV = 'prod'
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///proddata.db'


class DevConfig(Config):
    """Development configuration."""

    ENV = 'dev'
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///devdata.db'
    CACHE_TYPE = 'simple'

class TestConfig(Config):
    """Test configuration."""

    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///testdata.db'
    BCRYPT_LOG_ROUNDS = 4