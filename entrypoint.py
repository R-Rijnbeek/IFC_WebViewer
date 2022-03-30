#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
entrypoint.py: This script execute the create_app() function that activate the flask webservice
"""
__author__          = "Robert Rijnbeek"
__version__         = "1.0.1"
__maintainer__      = "Robert Rijnbeek"
__email__           = "robert270384@gmail.com"
__status__          = "Development"

__creation_date__   = '16/02/2022'
__last_update__     = '28/03/2022'

# =============== IMPORTS ==============

from app import create_app

# ==== ACTIVATION OF THE WEBSERVICE ====

create_app()
