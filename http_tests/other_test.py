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
    channel_info_pl = channel_info.json()

    #send message
    requests.post(config.url + 'message/send/v2', json = {
        'token': user_pl['token'],
        'channel_id': channel_info_pl['channel_id'],
        'message': 'Hello',
    })

    #def message_send_v1(token, channel_id, message):

    # return {
    #    'message_id': message_id,
    #}   
    assert requests.get(config.url + 'search/v2', json = {
        'token': user_pl['token'],
        'query_str': 'Hello',
    }).status_code == 200

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
    channel_info_pl = channel_info.json()

    requests.post(config.url + 'message/send/v2', json = {
        'token': user_pl['token'],
        'channel_id': channel_info_pl['channel_id'],
        'message': 'Hello',
    })

    assert requests.get(config.url + 'search/v2', json = {
        'token': user_pl['token'],
        'query_str':'Hello' * 1000,
    }).status_code == InputError.code

def test_search_v2_input_token(clear_data):
    assert requests.get(config.url + 'search/v2', json = {
        'token': 6,
        'query_str':'Hello',
    }).status_code == AccessError.code


#notification test
def test_notifications_get_invalid_token(clear_data):
    assert requests.get(config.url + 'notifications/get/v1', json = {
        'token': 6,
    }).status_code == AccessError.code

def test_notifications_get_tag(clear_data):
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

    notification = requests.get(config.url + 'notifications/get/v1', json = {
        'token': user_pl['token'],
    })
    notification_pl = notification.json()

    assert notification_pl['notifications'][0]['notification_message'] == 'gordonliang tagged you in Channel1: Hello @gordonliang'

'''
def test_notifications_get_tag(clear_data):
    [x] user = auth_register_v1('gordon@gmail.com', '12345678', 'Gordon', 'Liang')
    [x] channel_info = channels_create_v1(user['token'], 'Channel1', True)
    [x] message_send_v1(user['token'], channel_info['channel_id'], 'Hello @gordonliang')
    notification = notifications_get_v1(user['token'])
    assert notification['notifications'][0]['notification_message'] == 'gordonliang tagged you in Channel1: Hello @gordonliang'
'''

def test_notifications_get_add_to_channel(clear_data):
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

    notification = requests.get(config.url + 'notifications/get/v1', json = {
        'token': user2_pl['token'],
    })
    notification_pl = notification.json()

    assert notification_pl['notifications'][0]['notification_message'] == 'gordonliang added you to Channel1'

def test_notifications_get_tag_dm(clear_data):
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

    msg_senddm = requests.post(config.url + 'message/senddm/v1', json = {
        'token': user_pl['token'],
        'dm_id': dm_info_pl['dm_id'],
        'message': 'Hello @kanitsrihakorth',
    })

    notification = requests.get(config.url + 'notifications/get/v1', json = {
        'token': user2_pl['token'],
    })
    notification_pl = notification.json()
    #change input
    assert notification_pl['notifications'][0]['notification_message'] == 'gordonliang added you to gordonliang, kanitsrihakorth'
    assert notification_pl['notifications'][1]['notification_message'] == 'gordonliang tagged you in gordonliang, kanitsrihakorth: Hello @kanitsrihakor'

def test_notifications_get_add_to_dm(clear_data):
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

    notification = requests.get(config.url + 'notifications/get/v1', json = {
        'token': user2_pl['token'],
    })
    notification_pl = notification.json()

    assert notification_pl['notifications'][0]['notification_message'] == 'gordonliang added you to gordonliang, kanitsrihakorth' 

'''
def test_notifications_get_add_to_dm(clear_data):
    [x] user = auth_register_v1('gordon@gmail.com', '12345678', 'Gordon', 'Liang')
    [x] user2 = auth_register_v1('kanit@gmail.com', '12345678', 'Kanit', 'Srihakorth')
    [x] dm_info = dm_create_v1(user['token'], [user2['auth_user_id']])
    [x] notification = notifications_get_v1(user2['token'])
    assert notification['notifications'][0]['notification_message'] == 'gordonliang added you to gordonliang, kanitsrihakorth'
    '''