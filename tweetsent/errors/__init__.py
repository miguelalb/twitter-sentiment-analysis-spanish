from flask import Blueprint

bp = Blueprint('errors', __name__)

from tweetsent.errors import handlers