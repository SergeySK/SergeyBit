__author__ = 'SergeyKozlov'

import os
from settings import AppSettings
from oauth2 import OAuth2
from api_request import ApiRequest
from user_mgmt import UserMgr, User

# This is a hack, we're developing console application which can't handle callback URI invocation
def read_auth_code(client_id, cb_uri, auth_uri):
    print('Please open this URL in your browser, authorize application and enter code parameter from response')
    print('Example of response in browser address line: '
          'https://localhost/?code=805fed2a6f8fc6d20893f8ab75b01f955daab76e')
    print('We need everything that goes after code=')
    print(str(auth_uri) + '?'
          'response_type=code&'
          'client_id=' + str(client_id) + '&'
          'redirect_uri=' + str(cb_uri) + '&'
          'scope=activity%20nutrition%20heartrate%20location%20nutrition%20profile%20settings%20sleep%20social%20weight')

    return input('Code = ')


def get_auth_token(cur_app_settings, cur_user):
    auth_code = read_auth_code(cur_app_settings['client_id'], 'https://localhost/', 'https://www.fitbit.com/oauth2/authorize')
    oauth = OAuth2(app_settings)
    auth_data = oauth.request_token(auth_code)

    if auth_data:
        print('Tokens received')
        print(auth_data)
        user_mgr.renew_token(cur_user, auth_data)
        #TODO: store authentication data in persistent storage here
        return auth_data
    else:
        print('Token retrieval failure')
        return None

def testing(app_settings, user_mgr, user):
    api_req = ApiRequest(app_settings, user_mgr.get_token(user))
    # Testing:
    # GET https://api.fitbit.com/1/user/[user-id]/sleep/date/[date].json
    sleep_req = api_req.prepare_request(data_type='sleep', start_date='2015-11-11')
    print(sleep_req)
    sleep_data = api_req.send_request(sleep_req, 'GET')
    print(sleep_data)

    # GET https://api.fitbit.com/1/user/[user-id]/body/log/weight/[base-date]/[end-date].json
    weight_req = api_req.prepare_request(data_type='weight', start_date='2015-11-11', end_date='2015-11-12', group='body/log')
    print(weight_req)
    weight_data = api_req.send_request(weight_req, 'GET')
    print(weight_data)

    # GET https://api.fitbit.com/1/user/[user-id]/[resource-path]/date/[date]/[period].json
    sleep_adv_req = api_req.prepare_request(data_type='sleep', start_date='2015-11-11', period='1d', resource='timeInBed')
    print(sleep_adv_req)
    sleep_adv_data = api_req.send_request(sleep_adv_req, 'GET')
    print(sleep_adv_data)


app_settings = AppSettings(os.path.join(os.path.dirname(__file__), 'settings.xml')).read_settings()

# Get token for the user here:
print('Please enter your credentials. If you are a new user just enter User and Password and we\'ll create account')
user_name = input('User: ')
user_password = input('Password: ')

user = User(user_name, user_password)
user_mgr = UserMgr(app_settings)

if user_mgr.check_user(user):
    if user_mgr.check_password(user):
        auth_data = user_mgr.get_token(user)
        # If no token available
        if not auth_data:
            get_auth_token(app_settings, user)
    else:
        print('invalid credentials')
        exit(-1)
else:
    user_mgr.add_user(user)
    auth_data = get_auth_token(app_settings, user)
    if not auth_data:
        print('Token retrieval failure')
        exit(-1)

try:
    testing(app_settings, user_mgr, user)
except ValueError as err:
    if err.args[0] == 401:
        print('Your authorization is not valid, need to re-validate!!!')
        get_auth_token(app_settings, user)
        testing(app_settings, user_mgr, user)
    else:
        print('Unrecoverable error, terminating the app')
        exit(-1)