#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint
from flask import render_template, url_for, request, session, redirect

from socialoauth import socialsites
from socialoauth.utils import import_oauth_class
from socialoauth.exception import SocialAPIError

app_name  = __name__.split('.')[0]
blueprint = Blueprint('index', __name__)

socialsites.config({
    'facebook': ('{0}.providers.facebook.Facebook'.format(app_name), 1, 'Facebook', {
        'redirect_uri': 'http://localhost:5000/login/oauth/facebook',
        'client_id': '140162746163142',
        'client_secret': '1a97620871b77481c124bd01e53e9649',
        'scope': ['email']
    })
})

@blueprint.route('/')
def index():
    user = session.get('user')
    return render_template('index.html', user=user)

@blueprint.route('/login')
def login():
    connections = dict()
    for socialsite in socialsites.list_sites():
        provider = import_oauth_class(socialsite)()
        connections[provider.site_name] = provider
    
    return render_template('login.html', connections=connections)

@blueprint.route('/login/oauth/<provider>')
def login_oauth(provider):
    code = request.args.get('code')
    if not code:
        redirect(url_for('index.index'))
   
    socialsite = import_oauth_class(socialsites[provider])()
    
    try:
        socialsite.get_access_token(code)
    except SocialAPIError as e:
         print e.site_name
         print e.url
         print e.error_msg
         raise

    session['user'] = socialsite
         
    return redirect(url_for('index.index'))
