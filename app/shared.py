from flask import Flask
from .logger import ApplicationLogger

APP = Flask(__name__)
LOG = ApplicationLogger("main_logger")