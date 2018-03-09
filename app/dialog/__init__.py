# -*- coding: utf-8 -*-
from flask import Blueprint

dialog = Blueprint('dialog', __name__)

from . import views
