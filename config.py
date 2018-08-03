import os


class DevelopmentConfig(object):
    """ Development config """

    SECRET_KEY = os.urandom(24)
    DB_HOSTNAME = "db"
    DB_USERNAME = "root"
    DB_PASSWORD = "toor"
    DB_DATABASE = "todo"
    DB_PROTOCOL = "postgres"


class ProductionConfig(object):
    """ Production config (inexistent) """
    pass


ENVIRONMENT = os.getenv("ENVIRONMENT")

ENVIRONMENTS = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

CURRENT_CONFIG = ENVIRONMENTS.get(ENVIRONMENT or 'default')
