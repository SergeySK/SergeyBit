__author__ = 'SergeyKozlov'

import os
import json
from settings import AppSettings

class User:
    """
    Class that represents user and works with user's credentials to provide authenticated access to user's resources
    """

    def __init__(self, id, password):
        self.id = id
        # TODO: store hash here, not the password itself
        self.hash_password = password
        self.token = None

    def set_token(self, token):
        self.token = token


class UserMgr:
    """
    User management
    """

    def __init__(self, app_settings):
        self.db_file = app_settings['user_db_file']
        if not os.path.exists(self.db_file):
            fl = open(self.db_file, 'w')
            fl.close()

    def add_user(self, user):
        fl = open(self.db_file, 'a')
        fl.write(user.id + ':' + user.hash_password + '\n')
        fl.close()

    def delete_user(self, user):
        # No-op for now
        return False

    def check_user(self, user):
        for line in open(self.db_file, 'r'):
            if line.strip().split(':')[0] == user.id:
                return True
        else:
            return False

    def check_password(self, user):
        for line in open(self.db_file, 'r'):
            if line.strip().split(':')[0] == user.id and line.strip().split(':')[1] == user.hash_password:
                return True
        else:
            return False

    def get_token(self, user):
        token = None
        fl_name = user.id + '.tkn'
        if os.path.exists(fl_name):
            fl = open(fl_name, 'r')
            token_str = fl.read()
            fl.close()
            token = json.loads(token_str)
            user.set_token(token)
            print(token)
        return token

    def renew_token(self, user, token):
        fl_name = user.id + '.tkn'

        if os.path.exists(fl_name):
            os.remove(fl_name)

        fl = open(fl_name, 'w')
        fl.write(json.dumps(token))
        user.set_token(token)
        fl.close()
