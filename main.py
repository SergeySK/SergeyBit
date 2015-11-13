import os
from settings import AppSettings


# This is a hack, we're developing console application which can't handle callback URI invocation
def read_token(client_id, cb_uri, auth_uri):
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

app_settings = AppSettings(os.path.join(os.path.dirname(__file__), 'settings.xml')).read_settings()
token = read_token(app_settings['client_id'], 'https://localhost/', 'https://www.fitbit.com/oauth2/authorize')