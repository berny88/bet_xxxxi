# -*- coding: utf-8 -*-
from flask import Blueprint, jsonify, redirect, request, session,render_template
import logging
from uuid import uuid4

from flask import send_file
import hashlib

import io

logger = logging.getLogger(__name__)

u"""
**************************************************
ui layer
"""

front_end = Blueprint('front', __name__,
                       template_folder='dist', 
                       static_folder='dist',
                       static_url_path='dist')

@front_end.route("/")
def index():
    print("front root")
    return render_template('index.html')