'''
Implementation of http tests for other functions and routes
Written by Kanit Srihakorth and Tharushi Gunawardana
'''
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
    '''
    Clears data in data file
    '''
    requests.delete(config.url + 'clear/v1')


def test_search_v2(clear_data):
    '''
    Basic test for functionality of search function
    '''
    user = requests.post(config.url + 'auth/register/v2', json = {
        'email': 'skadi@gmail.com',
        'password': '1234aaaaaa',
        'name_first': 'Tom',
        'name_last': 'Diaaa',
    })
    user_pl = user.json()

    channel_info = requests.post(config.url + 'channels/create/v2', json = {
        'token': user_pl['token'],
        'name': 'Channel1',
        'is_public': True,
    })
    channel_info_pl = channel_info.json()

    requests.post(config.url + 'message/send/v2', json = {
        'token': user_pl['token'],
        'channel_id': channel_info_pl['channel_id'],
        'message': 'Hello',
    })
  
    assert requests.get(config.url + f"search/v2?token={user_pl['token']}&query_str=Hello").status_code == 200

def test_search_v2_input_error(clear_data):
    '''
    Test for invalid query_str in search function
    '''
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
    channel_info_pl = channel_info.json()

    requests.post(config.url + 'message/send/v2', json = {
        'token': user_pl['token'],
        'channel_id': channel_info_pl['channel_id'],
        'message': 'Hello',
    })

    assert requests.get(config.url + f"search/v2?token={user_pl['token']}&query_str={'Hello' * 1000}").status_code == InputError.code

def test_search_v2_input_token(clear_data):
    '''
    Test for invalid input token in search function
    '''
    assert requests.get(config.url + 'search/v2?token=6&query_str=Hello').status_code == InputError.code

def test_notifications_get_invalid_token(clear_data):
    '''
    Test for invalid input token in notification function
    '''
    assert requests.get(config.url + 'notifications/get/v1?token=6').status_code == InputError.code

def test_notifications_get_tag(clear_data):
    '''
    Test if user got tagged in channel
    '''
    user = requests.post(config.url + 'auth/register/v2', json = {
        'email': 'gordon@gmail.com',
        'password': '1234aaaaaa',
        'name_first': 'Gordon',
        'name_last': 'Liang',
    })
    user_pl = user.json()
    
    channel_info = requests.post(config.url + 'channels/create/v2', json = {
        'token': user_pl['token'],
        'name': 'Channel1',
        'is_public': True,
    })
    channel_info_pl = channel_info.json() 

    requests.post(config.url + 'message/send/v2', json = {
        'token': user_pl['token'],
        'channel_id': channel_info_pl['channel_id'],
        'message': 'Hello @gordonliang',
    })

    notification = requests.get(config.url + f"notifications/get/v1?token={user_pl['token']}")
    notification_pl = notification.json()

    assert notification_pl['notifications'][0]['notification_message'] == 'gordonliang tagged you in Channel1: Hello @gordonliang'

def test_notifications_get_add_to_channel(clear_data):
    '''
    Test if user got added in channel
    '''
    user = requests.post(config.url + 'auth/register/v2', json = {
        'email': 'gordon@gmail.com',
        'password': '1234aaaaaa',
        'name_first': 'Gordon',
        'name_last': 'Liang',
    })
    user_pl = user.json()

    user2 = requests.post(config.url + 'auth/register/v2', json = {
        'email': 'kanit@gmail.com',
        'password': '12345678',
        'name_first': 'Kanit',
        'name_last': 'Srihakorth',
    })
    user2_pl = user2.json()

    channel_info = requests.post(config.url + 'channels/create/v2', json = {
        'token': user_pl['token'],
        'name': 'Channel1',
        'is_public': True,
    })
    channel_info_pl = channel_info.json() 

    requests.post(config.url + 'channel/invite/v2', json = {
        'token': user_pl['token'],
        'channel_id': channel_info_pl['channel_id'],
        'u_id': user2_pl['auth_user_id'],
    })

    notification = requests.get(config.url + f"notifications/get/v1?token={user2_pl['token']}")
    notification_pl = notification.json()

    assert notification_pl['notifications'][0]['notification_message'] == 'gordonliang added you to Channel1'

def test_notifications_get_tag_dm(clear_data):
    '''
    Test if user got tagged in dm
    '''
    user = requests.post(config.url + 'auth/register/v2', json = {
        'email': 'gordon@gmail.com',
        'password': '1234aaaaaa',
        'name_first': 'Gordon',
        'name_last': 'Liang',
    })
    user_pl = user.json()

    user2 = requests.post(config.url + 'auth/register/v2', json = {
        'email': 'kanit@gmail.com',
        'password': '12345678',
        'name_first': 'Kanit',
        'name_last': 'Srihakorth',
    })
    user2_pl = user2.json()

    dm_info = requests.post(config.url + 'dm/create/v1', json = {
        'token': user_pl['token'],
        'u_ids': [user2_pl['auth_user_id']],
    })
    dm_info_pl = dm_info.json()

    requests.post(config.url + 'message/senddm/v1', json = {
        'token': user_pl['token'],
        'dm_id': dm_info_pl['dm_id'],
        'message': 'Hello @kanitsrihakorth',
    })

    notification = requests.get(config.url + f"notifications/get/v1?token={user2_pl['token']}")
    notification_pl = notification.json()
    assert notification_pl['notifications'][0]['notification_message'] == 'gordonliang added you to gordonliang, kanitsrihakorth'
    assert notification_pl['notifications'][1]['notification_message'] == 'gordonliang tagged you in gordonliang, kanitsrihakorth: Hello @kanitsrihakor'

def test_notifications_get_add_to_dm(clear_data):
    '''
    Test if user got added in dm
    '''
    user = requests.post(config.url + 'auth/register/v2', json = {
        'email': 'gordon@gmail.com',
        'password': '1234aaaaaa',
        'name_first': 'Gordon',
        'name_last': 'Liang',
    })
    user_pl = user.json()

    user2 = requests.post(config.url + 'auth/register/v2', json = {
        'email': 'kanit@gmail.com',
        'password': '12345678',
        'name_first': 'Kanit',
        'name_last': 'Srihakorth',
    })
    user2_pl = user2.json()

    requests.post(config.url + 'dm/create/v1', json = {
        'token': user_pl['token'],
        'u_ids': [user2_pl['auth_user_id']],
    })

    notification = requests.get(config.url + f"notifications/get/v1?token={user2_pl['token']}")
    notification_pl = notification.json()

    assert notification_pl['notifications'][0]['notification_message'] == 'gordonliang added you to gordonliang, kanitsrihakorth' 
