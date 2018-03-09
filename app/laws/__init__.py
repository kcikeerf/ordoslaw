# -*- coding: utf-8 -*-
from flask import Blueprint

laws = Blueprint('laws', __name__)

from . import views

