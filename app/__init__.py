#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__init__.py: This module define the the webservice function build with Flask
"""
# =============== IMPORTS ==============

from flask import Flask

from .utils import DeleteJSONFilesFromDirectory, CreateDirectoryIfItNotExist

# =============== PROCESS ===============

def create_app():
    """
    INFORMATION: Fuction that activate the webservice with the selected configuration values of url, Port and debug mode and SQL configuration defined in "dev_config.cfg"

    INPUT: None

    OUTPUT:BOOLEAN
    """
    try:
        # DEFINING OF THE FLASK OBJECT
        app = Flask(__name__)
        # CONFIGURE THE FLASK OBJECT with the 'dev_config.cfg' configuration file
        app.config.from_pyfile("dev_config.cfg")

        from .public import public_bp, js, upload
        app.register_blueprint(public_bp)
        app.register_blueprint(js)
        app.register_blueprint(upload)

        shape_path = app.config["SHAPE_DIR"]
        upload_path = app.config["UPLOAD_FOLDER"]
        CreateDirectoryIfItNotExist(shape_path)
        CreateDirectoryIfItNotExist(upload_path)
        DeleteJSONFilesFromDirectory(shape_path)

        host = app.config["HOST"]
        port = app.config["PORT"]

        app.run(host=host,port = port)

        return True
    except Exception as exc:
        print(f"ERROR: unexpected error activting the webservice process: {exc}")
        return False

# =============== EXECUTE TEST CODE ===============

if __name__ == "__main__":
    pass