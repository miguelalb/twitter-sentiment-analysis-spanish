from flask import Blueprint

bp = Blueprint('auth', __name__)

from tweetsent.auth import routes