import json
import requests
from datetime import datetime
from django.conf import settings


class RadonCookieRequests(object):
    radon_username = settings.TEST_USERNAME
    radon_password = settings.TEST_PASSWORD
    radon_base_url = settings.TEST_URL

    def __init__(self, *args, **kwargs):
        super(RadonCookieRequests, self).__init__(*args, **kwargs)
        self.session = requests.Session()

    def login(self):
        data = {
          "username": self.radon_username,
          "password": self.radon_password
        }
        req = self.session.post(
            '{}auth/login/'.format(self.radon_base_url),
            headers={'content-type': 'application/json'},
            json=data
        )
        response = req.json()
        self.refresh_token = response['refresh_token']['refresh_token']
        self.refresh_exp = response['refresh_token']['exp']

    def refresh(self):
        response = self.session.post(
            '{}auth/refresh/'.format(self.radon_base_url),
            json={'refresh': self.refresh_token}
        )
        token = response.json()['access']
        if response.status_code == 200:
            self.session.cookies.update({settings.JWT_AUTH_COOKIE: token})
        else:
            self.login()

    def refresh_or_login(self):
        if hasattr(self, 'refresh_token'):
            if self.refresh_exp > round(datetime.utcnow().timestamp()):
                self.refresh()
        else:
            self.login()

    def prepare_request(self, url_specific, specific_headers={}):
        URL = self.radon_base_url + url_specific
        main_headers = {'content-type': 'application/json'}
        self.session.cookies.clear_expired_cookies()
        headers = {**main_headers, **specific_headers}
        if not self.session.cookies:
            self.refresh_or_login()
        return URL, headers

    def send(self, method, url_specific, payload={}, specific_headers={}):
        URL, headers = self.prepare_request(url_specific, specific_headers)
        handler = getattr(self.session, method.lower())
        if method in ['post', 'put', 'patch']:
            response = handler(URL, headers=headers, json=payload)
        else:
            response = handler(URL, headers=headers)
        try:
            return response.json()
        except json.decoder.JSONDecodeError:
            return response.status_code

    def post(self, url_specific, payload, specific_headers={}):
        return self.send('post', url_specific, payload, specific_headers)

    def get(self, url, specific_headers={}):
        return self.send('get', url, specific_headers)


client = RadonCookieRequests()
