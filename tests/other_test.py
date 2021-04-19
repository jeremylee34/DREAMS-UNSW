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

@pytest.fixture
def clear_data():
    '''
    Clears all user data
    '''
    clear_v1()

@pytest.fixture
def user_token1():
    '''
    Registers first user
    '''
    user_token1 = auth_register_v1("firstUser@gmail.com", "password", "Paras", "Mins")
    return user_token1

@pytest.fixture
def user_token2():
    '''
    Registers second user
    '''
    user_token2 = auth_register_v1("secondUser@gmail.com", "password", "Goyas", "Lsiwe")
    return user_token2

@pytest.fixture
def user_token3():
    '''
    Registers third user
    '''
    user_token3 = auth_register_v1("thirdUser@gmail.com", "password", "Taraa", "safba")
    return user_token3

#search function tests
def test_search_v1(clear_data, user_token1):
    '''
    Test for functionality in search
    '''
    channel_info = channels_create_v1(user_token1['token'], 'Channel1', True)
    message_send_v1(user_token1['token'], channel_info['channel_id'], 'Hello')
    assert search_v1(user_token1['token'], 'Hello') != {}
    
def test_search_v1_input_error(clear_data, user_token1):
    '''
    Test for input error in search
    '''
    channel_info = channels_create_v1(user_token1['token'], 'Channel1', True)
    message_send_v1(user_token1['token'], channel_info['channel_id'], 'Hello')
    with pytest.raises(InputError):
        assert search_v1(user_token1['token'], 'Hello' * 1000)
        
def test_search_v1_invalid_token(clear_data):
    '''
    Test for invalid token in search
    '''
    with pytest.raises(InputError):
        assert search_v1(6, 'Hello')
        assert search_v1('asdf', 'Helloooo')

def test_search_v1_session(clear_data, user_token1, user_token2):
    '''
    Test for invalid session in search
    '''
    dm_info = dm_create_v1(user_token1['token'], [user_token2['auth_user_id']])
    message_senddm_v1(user_token1['token'], dm_info['dm_id'], 'Hello @goyaslsiwe')
    notification = notifications_get_v1(user_token2['token'])
    assert notification['notifications'][0]['notification_message'] == 'parasmins added you to goyaslsiwe, parasmins'
    assert notification['notifications'][1]['notification_message'] == 'parasmins tagged you in goyaslsiwe, parasmins: Hello @goyaslsiwe'
   
def test_search_v1_dm(clear_data, user_token1, user_token2):
    '''
    Test for dm in search
    '''
    dm_info = dm_create_v1(user_token1['token'], [user_token2['auth_user_id']])
    message_senddm_v1(user_token1['token'], dm_info['dm_id'], 'Hello')
    message_senddm_v1(user_token1['token'], dm_info['dm_id'], 'So')
    message_senddm_v1(user_token1['token'], dm_info['dm_id'], 'Sleepy')

    result = search_v1(user_token1['token'], 'Hello')
    assert len(result['messages']) == 1
    message_senddm_v1(user_token1['token'], dm_info['dm_id'], 'Hello')
    result = search_v1(user_token1['token'], 'Hello')
    assert len(result['messages']) == 2

    assert len(dm_messages_v1(user_token1['token'], dm_info['dm_id'], 0)['messages']) == 4

def test_search_v1_query(clear_data, user_token1):
    '''
    Test if query_str != message
    '''
    channel_info = channels_create_v1(user_token1['token'], 'Channel1', True)
    message_send_v1(user_token1['token'], channel_info['channel_id'], 'Hello')
    message_send_v1(user_token1['token'], channel_info['channel_id'], 'So')
    message_send_v1(user_token1['token'], channel_info['channel_id'], 'Sleepy')

    result = search_v1(user_token1['token'], '')
    assert len(result['messages']) == 0

#notifications function tests
def test_notifications_get_invalid_token(clear_data):
    '''
    Test for invalid token in notifications_get
    '''
    with pytest.raises(InputError):
        assert notifications_get_v1(5)

def test_notifications_get_tag(clear_data, user_token1):
    '''
    Test if user got tagged in channel appear in notifications_get
    '''
    channel_info = channels_create_v1(user_token1['token'], 'Channel1', True)
    message_send_v1(user_token1['token'], channel_info['channel_id'], 'Hello @parasmins')
    notification = notifications_get_v1(user_token1['token'])
    assert notification['notifications'][0]['notification_message'] == 'parasmins tagged you in Channel1: Hello @parasmins'

def test_notifications_get_add_to_channel(clear_data, user_token1, user_token2):
    '''
    Test if user got added in channel appear in notifications_get
    '''
    channel_info = channels_create_v1(user_token1['token'], 'Channel1', True)
    channel_invite_v1(user_token1['token'], channel_info['channel_id'], user_token2['auth_user_id'])
    notification = notifications_get_v1(user_token2['token'])
    assert notification['notifications'][0]['notification_message'] == 'parasmins added you to Channel1'

def test_notifications_get_tag_dm(clear_data, user_token1, user_token2):
    '''
    Test if user got tagged in dm appear in notifications_get
    '''
    dm_info = dm_create_v1(user_token1['token'], [user_token2['auth_user_id']])
    message_senddm_v1(user_token1['token'], dm_info['dm_id'], 'Hello @goyaslsiwe')
    notification = notifications_get_v1(user_token2['token'])
    assert notification['notifications'][0]['notification_message'] == 'parasmins added you to goyaslsiwe, parasmins'
    assert notification['notifications'][1]['notification_message'] == 'parasmins tagged you in goyaslsiwe, parasmins: Hello @goyaslsiwe'

def test_notifications_get_add_to_dm(clear_data, user_token1, user_token2):
    '''
    Test if user got added in dm appear in notifications_get
    '''
    dm_create_v1(user_token1['token'], [user_token2['auth_user_id']])
    notification = notifications_get_v1(user_token2['token'])
    assert notification['notifications'][0]['notification_message'] == 'parasmins added you to goyaslsiwe, parasmins'

def test_notifications_break_when_noti_twenty(clear_data, user_token1, user_token2):
    '''
    Test if the function break when it over 20
    '''
    dm_info = dm_create_v1(user_token1['token'], [user_token2['auth_user_id']])

    for i in range(0, 20):
        message_senddm_v1(user_token1['token'], dm_info['dm_id'], 'Hello @goyaslsiwe')
        i+=1

    notification = notifications_get_v1(user_token2['token'])
    assert notification['notifications'][19]['notification_message'] == 'parasmins tagged you in goyaslsiwe, parasmins: Hello @goyaslsiwe'
    

