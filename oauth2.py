from settings import AppSettings
import requests
import base64

class OAuth2:
    """ Class that is responsible for OAuth2 authentication """

    def __init__(self, app_settings):
        self.app_settings = app_settings
        self.token = dict()
        self.token['access'] = ''
        self.token['refresh'] = ''
        self.token['expiration'] = 0
        self.scope = set([])
        self.user_id = ''
        self.bAvailable = False

    def __make_magic_str(self):
        magic_str = base64.b64encode(bytearray(self.app_settings['client_id'] + ':' + self.app_settings['client_secret'], 'utf-8'))
        return str(magic_str.decode())

    def request_token(self, auth_code):

        magic_str = self.__make_magic_str()
        print(magic_str)

        headers = {'Authorization': 'Basic ' + magic_str,
                   'Content-Type': 'application/x-www-form-urlencoded'}

        data = {'client_id': self.app_settings['client_id'],
                'grant_type': 'authorization_code',
                'redirect_uri': self.app_settings['callback_uri'],
                'code': auth_code}

        print(self.app_settings['auth2_tokenreq_uri'])

        req = requests.post(self.app_settings['auth2_tokenreq_uri'], data=data, headers=headers)
        print(req.status_code)
        print(req.json())

        self.bAvailable = True
        return self.bAvailable

    def get_tokens(self):
        if self.bAvailable:
            return self.token
        else:
            return None

    def get_user_id(self):
        if self.bAvailable:
            return self.user_id
        else:
            return None

    def get_scope(self):
        if self.bAvailable:
            return self.scope
        else:
            return None
