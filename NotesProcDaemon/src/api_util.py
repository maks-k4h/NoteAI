import os
from typing import Any

import requests
from requests import codes, request

from . import schemas

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
        reauthenticate: bool = True
):
    """
    Wrapper for pyrequests' requests. Updates access token if needed.
    """
    method = method.lower()
    url = f'{API_URL}{path}'

    response = request(method, url, params=params, data=data, headers=_headers())

    if response.status_code == codes.unauthorized:
        if reauthenticate:
            _authorize()
            return _request(method, path, params=params, data=data, reauthenticate=False)
        else:
            raise Exception('Unauthorized')

    return response


def get_note_by_uuid(uuid: str):
    response = _request(
        'get',
        f'/notes/{uuid}'
    )
    if response.status_code != codes.ok:
        raise Exception('Cannot retrieve note by uuid.', response)
    data = response.json()
    return schemas.Note(
        uuid=uuid,
        title=data['title'],
        content=data['content'],
    )

