#!/usr/bin/env python
# -*- coding: utf-8 -*-

from socialoauth.sites.base import OAuth2

class Facebook(OAuth2):
    GRAPH_URL        = 'https://graph.facebook.com'
    AUTHORIZE_URL    = 'https://www.facebook.com/dialog/oauth'
    ACCESS_TOKEN_URL = '{0}/oauth/access_token'.format(GRAPH_URL)

    SMALL_IMAGE = '{0}/{1}/picture'
    LARGE_IMAGE = '{0}/{1}/picture?type=large'
    
    def build_api_url(self, url):
        return url

    def build_api_data(self, **kwargs):
        data = {
            'access_token': self.access_token
        }
        data.update(kwargs)
        return data

    def parse_token_response(self, res):
        res = res.split('&')
        res = [_r.split('=') for _r in res]
        res = dict(res)
        
        self.access_token = res['access_token']
        self.expires_in = int(res['expires'])
        self.refresh_token = None

        res = self.http_get('https://graph.facebook.com/me', {
            'access_token': self.access_token
        })

        self.uid = res['id']
        self.name = res['username']
        self.avatar = self.SMALL_IMAGE.format(self.GRAPH_URL, res['username'])
        self.avatar_large = self.LARGE_IMAGE.format(self.GRAPH_URL, res['username'])

    def get_access_token(self, code):
        super(Facebook, self).get_access_token(code, method='GET', parse=False)
