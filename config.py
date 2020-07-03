import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))
baseDB = os.path.join(basedir, 'app.db')
finalDB = os.environ.get('TWEETSENT_DATABASE_URL')

class Config(object):
    SECRET_KEY = os.environ.get('TWEETSENT_SECRET_KEY') or 'Nevermind_brother'
    SQLALCHEMY_DATABASE_URI = finalDB or 'sqlite:///' + baseDB
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['miguelacevedowah@gmail.com']
    