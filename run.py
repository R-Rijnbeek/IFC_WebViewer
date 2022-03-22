#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, jsonify
from ifcopenshell import version as IFC_VERSION
from OCC import VERSION as OCC_VERSION
import os

app = Flask(__name__)
 
@app.route('/', methods=['GET'])
def hello_world():
    return jsonify({'message': str(OCC_VERSION)})

@app.route('/test', methods=['GET'])
def test():
    return jsonify({'test': str(IFC_VERSION)})

if __name__ == "__main__":
    port = os.environ.get("PORT",5000)
    app.run(debug=False, host="0.0.0.0", port=port)
