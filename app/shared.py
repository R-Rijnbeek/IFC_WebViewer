# =============== DEFINE BLUEPRINTS ==============

from flask import Flask
from .utils.logger import ApplicationLogger
from .utils.bulk import Bulk

# =============== DEFINE SHARED OBJECTS ==============

APP = Flask(__name__)
BULK = Bulk()
LOG = ApplicationLogger("main_logger")