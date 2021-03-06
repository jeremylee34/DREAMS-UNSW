import pytest
import re
from src.other import search_v1
from src.other import notifications_get_v1
from src.auth import auth_register_v1
from src.channels import channels_create_v1
from src.channel import channel_invite_v1
from src.dm import dm_invite_v1 
from src.dm import dm_create_v1
from src.dm import dm_messages_v1
from src.message import message_send_v1
from src.message import message_senddm_v1
from src.other import clear_v1
from src.error import InputError, AccessError
from src.data import data

@pytest.fixture
def clear_data():
    clear_v1()

#search function tests
def test_search_v1(clear_data):
    '''
    Test for functionality in search
    '''
    user = auth_register_v1('gordon@gmail.com', '12345678', 'Gordon', 'Liang')
    channel_info = channels_create_v1(user['token'], 'Channel1', True)
    message_send_v1(user['token'], channel_info['channel_id'], 'Hello')
    assert search_v1(user['token'], 'Hello') != {}
    
def test_search_v1_input_error(clear_data):
    '''
    Test for input error in search
    '''
    user = auth_register_v1('gordon@gmail.com', '12345678', 'Gordon', 'Liang')
    channel_info = channels_create_v1(user['token'], 'Channel1', True)
    message_send_v1(user['token'], channel_info['channel_id'], 'Hello')
    with pytest.raises(InputError):
        assert search_v1(user['token'], 'Hello' * 1000)
        
def test_search_v1_invalid_token(clear_data):
    '''
    Test for invalid token in search
    '''
    with pytest.raises(AccessError):
        assert search_v1(6, 'Hello')
        assert search_v1('asdf', 'Helloooo')

def test_search_v1_session(clear_data):
    '''
    Test for invalid session in search
    '''
    user = auth_register_v1('gordon@gmail.com', '12345678', 'Gordon', 'Liang')
    user2 = auth_register_v1('kanit@gmail.com', '12345678', 'Kanit', 'Srihakorth')
    dm_info = dm_create_v1(user['token'], [user2['auth_user_id']])
    message_senddm_v1(user['token'], dm_info['dm_id'], 'Hello @kanitsrihakorth')
    notification = notifications_get_v1(user2['token'])
    assert notification['notifications'][0]['notification_message'] == 'gordonliang added you to gordonliang, kanitsrihakorth'
    assert notification['notifications'][1]['notification_message'] == 'gordonliang tagged you in gordonliang, kanitsrihakorth: Hello @kanitsrihakor'
    ###############
   

def test_search_v1_dm(clear_data):
    '''
    Test for dm in search
    '''
    user = auth_register_v1('gordon@gmail.com', '12345678', 'Gordon', 'Liang')
    user2 = auth_register_v1('kanit@gmail.com', '12345678', 'Kanit', 'Srihakorth')
    dm_info = dm_create_v1(user['token'], [user2['auth_user_id']])
    message_senddm_v1(user['token'], dm_info['dm_id'], 'Hello')
    message_senddm_v1(user['token'], dm_info['dm_id'], 'So')
    message_senddm_v1(user['token'], dm_info['dm_id'], 'Sleepy')

    result = search_v1(user['token'], 'Hello')
    assert len(result['messages']) == 1
    message_senddm_v1(user['token'], dm_info['dm_id'], 'Hello')
    result = search_v1(user['token'], 'Hello')
    assert len(result['messages']) == 2

    assert len(dm_messages_v1(user['token'], dm_info['dm_id'], 0)['messages']) == 4

def test_search_v1_query(clear_data):
    '''
    Test if query_str != message
    '''
    user = auth_register_v1('gordon@gmail.com', '12345678', 'Gordon', 'Liang')
    channel_info = channels_create_v1(user['token'], 'Channel1', True)
    message_send_v1(user['token'], channel_info['channel_id'], 'Hello')
    message_send_v1(user['token'], channel_info['channel_id'], 'So')
    message_send_v1(user['token'], channel_info['channel_id'], 'Sleepy')

    result = search_v1(user['token'], '')
    assert len(result['messages']) == 0

#notifications function tests
def test_notifications_get_invalid_token(clear_data):
    '''
    Test for invalid token in notifications_get
    '''
    with pytest.raises(AccessError):
        assert notifications_get_v1(5)

def test_notifications_get_tag(clear_data):
    '''
    Test if user got tagged in channel appear in notifications_get
    '''
    user = auth_register_v1('gordon@gmail.com', '12345678', 'Gordon', 'Liang')
    channel_info = channels_create_v1(user['token'], 'Channel1', True)
    message_send_v1(user['token'], channel_info['channel_id'], 'Hello @gordonliang')
    notification = notifications_get_v1(user['token'])
    assert notification['notifications'][0]['notification_message'] == 'gordonliang tagged you in Channel1: Hello @gordonliang'

def test_notifications_get_add_to_channel(clear_data):
    '''
    Test if user got added in channel appear in notifications_get
    '''
    user = auth_register_v1('gordon@gmail.com', '12345678', 'Gordon', 'Liang')
    user2 = auth_register_v1('kanit@gmail.com', '12345678', 'Kanit', 'Srihakorth')
    channel_info = channels_create_v1(user['token'], 'Channel1', True)
    channel_invite_v1(user['token'], channel_info['channel_id'], user2['auth_user_id'])
    notification = notifications_get_v1(user2['token'])
    assert notification['notifications'][0]['notification_message'] == 'gordonliang added you to Channel1'

def test_notifications_get_tag_dm(clear_data):
    '''
    Test if user got tagged in dm appear in notifications_get
    '''
    user = auth_register_v1('gordon@gmail.com', '12345678', 'Gordon', 'Liang')
    user2 = auth_register_v1('kanit@gmail.com', '12345678', 'Kanit', 'Srihakorth')
    dm_info = dm_create_v1(user['token'], [user2['auth_user_id']])
    message_senddm_v1(user['token'], dm_info['dm_id'], 'Hello @kanitsrihakorth')
    notification = notifications_get_v1(user2['token'])
    assert notification['notifications'][0]['notification_message'] == 'gordonliang added you to gordonliang, kanitsrihakorth'
    assert notification['notifications'][1]['notification_message'] == 'gordonliang tagged you in gordonliang, kanitsrihakorth: Hello @kanitsrihakor'

def test_notifications_get_add_to_dm(clear_data):
    '''
    Test if user got added in dm appear in notifications_get
    '''
    user = auth_register_v1('gordon@gmail.com', '12345678', 'Gordon', 'Liang')
    user2 = auth_register_v1('kanit@gmail.com', '12345678', 'Kanit', 'Srihakorth')
    dm_create_v1(user['token'], [user2['auth_user_id']])
    notification = notifications_get_v1(user2['token'])
    assert notification['notifications'][0]['notification_message'] == 'gordonliang added you to gordonliang, kanitsrihakorth'

def test_notifications_break_when_noti_twenty(clear_data):
    '''
    Test if the function break when it over 20
    '''
    user = auth_register_v1('gordon@gmail.com', '12345678', 'Gordon', 'Liang')
    user2 = auth_register_v1('kanit@gmail.com', '12345678', 'Kanit', 'Srihakorth')
    dm_info = dm_create_v1(user['token'], [user2['auth_user_id']])
    
    message_senddm_v1(user['token'], dm_info['dm_id'], 'Hello @kanitsrihakorth')
    message_senddm_v1(user['token'], dm_info['dm_id'], 'Hello @kanitsrihakorth')
    message_senddm_v1(user['token'], dm_info['dm_id'], 'Hello @kanitsrihakorth')
    message_senddm_v1(user['token'], dm_info['dm_id'], 'Hello @kanitsrihakorth')
    message_senddm_v1(user['token'], dm_info['dm_id'], 'Hello @kanitsrihakorth')
    message_senddm_v1(user['token'], dm_info['dm_id'], 'Hello @kanitsrihakorth')
    message_senddm_v1(user['token'], dm_info['dm_id'], 'Hello @kanitsrihakorth')
    message_senddm_v1(user['token'], dm_info['dm_id'], 'Hello @kanitsrihakorth')
    message_senddm_v1(user['token'], dm_info['dm_id'], 'Hello @kanitsrihakorth')
    message_senddm_v1(user['token'], dm_info['dm_id'], 'Hello @kanitsrihakorth')
    message_senddm_v1(user['token'], dm_info['dm_id'], 'Hello @kanitsrihakorth')
    message_senddm_v1(user['token'], dm_info['dm_id'], 'Hello @kanitsrihakorth')
    message_senddm_v1(user['token'], dm_info['dm_id'], 'Hello @kanitsrihakorth')
    message_senddm_v1(user['token'], dm_info['dm_id'], 'Hello @kanitsrihakorth')
    message_senddm_v1(user['token'], dm_info['dm_id'], 'Hello @kanitsrihakorth')
    message_senddm_v1(user['token'], dm_info['dm_id'], 'Hello @kanitsrihakorth')
    message_senddm_v1(user['token'], dm_info['dm_id'], 'Hello @kanitsrihakorth')
    message_senddm_v1(user['token'], dm_info['dm_id'], 'Hello @kanitsrihakorth')
    message_senddm_v1(user['token'], dm_info['dm_id'], 'Hello @kanitsrihakorth')
    message_senddm_v1(user['token'], dm_info['dm_id'], 'Hello @kanitsrihakorth')
    message_senddm_v1(user['token'], dm_info['dm_id'], 'Hello @kanitsrihakorth')

    notification = notifications_get_v1(user2['token'])
    assert notification['notifications'][19]['notification_message'] == 'gordonliang tagged you in gordonliang, kanitsrihakorth: Hello @kanitsrihakor'
    

