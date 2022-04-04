# =============== DEFINE BLUEPRINTS ==============

from flask import Flask
from .bulk import Bulk
from .logger import ApplicationLogger

# =============== DEFINE SHARED OBJECTS ==============

APP = Flask(__name__)
BULK = Bulk()
LOG = ApplicationLogger("main_logger")