import os

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'AF5lqPhOnECpAgQjTmuHWY2gFvqIiw2s'
   
class DevConfig(Config):
    ENV="development"
    DEVELOPMENT=True
    DEBUG=True