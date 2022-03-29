from flask import Blueprint

public_bp = Blueprint('public', __name__, template_folder = 'templates')

js = Blueprint('js', __name__, template_folder = 'templates')

upload = Blueprint('upload', __name__)

from . import routes