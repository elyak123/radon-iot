import json
from pprint import pprint
import requests
from django.conf import settings


class RadonCookieRequests(object):
    radon_username = settings.TEST_USERNAME
    radon_password = settings.TEST_PASSWORD
    radon_base_url = settings.TEST_URL

    def __init__(self, *args, **kwargs):
        super(RadonCookieRequests, self).__init__(*args, **kwargs)
        self.session = requests.Session()

    def login(self, username=None, password=None):
        if not username:
            username = self.radon_username
        if not password:
            password = self.radon_password
        data = {
          "username": username,
          "password": password
        }
        req = self.session.post(
            '{}auth/login/'.format(self.radon_base_url),
            headers={'content-type': 'application/json'},
            json=data
        )
        response = req.json()
        if bool([x for x in response.keys() if 'error' in x]):
            return response
        self.refresh_token = response['refresh_token']['token']
        self.refresh_exp = response['refresh_token']['exp']
        return response

    def change_user(self, username, password):
        self.session.cookies.clear()
        try:
            resp = self.login(username=username, password=password)
        except KeyError:
            return resp
        return resp

    def refresh(self):
        response = self.session.post(
            '{}auth/refresh/'.format(self.radon_base_url),
            json={'refresh': self.refresh_token}
        )
        token = response.json()['access']['token']
        if response.status_code == 200:
            self.session.cookies.update({settings.JWT_AUTH_COOKIE: token})
        else:
            self.login()

    def prepare_request(self, url_specific, specific_headers={}):
        URL = self.radon_base_url + url_specific
        main_headers = {'content-type': 'application/json'}
        headers = {**main_headers, **specific_headers}
        return URL, headers

    def send(self, method, url_specific, payload={}, specific_headers={}, pretty=False, params=None):
        URL, headers = self.prepare_request(url_specific, specific_headers)
        handler = getattr(self.session, method.lower())
        kwargs = {'headers': headers}
        if method in ['post', 'put', 'patch']:
            kwargs['json'] = payload
        if method == 'get' and params:
            kwargs['params'] = params
        response = handler(URL, **kwargs)
        if response.status_code == 401:
            if hasattr(self, 'refresh_token'):
                self.refresh()
            else:
                self.login()
            response = handler(URL, **kwargs)
        try:
            if pretty:
                return pprint(response.json())
            else:
                return response.json()
        except json.decoder.JSONDecodeError:
            return response.status_code

    def post(self, url_specific, payload, specific_headers={}):
        return self.send('post', url_specific, payload, specific_headers)

    def get(self, url, params=None, specific_headers={}, pretty=False):
        return self.send('get', url, specific_headers, pretty=pretty, params=params)


client = RadonCookieRequests()
