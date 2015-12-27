__author__ = 'SergeyKozlov'

import requests

def get_api_path(api_url, api_version):
    return api_url + '/' + api_version


def get_date_period(start_date=None, end_date=None, period=None):
    date = ''
    if start_date:
        date += '/date/' + start_date
    if end_date:
        date += '/' + end_date
    else:
        if period:
            date += '/' + period
    print(date)
    return date


def get_resource_path(data_type, resource=None, group=None):
    res = dt = grp = ''

    if resource:
        res = '/' + resource
    if data_type:
        dt = '/' + data_type
    if group:
        grp = '/' + group

    return grp + dt + res

def get_api_call(api_path, user_id, res_path, date_period):
    return api_path + '/' + 'user/' + user_id + res_path + date_period + '.json'

class ApiRequest:
    """ FitBit REST API """

    def __init__(self, settings, auth_data):
        self.settings = settings
        self.auth_data = auth_data

    # URI/user/user-id/<group>/<data_type>/<resource>/<date>/<req_date>/<>.json
    # URI: API url + API version: https://api.fitbit.com/1/
    # user_id: user_id from auth_data or current user '-'
    # start_date, end_date: yyyy-MM-dd or today
    # data_type: weight, heart, sleep
    # period: 1d, 7d, 30d, 1w, 1m, 3m, 6m, 1y, or max.
    # resource: startTime, timeInBed, minutesAsleep, awakeningsCount, etc
    # group: /body/log/, /activities/
    # Examples:
    # /group/data_type/ ==> /body/log/weight, /activities/heart
    # /data_type/resource ==> /sleep/timeInBed
    def prepare_request(self, user_id='-', data_type=None, start_date=None, end_date=None, period=None, resource=None, group=None):
        date_period = get_date_period(start_date, end_date, period)
        api_path = get_api_path(self.settings['api_url'], self.settings['api_version'])
        res_path = get_resource_path(data_type, resource, group)
        api_call = get_api_call(api_path, user_id, res_path, date_period)
        print('API CALL: ' + api_call)
        return api_call

    def send_request(self, request, request_method):
        print('CALLING API: ' + request_method + ': ' + request)
        req = None

        if request_method not in ['GET', 'get', 'POST', 'post', 'DELETE', 'delete', 'PUT', 'put']:
            print('Wrong request method: ' + request_method)
            return None

        headers = {'Authorization': 'Bearer ' + self.auth_data['access_token']}

        if request_method in ['GET', 'get']:
            print('Executing GET request for ' + request)
            req = requests.get(request, headers=headers)
            if req.status_code != requests.codes.ok:
                print('Request failed with error code ' + str(req.status_code))
                raise ValueError(req.status_code)
                return None
            else:
                return req.json()
        else:
            if request_method in ['POST', 'post']:
                print('POST not supported at this time')
                return None
            else:
                if request_method in ['DELETE', 'delete']:
                    print('DELETE not supported at this time')
                    return None
                else:
                    if request_method in ['PUT', 'put']:
                        print('PUT not supported at this time')
                        return None