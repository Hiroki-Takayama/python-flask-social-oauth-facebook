#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask
from .routes import index

def create_app():
    app = Flask(__name__, static_folder='statics', template_folder='templates')
    app.config['DEBUG'] = True
    app.config['SECRET_KEY'] = 'Some Secret Key'
    
    app.register_blueprint(index.blueprint, url_prefix='')
    
    return app
