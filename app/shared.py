# =============== DEFINE BLUEPRINTS ==============

from flask import Flask
from .logger import ApplicationLogger
from .bulk import Bulk

# =============== DEFINE SHARED OBJECTS ==============

APP = Flask(__name__)
BULK = Bulk()
LOG = ApplicationLogger("main_logger")