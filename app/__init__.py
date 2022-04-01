#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__init__.py: This module define the the webservice function build with Flask
"""
# =============== IMPORTS ==============

from .utils import DeleteJSONFilesFromDirectory, CreateDirectoryIfItNotExist
from .shared import APP, LOG

# =============== PROCESS ===============

def create_app():
    """
    INFORMATION: Fuction that activate the webservice with the selected configuration values of url, Port and debug mode and SQL configuration defined in "dev_config.cfg"

    INPUT: None

    OUTPUT:BOOLEAN
    """
    try:
        # CONFIGURE THE FLASK OBJECT with the 'dev_config.cfg' configuration file
        APP.config.from_pyfile("dev_config.cfg")
        # INITIALIZE LOGGER INSTANCE
        LOG.init_app(APP)

        from .public import public_bp, js, upload
        APP.register_blueprint(public_bp)
        APP.register_blueprint(js)
        APP.register_blueprint(upload)

        shape_path = APP.config["SHAPE_DIR"]
        upload_path = APP.config["UPLOAD_FOLDER"]
        CreateDirectoryIfItNotExist(shape_path)
        CreateDirectoryIfItNotExist(upload_path)
        DeleteJSONFilesFromDirectory(shape_path)

        host = APP.config["HOST"]
        port = APP.config["PORT"]

        APP.run(host=host,port = port)

        return True
    except Exception as exc:
        print(f"ERROR: unexpected error activting the webservice process: {exc}")
        return False

# =============== EXECUTE TEST CODE ===============

if __name__ == "__main__":
    pass