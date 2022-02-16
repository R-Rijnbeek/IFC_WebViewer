#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
entrypoint.py: This script execute the OpenWebservice() function that activate the flask webservice
"""
__author__          = "Robert Rijnbeek"
__version__         = "1.0.1"
__maintainer__      = "Robert Rijnbeek"
__email__           = "r.rijnbeek@dinsa.es"
__status__          = "Development"

__creation_date__   = '31/3/2019'
__last_update__     = '31/3/2019'

# =============== IMPORTS ==============

from app import create_app

# ==== ACTIVATION OF THE WEBSERVICE ====

create_app()
