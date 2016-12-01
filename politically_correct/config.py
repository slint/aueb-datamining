import os


class EnvConfig(object):
    """Config that checks os.environ first.

    If you want to set some configuration variable in your production/local
    running instance of the application you can just add it to your
    environment by doing `export SECRET_VAR=secret123`.
    """
    DEBUG = False

    # DB config
    DATABASE_URL = ('sqlite:///politically_correct.db')

    # For PostgreSQL setup and try:
    # DATABASE_URL = ('postgresql+psycopg2://'
    #                 'aueb:aueb'
    #                 '@localhost/politically_correct')

    # Twitter config
    TWITTER_CONSUMER_KEY = 'CHANGE_ME'
    TWITTER_CONSUMER_SECRET = 'CHANGE_ME'
    TWITTER_ACCESS_TOKEN = 'CHANGE_ME'
    TWITTER_ACCESS_SECRET = 'CHANGE_ME'

    def __getattribute__(self, name):
        return os.environ.get(name, object.__getattribute__(self, name))


cfg = EnvConfig()
