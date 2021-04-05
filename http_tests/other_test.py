import requests
import pytest
from src import config
import src.auth
import src.user
import src.other
import src.data
from src.error import InputError, AccessError

@pytest.fixture
def clear_data():
    requests.delete(config.url + 'clear/v1')

#search test
def test_search_v2(clear_data):
    user = requests.post(config.url + 'auth/register/v2', json = {
        'email': 'skadi@gmail.com',
        'password': '1234aaaaaa',
        'name_first': 'Tom',
        'name_last': 'Diaaa',
    })
    #join server
    user_pl = user.json()

    channel_info = requests.post(config.url + 'channels/create/v2', json = {
        'token': user_pl['token'],
        'name': 'Channel1',
        'is_public': True,
    })
    channel_info = channel_info.json()

    #send message
    requests.post(config.url + 'message/send/v2', json = {
        'token': user_pl['token'],
        'channel_id': channel_info['channel_id'],
        'message': 'Hello',
    })

    assert requests.get(config.url + 'search/v1', json = {
        'token': user_pl['token'],
        'query_str':'Hello',
    }).status_code == 400

def test_search_v2_input_error(clear_data):
    user = requests.post(config.url + 'auth/register/v2', json = {
        'email': 'skadi@gmail.com',
        'password': '1234aaaaaa',
        'name_first': 'Sing',
        'name_last': 'Diaaa',
    })
    user_pl = user.json()

    channel_info = requests.post(config.url + 'channels/create/v2', json = {
        'token': user_pl['token'],
        'name': 'Channel1',
        'is_public': True,
    })
    channel_info = channel_info.json()

    requests.post(config.url + 'message/send/v2', json = {
        'token': user_pl['token'],
        'channel_id': channel_info['channel_id'],
        'message': 'Hello',
    })

    assert requests.get(config.url + 'search/v1', json = {
        'token': user_pl['token'],
        'query_str':'Hello' * 1000,
    }).status_code == InputError.code

def test_search_v2_input_token(clear_data):
    assert requests.get(config.url + 'search/v1', json = {
        'token': 6,
        'query_str':'Hello',
    }).status_code == AccessError.code


#notification test
def test_notifications_get(clear_data):
    user1 = requests.post(config.url + 'auth/register/v2', json = {
        'email': 'ska@gmail.com',
        'password': '1234aaaaaa',
        'name_first': 'Tom',
        'name_last': 'Diaaa',
    })
    payload = user1.json()
    requests.get(config.url + 'search/v1', json = {
        'token': payload['token'],
    })