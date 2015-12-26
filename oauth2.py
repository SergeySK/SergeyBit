__author__ = 'SergeyKozlov'

from settings import AppSettings
import requests
import base64

class OAuth2:
    """ Class that is responsible for OAuth2 authentication """

    def __init__(self, app_settings):
        self.app_settings = app_settings
        self.app_auth_data = dict()

    def __make_magic_str(self):
        """ Magic string which is required by FitBit API """
        magic_str = base64.b64encode(bytearray(self.app_settings['client_id'] + ':' + self.app_settings['client_secret'], 'utf-8'))
        return str(magic_str.decode())

    def request_token(self, auth_code):

        magic_str = self.__make_magic_str()

        headers = {'Authorization': 'Basic ' + magic_str,
                   'Content-Type': 'application/x-www-form-urlencoded'}

        data = {'client_id': self.app_settings['client_id'],
                'grant_type': 'authorization_code',
                'redirect_uri': self.app_settings['callback_uri'],
                'code': auth_code}

        print('Token request URI: ' + self.app_settings['auth2_tokenreq_uri'])

        req = requests.post(self.app_settings['auth2_tokenreq_uri'], data=data, headers=headers)

        if req.status_code != requests.codes.ok:
            print('Token request failed with error code ' + str(req.status_code))
            return None

        self.app_auth_data = req.json()
        return self.app_auth_data

    def get_auth_data(self):
        return self.app_auth_data