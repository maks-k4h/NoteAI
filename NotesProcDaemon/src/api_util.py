import os
from typing import Any

import requests
from requests import codes

API_URL = os.environ['API_URL']
API_LOGIN = os.environ['API_LOGIN']
API_PASSWORD = os.environ['API_PASSWORD']

CURRENT_TOKEN = 'empty'


def _headers():
    return {
        'Authorization': f'Bearer {CURRENT_TOKEN}'
    }


def _authorize():
    """
    Update access token.
    """
    response = requests.post(
        f'{API_URL}/account/token',
        data={
            'username': API_LOGIN,
            'password': API_PASSWORD,
        }
    )

    if response.status_code == codes.ok:
        global CURRENT_TOKEN
        CURRENT_TOKEN = response.json()['access_token']
        print('Token updated.')
    else:
        raise Exception('Cannot authenticate in API.')


def _request(
        method: str,
        path: str | bytes,
        params: Any = None,
        *args,
        data: Any = None,
        headers: Any = None,
        reauthenticate: bool = True
):
    """
    Wrapper for pyrequests' requests. Updates access token if needed.
    """
    method = method.lower()
    url = f'{API_URL}{path}'

    if method == 'get':
        response = requests.get(url, params=params, data=data, headers=headers)
    elif method == 'post':
        response = requests.post(url, params=params, data=data, headers=headers)
    elif method == 'put':
        response = requests.put(url, params=params, data=data, headers=headers)
    elif method == 'delete':
        response = requests.delete(url, params=params, data=data, headers=headers)
    else:
        raise Exception('Unknown method.')

    if response.status_code == codes.unauthorized:
        if reauthenticate:
            _authorize()
            _request(method, url, params=params, data=data, headers=headers, reauthenticate=False)
        else:
            raise Exception('Unauthorized', response.json())

    return response


def get_note_by_uuid(uuid: str):
    response = _request(
        'get',
        f'/notes/{uuid}',
        headers=_headers()
    )
    return response.json()

