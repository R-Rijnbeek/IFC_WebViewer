# =============== DEFINE BLUEPRINTS ==============

from flask import Flask
from .logger import ApplicationLogger

# =============== DEFINE SHARED OBJECTS ==============

APP = Flask(__name__)
LOG = ApplicationLogger("main_logger")