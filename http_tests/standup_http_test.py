
################################################################################
#########################         IMPORTS          #############################
################################################################################

import pytest
import jwt
import requests
import time
from src.config import url
from src.other import clear_v1
from src.error import InputError
from src.error import AccessError

################################################################################
#########################     GLOBAL VARIABLES     #############################
################################################################################

INPUT_ERROR = 400
ACCESS_ERROR = 403
INVALID_ID = 9999
SECRET = "HELLO"
INVALID_TOKEN = jwt.encode({"session_id": 9999}, SECRET, algorithm = "HS256")

################################################################################
#########################         FIXTURES         #############################
################################################################################

@pytest.fixture
def clear_data():
    requests.delete(f"{url}/clear/v1")

@pytest.fixture
def user_token1():
    info1 = requests.post(f"{url}/auth/register/v2", json={
        'email': 'Godan@gmail.com',
        'password': 'password',
        'name_first': 'Godan',
        'name_last': 'Liang'
    }).json()
    return info1

@pytest.fixture
def user_token2(user_token1):
    info2 = requests.post(f"{url}/auth/register/v2", json={
        'email': 'Jeremy@gmail.com',
        'password': 'password',
        'name_first': 'Jeremy',
        'name_last': 'Lee'
    }).json()
    return info2

@pytest.fixture
def channel_id1(user_token1):
    channel_id1 = requests.post(f"{url}/channels/create/v2", json={
        'token': user_token1['token'],
        'name': "Channel1",
        'is_public': True
    }).json()
    return channel_id1

################################################################################
#####################      standup_start_v1 tests      #########################
################################################################################

def test_standup_start_v1_input_error1(clear_data, user_token1):
    """
    Tests when channel_id is not valid
    """
    length = 0.05
    assert requests.post(f"{url}/standup/start/v1", json={
        'token': user_token1['token'],
        'channel_id': INVALID_ID,
        'length': length
    }).status_code == INPUT_ERROR

def test_standup_start_v1_input_error2(clear_data, user_token1, channel_id1):
    """
    Tests when a standup is trying to be started when there is already an 
    active standup in the channel
    """
    length = 0.05
    requests.post(f"{url}/standup/start/v1", json={
        'token': user_token1['token'],
        'channel_id': channel_id1['channel_id'],
        'length': length
    })
    assert requests.post(f"{url}/standup/start/v1", json={
        'token': user_token1['token'],
        'channel_id': channel_id1['channel_id'],
        'length': length
    }).status_code == INPUT_ERROR

def test_standup_start_v1_access_error(clear_data, user_token2, channel_id1):
    """
    Tests when authorised user is not the channel
    """
    length = 0.05
    assert requests.post(f"{url}/standup/start/v1", json={
        'token': user_token2['token'],
        'channel_id': channel_id1['channel_id'],
        'length': length
    }).status_code == ACCESS_ERROR

def test_standup_start_v1_invalid_token(clear_data, channel_id1):
    """
    Tests when an invalid token is passed in
    """
    length = 0.05
    assert requests.post(f"{url}/standup/start/v1", json={
        'token': INVALID_TOKEN,
        'channel_id': channel_id1['channel_id'],
        'length': length
    }).status_code == INPUT_ERROR

def test_standup_start_v1_simple(clear_data, user_token1, channel_id1):
    """
    No way to test that time finish is exactly precise, so just testing that
    no exceptions are raised.
    """
    length = 0.05
    requests.post(f"{url}/standup/start/v1", json={
        'token': user_token1['token'],
        'channel_id': channel_id1['channel_id'],
        'length': length
    })

def test_standup_active_v1_input_error1(clear_data, user_token1):
    """
    Tests when channel_id is not valid
    """
    assert requests.get(f"{url}/standup/active/v1?token={user_token1['token']}&channel_id={INVALID_ID}").status_code == INPUT_ERROR

def test_standup_active_v1_invalid_token(clear_data, channel_id1):
    """
    Tests when an invalid token is passed in
    """
    assert requests.get(f"{url}/standup/active/v1?token={INVALID_TOKEN}&channel_id={channel_id1['channel_id']}").status_code == INPUT_ERROR

def test_standup_active_v1_active(clear_data, user_token1, channel_id1):
    """
    Tests return values when there is an active standup
    """
    length = 0.05
    requests.post(f"{url}/standup/start/v1", json={
        'token': user_token1['token'],
        'channel_id': channel_id1['channel_id'],
        'length': length
    })
    activity = requests.get(f"{url}/standup/active/v1?token={user_token1['token']}&channel_id={channel_id1['channel_id']}").json()
    assert activity['is_active'] is True
    assert activity['time_finish'] is not None

def test_standup_active_v1_inactive(clear_data, user_token1, channel_id1):
    """
    Tests return values when the active standup has timed out
    """
    length = 0.05
    requests.post(f"{url}/standup/start/v1", json={
        'token': user_token1['token'],
        'channel_id': channel_id1['channel_id'],
        'length': length
    })
    time.sleep(0.06)
    activity = requests.get(f"{url}/standup/active/v1?token={user_token1['token']}&channel_id={channel_id1['channel_id']}").json()
    assert activity['is_active'] is False
    assert activity['time_finish'] is None

def test_standup_send_v1_input_error1(clear_data, user_token1, channel_id1):
    """
    Tests when channel_id is not valid
    """
    length = 0.05
    message = 'hello'
    requests.post(f"{url}/standup/start/v1", json={
        'token': user_token1['token'],
        'channel_id': channel_id1['channel_id'],
        'length': length
    })
    assert requests.post(f"{url}/standup/send/v1", json={
        'token': user_token1['token'],
        'channel_id': INVALID_ID,
        'message': message
    }).status_code == INPUT_ERROR

def test_standup_send_v1_input_error2(clear_data, user_token1, channel_id1):
    """
    Tests when message is over 1000 characters
    """
    length = 0.05
    message = 'a' * 1001
    requests.post(f"{url}/standup/start/v1", json={
        'token': user_token1['token'],
        'channel_id': channel_id1['channel_id'],
        'length': length
    })
    assert requests.post(f"{url}/standup/send/v1", json={
        'token': user_token1['token'],
        'channel_id': channel_id1['channel_id'],
        'message': message
    }).status_code == INPUT_ERROR

def test_standup_send_v1_input_error3(clear_data, user_token1, channel_id1):
    """
    Test when there is no active standup in the channel
    """
    message = 'hi'
    assert requests.post(f"{url}/standup/send/v1", json={
        'token': user_token1['token'],
        'channel_id': channel_id1['channel_id'],
        'message': message
    }).status_code == INPUT_ERROR

def test_standup_send_v1_access_error(clear_data, user_token1, user_token2, channel_id1):
    """
    Test when user is not in the channel
    """
    length = 0.05
    message = 'hi'
    requests.post(f"{url}/standup/start/v1", json={
        'token': user_token2['token'],
        'channel_id': channel_id1['channel_id'],
        'length': length
    })

def test_standup_send_v1(clear_data, user_token1, channel_id1):
    """
    Testing whether a standup message is collected and added to messages
    """
    length = 0.05
    message = 'hi'
    requests.post(f"{url}/standup/start/v1", json={
        'token': user_token1['token'],
        'channel_id': channel_id1['channel_id'],
        'length': length
    })
    requests.post(f"{url}/standup/send/v1", json={
        'token': user_token1['token'],
        'channel_id': channel_id1['channel_id'],
        'message': message
    })
    time.sleep(0.06)
    msgs = requests.get(f"{url}/channel/messages/v2?token={user_token1['token']}&channel_id={channel_id1['channel_id']}&start={0}").json()
    assert len(msgs['messages']) == 1

def test_standup_send_v1_many_messages(clear_data, user_token1, channel_id1):
    """
    Testing whether multiple standup messages are collected and added to messages
    correctly
    """
    length = 1.0
    requests.post(f"{url}/standup/start/v1", json={
        'token': user_token1['token'],
        'channel_id': channel_id1['channel_id'],
        'length': length
    })
    for i in range(0, 10):
        requests.post(f"{url}/standup/send/v1", json={
            'token': user_token1['token'],
            'channel_id': channel_id1['channel_id'],
            'message': str(i)
        })
    test_msg = []
    for j in range(0,10):
        test_msg.append(f"godanliang: {str(j)}")
    msg_block_joined = '\n'.join(test_msg)
    time.sleep(1.01)
    msgs = requests.get(f"{url}/channel/messages/v2?token={user_token1['token']}&channel_id={channel_id1['channel_id']}&start={0}").json()
    assert len(msgs['messages']) == 1
    assert msgs['messages'][0]['message'] == msg_block_joined

def test_standup_send_v1_multiple_standups(clear_data, user_token1, channel_id1):
    """
    Testing whether having standups run back-to-back adds to messages each time
    """
    length = 0.05
    message = 'hi'
    requests.post(f"{url}/standup/start/v1", json={
        'token': user_token1['token'],
        'channel_id': channel_id1['channel_id'],
        'length': length
    })
    requests.post(f"{url}/standup/send/v1", json={
        'token': user_token1['token'],
        'channel_id': channel_id1['channel_id'],
        'message': message
    })
    time.sleep(0.06)
    requests.post(f"{url}/standup/start/v1", json={
        'token': user_token1['token'],
        'channel_id': channel_id1['channel_id'],
        'length': length
    })
    requests.post(f"{url}/standup/send/v1", json={
        'token': user_token1['token'],
        'channel_id': channel_id1['channel_id'],
        'message': message
    })
    time.sleep(0.06)
    msgs = requests.get(f"{url}/channel/messages/v2?token={user_token1['token']}&channel_id={channel_id1['channel_id']}&start={0}").json()
    assert len(msgs['messages']) == 2