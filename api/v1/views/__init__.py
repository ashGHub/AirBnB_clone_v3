#!/usr/bin/python3
"""
Module that initializes api/v1 route blueprint. Mainly initializes
each route blueprint for each model
"""
from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
from api.v1.views.index import *
from api.v1.views.states import *
