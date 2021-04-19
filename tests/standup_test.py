
################################################################################
#########################         IMPORTS          #############################
################################################################################

from src.standup import standup_start_v1
from src.standup import standup_active_v1
from src.standup import standup_send_v1
from src.auth import auth_register_v1
from src.channels import channels_create_v1
from src.user import user_profile_v1
from src.channel import channel_messages_v1

#Import error from src
from src.error import InputError
from src.error import AccessError

#Import other from src
from src.other import clear_v1

from datetime import datetime
from datetime import timedelta
from datetime import timezone

import pytest
import jwt
import time

##############################################################################
#########################     GLOBAL VARIABLES     #############################
################################################################################

INVALID_ID = 1000
SECRET = "HELLO"
INVALID_TOKEN = jwt.encode({"session_id": 9999}, SECRET, algorithm = "HS256")

################################################################################
#########################         FIXTURES         #############################
################################################################################

@pytest.fixture
def user_token1():
    user_token1 = auth_register_v1("Roland@gmail.com", "password", "Roland", "Lin")
    return user_token1

@pytest.fixture
def user_token2(user_token1):
    user_token2 = auth_register_v1("Godan@gmail.com", "password", "Godan", "Liang")
    return user_token2
    
@pytest.fixture
def user_token3(user_token1, user_token2):
    user_token3 = auth_register_v1("Jeremy@gmail.com", "password", "Jeremy", "Lee")
    return user_token3

@pytest.fixture    
def channel_id1(user_token1):
    channel_id1 = channels_create_v1(user_token1['token'], "Channel1", True)
    return channel_id1

#Fixture for clear to prevent clearing of other fixtures
@pytest.fixture
def clear_data():
    clear_v1()

################################################################################
#####################          standup tests           #########################
################################################################################

def test_standup_start_v1_input_error1(clear_data, user_token1):
    """
    Tests when channel_id is not valid
    """
    length = 1.0
    with pytest.raises(InputError):
        standup_start_v1(user_token1['token'], INVALID_ID, length)

def test_standup_start_v1_input_error2(clear_data, user_token1, channel_id1):
    """
    Tests when a standup is trying to be started when there is already an 
    active standup in the channel
    """
    length = 1.0
    standup_start_v1(user_token1['token'], channel_id1['channel_id'], length)
    with pytest.raises(InputError):
        standup_start_v1(user_token1['token'], channel_id1['channel_id'], length)

def test_standup_start_v1_access_error(clear_data, user_token2, channel_id1):
    """
    Tests when authorised user is not the channel
    """
    length = 1.0
    with pytest.raises(AccessError):
        standup_start_v1(user_token2['token'], channel_id1['channel_id'], length)

def test_standup_start_v1_invalid_token(clear_data, channel_id1):
    """
    Tests when an invalid token is passed in
    """
    length = 1.0
    with pytest.raises(InputError):
        standup_start_v1(INVALID_TOKEN, channel_id1['channel_id'], length)

def test_standup_start_v1_simple(clear_data, user_token1, channel_id1):
    """
    No way to test that time finish is exactly precise, so just testing that
    no exceptions are raised.
    """
    length = 1.0
    standup_start_v1(user_token1['token'], channel_id1['channel_id'], length)
    msgs = channel_messages_v1(user_token1['token'], channel_id1['channel_id'], 0)
    assert len(msgs['messages']) == 0
    time.sleep(1.5)
    

def test_standup_active_v1_input_error1(clear_data, user_token1):
    """
    Tests when channel_id is not valid
    """
    with pytest.raises(InputError):
        standup_active_v1(user_token1['token'], INVALID_ID)

def test_standup_active_v1_invalid_token(clear_data, channel_id1):
    """
    Tests when an invalid token is passed in
    """
    with pytest.raises(InputError):
        standup_active_v1(INVALID_TOKEN, channel_id1['channel_id'])

def test_standup_active_v1_active(clear_data, user_token1, channel_id1):
    """
    Tests return values when there is an active standup
    """
    length = 1.0
    standup_start_v1(user_token1['token'], channel_id1['channel_id'], length)
    activity = standup_active_v1(user_token1['token'], channel_id1['channel_id'])
    assert activity['is_active'] is True
    assert activity['time_finish'] is not None
    time.sleep(1.5)

def test_standup_active_v1_inactive(clear_data, user_token1, channel_id1):
    """
    Tests return values when the active standup has timed out
    """
    length = 1.0
    standup_start_v1(user_token1['token'], channel_id1['channel_id'], length)
    time.sleep(1.5)
    activity = standup_active_v1(user_token1['token'], channel_id1['channel_id'])
    assert activity['is_active'] is False
    assert activity['time_finish'] is None

def test_standup_send_v1_input_error1(clear_data, user_token1, channel_id1):
    """
    Tests when channel_id is not valid
    """
    length = 1.0
    message = 'hello'
    standup_start_v1(user_token1['token'], channel_id1['channel_id'], length)
    with pytest.raises(InputError):
        standup_send_v1(user_token1['token'], INVALID_ID, message)
    time.sleep(1.5)

def test_standup_send_v1_input_error2(clear_data, user_token1, channel_id1):
    """
    Tests when message is over 1000 characters
    """
    length = 1.0
    message = 'a' * 1001
    standup_start_v1(user_token1['token'], channel_id1['channel_id'], length)
    with pytest.raises(InputError):
        standup_send_v1(user_token1['token'], channel_id1['channel_id'], message)
    time.sleep(1.5)

def test_standup_send_v1_input_error3(clear_data, user_token1, channel_id1):
    """
    Test when there is no active standup in the channel
    """
    message = 'hi'
    with pytest.raises(InputError):
        standup_send_v1(user_token1['token'], channel_id1['channel_id'], message)

def test_standup_send_v1_access_error(clear_data, user_token1, user_token2, channel_id1):
    """
    Test when user is not in the channel
    """
    length = 1.0
    message = 'hi'
    standup_start_v1(user_token1['token'], channel_id1['channel_id'], length)
    with pytest.raises(AccessError):
        standup_send_v1(user_token2['token'], channel_id1['channel_id'], message)
    time.sleep(1.5)

def test_standup_send_v1(clear_data, user_token1, channel_id1):
    """
    Testing whether a standup message is collected and added to messages
    """
    length = 1.0
    message = 'hi'
    standup_start_v1(user_token1['token'], channel_id1['channel_id'], length)
    standup_send_v1(user_token1['token'], channel_id1['channel_id'], message)
    time.sleep(1.5)
    msgs = channel_messages_v1(user_token1['token'], channel_id1['channel_id'], 0)
    assert len(msgs['messages']) == 1

def test_standup_send_v1_many_messages(clear_data, user_token1, channel_id1):
    """
    Testing whether multiple standup messages are collected and added to messages
    correctly
    """
    length = 1.0
    standup_start_v1(user_token1['token'], channel_id1['channel_id'], length)
    for i in range(0, 10):
        standup_send_v1(user_token1['token'], channel_id1['channel_id'], str(i))
    test_msg = []
    for j in range(0,10):
        test_msg.append(f"rolandlin: {str(j)}")
    msg_block_joined = '\n'.join(test_msg)
    time.sleep(1.5)
    msgs = channel_messages_v1(user_token1['token'], channel_id1['channel_id'], 0)
    assert len(msgs['messages']) == 1
    assert msgs['messages'][0]['message'] == msg_block_joined

def test_standup_send_v1_multiple_standups(clear_data, user_token1, channel_id1):
    """
    Testing whether having standups run back-to-back adds to messages each time
    """
    length = 1.0
    message = 'hi'
    standup_start_v1(user_token1['token'], channel_id1['channel_id'], length)
    standup_send_v1(user_token1['token'], channel_id1['channel_id'], message)
    time.sleep(1.5)
    standup_start_v1(user_token1['token'], channel_id1['channel_id'], length)
    standup_send_v1(user_token1['token'], channel_id1['channel_id'], message)
    time.sleep(1.5)
    msgs = channel_messages_v1(user_token1['token'], channel_id1['channel_id'], 0)
    assert len(msgs['messages']) == 2

def test_standup_send_v1_invalid_token(clear_data, user_token1, channel_id1):
    """
    Testing when user token is invalid
    """
    length = 1.0
    message = 'hi'
    standup_start_v1(user_token1['token'], channel_id1['channel_id'], length)
    with pytest.raises(InputError):
        standup_send_v1(INVALID_TOKEN, channel_id1['channel_id'], message)
    time.sleep(1.5)