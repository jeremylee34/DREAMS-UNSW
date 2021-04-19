'''
Http tests for message functions
Written by Gordon Liang
'''
import pytest
import requests
from src.config import url
from datetime import datetime, timedelta, timezone
import time

@pytest.fixture
def clear():
    '''
    Clears data in data file
    '''
    requests.delete(f"{url}/clear/v1")
@pytest.fixture
def register_info():
    '''
    Registers a user
    '''
    register_info = requests.post(f"{url}/auth/register/v2", json={
        'email': 'gordon@gmail.com',
        'password': '12345678',
        'name_first': 'Gordon',
        'name_last': 'Liang'
    })
    register_info = register_info.json()
    return register_info
@pytest.fixture
def register_info2():
    '''
    Registers a second user
    '''
    register_info2 = requests.post(f"{url}/auth/register/v2", json={
        'email': 'roland@gmail.com',
        'password': '12345678',
        'name_first': 'Roland',
        'name_last': 'Lin'
    })
    register_info2 = register_info2.json()
    return register_info2
@pytest.fixture
def register_info3():
    '''
    Registers a third user
    '''
    register_info3 = requests.post(f"{url}/auth/register/v2", json={
        'email': 'jeremy@gmail.com',
        'password': '12345678',
        'name_first': 'Jeremy',
        'name_last': 'Lee'
    })
    register_info3 = register_info3.json()
    return register_info3
@pytest.fixture
def channel(register_info):
    '''
    Creates a channel with first user
    '''
    channel = requests.post(f"{url}/channels/create/v2", json={
        'token': register_info['token'],
        'name': 'Channel1',
        'is_public': True
    })
    channel = channel.json()
    return channel
@pytest.fixture
def message_id(register_info, channel):
    '''
    Sends a message to first channel
    '''
    message_id = requests.post(f"{url}/message/send/v2", json={
        'token': register_info['token'],
        'channel_id': channel['channel_id'],
        'message': 'Hello'
    })
    message_id = message_id.json()
    return message_id
@pytest.fixture
def messages(register_info, channel):
    '''
    Gets the messages of a channel
    '''
    messages = requests.get(f"{url}/channel/messages/v2?token={register_info['token']}&channel_id={channel['channel_id']}&start=0")
    messages = messages.json()
    return messages
@pytest.fixture
def edit(register_info, message_id):
    '''
    Edits a message
    '''
    requests.put(f"{url}/message/edit/v2", json={
        'token': register_info['token'],
        'message_id': message_id['message_id'],
        'message': '123'
    })
@pytest.fixture
def remove(register_info, message_id):
    '''
    Removes a message
    '''
    requests.delete(f"{url}/message/remove/v1", json={
        'token': register_info['token'],
        'message_id': message_id['message_id']
    })
@pytest.fixture
def join(register_info2, channel):
    '''
    Joins a channel
    '''
    requests.post(f"{url}/channel/join/v2", json={
        'token': register_info2['token'],
        'channel_id': channel['channel_id']
    })
@pytest.fixture
def dm_info(register_info, register_info2):
    '''
    Creates a DM with two users
    '''
    dm_info = requests.post(f"{url}/dm/create/v1", json={
        'token': register_info['token'],
        'u_ids': [register_info2['auth_user_id']]
    })
    dm_info = dm_info.json()
    return dm_info
@pytest.fixture
def dm_message_id(register_info, dm_info):
    '''
    Sends a message to a DM
    '''
    dm_message_id = requests.post(f"{url}/message/senddm/v1", json={
        'token': register_info['token'],
        'dm_id': dm_info['dm_id'],
        'message': 'Hello'
    })
    dm_message_id = dm_message_id.json()
    return dm_message_id
@pytest.fixture
def channel2(register_info):
    '''
    Creates a second channel
    '''
    channel2 = requests.post(f"{url}/channels/create/v2", json={
        'token': register_info['token'],
        'name': 'Channel2',
        'is_public': True
    })
    channel2 = channel2.json()
    return channel2
@pytest.fixture
def timestamp():
    '''
    Creates a time two seconds from the present as a unix timestamp
    '''
    timestamp = int(time.time())
    return timestamp
@pytest.fixture
def past_time():
    '''
    Creates a past time as a unix timestamp
    '''
    time = datetime(2020, 4, 20)
    new_time = time + timedelta(seconds=5)
    timestamp = new_time.replace(tzinfo=timezone.utc).timestamp()
    return timestamp
def test_message_send(clear, register_info, channel, message_id, messages):
    '''
    Basic test for functionality of message/send/v2
    '''
    assert messages['messages'][0]['message'] == 'Hello'
def test_message_send_input_error(clear, register_info, channel):
    '''
    Tests for when message is over 1000 characters
    '''
    assert requests.post(f"{url}/message/send/v2", json={
        'token': register_info['token'],
        'channel_id': channel['channel_id'],
        'message': 'Hello' * 500
    }).status_code == 400
def test_message_send_input_error2(clear, register_info, channel):
    '''
    Tests for when no message is put in
    '''
    assert requests.post(f"{url}/message/send/v2", json={
        'token': register_info['token'],
        'channel_id': channel['channel_id'],
        'message': ''
    }).status_code == 400
def test_message_send_access_error(clear, register_info, register_info2, channel):
    '''
    Tests for when a user hasn't joined the channel and tries to send message
    '''
    assert requests.post(f"{url}/message/send/v2", json={
        'token': register_info2['token'],
        'channel_id': channel['channel_id'],
        'message': 'Hello'
    }).status_code == 403
def test_message_send_invalid_token(clear, register_info, channel):
    '''
    Tests for invalid token
    '''
    assert requests.post(f"{url}/message/send/v2", json={
        'token': 4,
        'channel_id': channel['channel_id'],
        'message': 'Hello'
    }).status_code == 400

def test_message_edit(clear, register_info, channel, message_id, edit, messages):
    '''
    Basic test for functionality of message/edit/v2
    '''
    assert messages['messages'][0]['message'] == '123'
def test_message_edit_input_error(clear, register_info, channel, message_id):
    '''
    Tests for when message is more than 1000 characters
    '''
    assert requests.put(f"{url}/message/edit/v2", json={
        'token': register_info['token'],
        'message_id': message_id['message_id'],
        'message': '123' * 1000
    }).status_code == 400
def test_message_edit_input_error2(clear, register_info, channel, message_id, remove):
    '''
    Tests for when a message has already been deleted
    '''
    assert requests.put(f"{url}/message/edit/v2", json={
        'token': register_info['token'],
        'message_id': message_id['message_id'],
        'message': '123'
    }).status_code == 400
def test_message_edit_access_error(clear, register_info, register_info2, channel, message_id, join):
    '''
    Tests for when the message was not sent by user and user is not an owner
    '''
    assert requests.put(f"{url}/message/edit/v2", json={
        'token': register_info2['token'],
        'message_id': message_id['message_id'],
        'message': '1'
    }).status_code == 403
def test_edit_message_no_error(clear, register_info, register_info2, channel, join):
    '''
    Checks to see if regular member can edit their message
    '''
    message_id = requests.post(f"{url}/message/send/v2", json={
        'token': register_info2['token'],
        'channel_id': channel['channel_id'],
        'message': 'Hello'
    })
    message_id = message_id.json()
    requests.put(f"{url}/message/edit/v2", json={
        'token': register_info2['token'],
        'message_id': message_id['message_id'],
        'message': '123'
    })
    messages = requests.get(f"{url}/channel/messages/v2?token={register_info2['token']}&channel_id={channel['channel_id']}&start=0")
    messages = messages.json()
    assert messages['messages'][0]['message'] == '123'

def test_message_remove(clear, register_info, channel, message_id, remove, messages):
    '''
    Basic test for message/remove/v2
    '''
    assert messages['messages'] == []
def test_message_remove_input_error(clear, register_info, channel, message_id, remove):
    '''
    Tests for when message has already been removed
    '''
    assert requests.delete(f"{url}/message/remove/v1", json={
        'token': register_info['token'],
        'message_id': message_id['message_id']
    }).status_code == 400
def test_message_remove_access_error(clear, register_info, register_info2, channel, message_id, join):
    '''
    Tests for when the message was not sent by the user and user is not an owner
    '''
    assert requests.delete(f"{url}/message/remove/v1", json={
        'token': register_info2['token'],
        'message_id': message_id['message_id'],
    }).status_code == 403
def test_message_remove_dm(clear, register_info, register_info2, dm_info, dm_message_id, ):
    '''
    Tests removing a message from a dm
    '''
    requests.delete(f"{url}/message/remove/v1", json={
        'token': register_info['token'],
        'message_id': dm_message_id['message_id'],
    })
    messages = requests.get(f"{url}/dm/messages/v1?token={register_info['token']}&dm_id={dm_info['dm_id']}&start=0")
    messages = messages.json()
    assert messages['messages'][0]['message'] == ''

def test_message_share(clear, register_info, channel, channel2, message_id):
    '''
    Basic testfor message/share/v2
    '''
    requests.post(f"{url}/message/share/v1", json={
        'token': register_info['token'],
        'og_message_id': message_id['message_id'],
        'message': '123',
        'channel_id': channel2['channel_id'],
        'dm_id': -1
    })
    messages = requests.get(f"{url}/channel/messages/v2?token={register_info['token']}&channel_id={channel2['channel_id']}&start=0")
    messages = messages.json()
    assert messages['messages'][0]['message'] == 'Hello123'
def test_message_share_access_error(clear, register_info, register_info2, channel, message_id):
    '''
    Tests for when the user has not joined the channel they are sharing to
    '''
    channel2 = requests.post(f"{url}/channels/create/v2", json={
        'token': register_info2['token'],
        'name': 'Channel2',
        'is_public': True
    })
    channel2 = channel2.json()
    assert requests.post(f"{url}/message/share/v1", json={
        'token': register_info['token'],
        'og_message_id': message_id['message_id'],
        'message': '123',
        'channel_id': channel2['channel_id'],
        'dm_id': -1
    }).status_code == 403
def test_message_share_invalid_token(clear, register_info, channel, message_id, channel2):
    '''
    Tests for invalid token
    '''
    assert requests.post(f"{url}/message/share/v1", json={
        'token': 1,
        'og_message_id': message_id['message_id'],
        'message': '123',
        'channel_id': channel2['channel_id'],
        'dm_id': -1
    }).status_code == 400
# def test_message_share_deleted_message(clear):
#     '''
#     Tests for when a message is deleted
#     '''
#     register_info = requests.post(f"{url}/auth/register/v2", json={
#         'email': 'gordon@gmail.com',
#         'password': '12345678',
#         'name_first': 'Gordon',
#         'name_last': 'Liang'
#     })
#     register_info = register_info.json()
#     channel = requests.post(f"{url}/channels/create/v2", json={
#         'token': register_info['token'],
#         'name': 'Channel1',
#         'is_public': True
#     })
#     channel = channel.json()
#     channel2 = requests.post(f"{url}/channels/create/v2", json={
#         'token': register_info['token'],
#         'name': 'Channel2',
#         'is_public': True
#     })
#     channel2 = channel2.json()
#     message_info = requests.post(f"{url}/message/send/v2", json={
#         'token': register_info['token'],
#         'channel_id': channel['channel_id'],
#         'message': 'Hello'
#     })
#     message_info = message_info.json()
#     requests.delete(f"{url}/message/remove/v1", json={
#         'token': register_info['token'],
#         'message_id': message_info['message_id']
#     })
#     assert requests.post(f"{url}/message/share/v1", json={
#         'token': register_info['token'],
#         'og_message_id': message_info['message_id'],
#         'message': '123',
#         'channel_id': channel2['channel_id'],
#         'dm_id': -1
#     }).status_code == 400

def test_message_senddm(clear, register_info, register_info2, dm_info, dm_message_id):
    '''
    Basic test for functionality of message/senddm/v2
    '''
    messages = requests.get(f"{url}/dm/messages/v1?token={register_info['token']}&dm_id={dm_info['dm_id']}&start=0")
    messages = messages.json()
    assert messages['messages'][0]['message'] == 'Hello'
def test_message_senddm_input_error(clear, register_info, register_info2, dm_info):
    '''
    Tests for when message is over 1000 characters
    '''
    assert requests.post(f"{url}/message/senddm/v1", json={
        'token': register_info['token'],
        'dm_id': dm_info['dm_id'],
        'message': 'Hello' * 500
    }).status_code == 400
def test_message_senddm_access_error(clear, register_info, register_info2, dm_info):
    '''
    Tests for when user is not part of the dm
    '''
    register_info3 = requests.post(f"{url}/auth/register/v2", json={
        'email': 'jeremy@gmail.com',
        'password': '12345678',
        'name_first': 'Jeremy',
        'name_last': 'Lee'
    })
    register_info3 = register_info3.json()
    assert requests.post(f"{url}/message/senddm/v1", json={
        'token': register_info3['token'],
        'dm_id': dm_info['dm_id'],
        'message': 'Hello'
    }).status_code == 403
def test_message_senddm_invalid_token(clear, register_info, register_info2, dm_info):
    '''
    Tests for invalid token
    '''
    assert requests.post(f"{url}/message/senddm/v1", json={
        'token': 1,
        'dm_id': dm_info['dm_id'],
        'message': 'Hello'
    }).status_code == 400

def test_message_sendlater(clear, register_info, channel, timestamp):
    requests.post(f"{url}/message/sendlater/v1", json={
        'token': register_info['token'],
        'channel_id': channel['channel_id'],
        'message': 'Goodbye',
        'time_sent': timestamp
    })
    time.sleep(3)
    messages = requests.get(f"{url}/channel/messages/v2?token={register_info['token']}&channel_id={channel['channel_id']}&start=0")
    messages = messages.json()
    assert messages['messages'][0]['message'] == 'Goodbye'
def test_message_sendlater_invalid_channel(clear, register_info, channel, timestamp):
    assert requests.post(f"{url}/message/sendlater/v1", json={
        'token': register_info['token'],
        'channel_id': 4,
        'message': 'Goodbye',
        'time_sent': timestamp
    }).status_code == 400
def test_message_sendlater_invalid_message(clear, register_info, channel, timestamp):
    assert requests.post(f"{url}/message/sendlater/v1", json={
        'token': register_info['token'],
        'channel_id': channel['channel_id'],
        'message': 'Goodbye' * 1000,
        'time_sent': timestamp
    }).status_code == 400
def test_message_sendlater_past_time(clear, register_info, channel, timestamp, past_time):
    assert requests.post(f"{url}/message/sendlater/v1", json={
        'token': register_info['token'],
        'channel_id': channel['channel_id'],
        'message': 'Goodbye',
        'time_sent': past_time
    }).status_code == 400
def test_message_sendlater_access_error(clear, register_info, register_info2, channel, timestamp):
    assert requests.post(f"{url}/message/sendlater/v1", json={
        'token': register_info2['token'],
        'channel_id': channel['channel_id'],
        'message': 'Goodbye',
        'time_sent': timestamp
    }).status_code == 403
def test_message_sendlater_invalid_token(clear, register_info, channel, timestamp):
    assert requests.post(f"{url}/message/sendlater/v1", json={
        'token': 6,
        'channel_id': channel['channel_id'],
        'message': 'Goodbye',
        'time_sent': timestamp
    }).status_code == 400


def test_message_sendlaterdm(clear, register_info, register_info2, dm_info, timestamp):
    requests.post(f"{url}/message/sendlaterdm/v1", json={
        'token': register_info['token'],
        'dm_id': dm_info['dm_id'],
        'message': 'Goodbye',
        'time_sent': timestamp
    })
    time.sleep(3)
    dm_messages = requests.get(f"{url}/dm/messages/v1?token={register_info['token']}&dm_id={dm_info['dm_id']}&start=0")
    dm_messages = dm_messages.json()
    assert dm_messages['messages'][0]['message'] == 'Goodbye'
def test_message_sendlaterdm_invalid_dm(clear, register_info, register_info2, dm_info, timestamp):
    assert requests.post(f"{url}/message/sendlaterdm/v1", json={
        'token': register_info['token'],
        'dm_id': 7,
        'message': 'Goodbye',
        'time_sent': timestamp
    }).status_code == 400
def test_message_sendlaterdm_invalid_message(clear, register_info, register_info2, dm_info, timestamp):
    assert requests.post(f"{url}/message/sendlaterdm/v1", json={
        'token': register_info['token'],
        'dm_id': dm_info['dm_id'],
        'message': 'Goodbye' * 1000,
        'time_sent': timestamp
    }).status_code == 400
def test_message_sendlaterdm_past_time(clear, register_info, register_info2, dm_info, past_time):
    assert requests.post(f"{url}/message/sendlaterdm/v1", json={
        'token': register_info['token'],
        'dm_id': dm_info['dm_id'],
        'message': 'Goodbye',
        'time_sent': past_time
    }).status_code == 400
def test_message_sendlaterdm_access_error(clear, register_info, register_info2, register_info3, dm_info, timestamp):
    assert requests.post(f"{url}/message/sendlaterdm/v1", json={
        'token': register_info3['token'],
        'dm_id': dm_info['dm_id'],
        'message': 'Goodbye',
        'time_sent': timestamp
    }).status_code == 403
def test_message_sendlaterdm_invalid_token(clear, register_info, register_info2, dm_info, timestamp):
    assert requests.post(f"{url}/message/sendlaterdm/v1", json={
        'token': 7,
        'dm_id': dm_info['dm_id'],
        'message': 'Goodbye',
        'time_sent': timestamp
    }).status_code == 400


def test_message_react_channel(clear, register_info, channel, message_id):
    requests.post(f"{url}/message/react/v1", json={
        'token': register_info['token'],
        'message_id': message_id['message_id'],
        'react_id': 1
    })
    messages = requests.get(f"{url}/channel/messages/v2?token={register_info['token']}&channel_id={channel['channel_id']}&start=0")
    messages = messages.json()
    assert messages['messages'][0]['reacts'][0]['react_id'] == 1
    assert register_info['auth_user_id'] in messages['messages'][0]['reacts'][0]['u_ids']
def test_message_react_dm(clear, register_info, register_info2, dm_info, dm_message_id):
    requests.post(f"{url}/message/react/v1", json={
        'token': register_info['token'],
        'message_id': dm_message_id['message_id'],
        'react_id': 1
    })
    dm_messages = requests.get(f"{url}/dm/messages/v1?token={register_info['token']}&dm_id={dm_info['dm_id']}&start=0")
    dm_messages = dm_messages.json()
    assert dm_messages['messages'][0]['reacts'][0]['react_id'] == 1
    assert register_info['auth_user_id'] in dm_messages['messages'][0]['reacts'][0]['u_ids'] 
def test_message_react_invalid_message_id(clear, register_info, channel, message_id):
    assert requests.post(f"{url}/message/react/v1", json={
        'token': register_info['token'],
        'message_id': 5,
        'react_id': 1
    }).status_code == 400
def test_message_react_invalid_react_id(clear, register_info, channel, message_id):
    assert requests.post(f"{url}/message/react/v1", json={
        'token': register_info['token'],
        'message_id': message_id['message_id'],
        'react_id': 10
    }).status_code == 400
def test_message_react_already_reacted(clear, register_info, channel, message_id):
    requests.post(f"{url}/message/react/v1", json={
        'token': register_info['token'],
        'message_id': message_id['message_id'],
        'react_id': 1
    })
    assert requests.post(f"{url}/message/react/v1", json={
        'token': register_info['token'],
        'message_id': message_id['message_id'],
        'react_id': 1
    }).status_code == 400
def test_message_react_access_error(clear, register_info, register_info2, channel, message_id):
    assert requests.post(f"{url}/message/react/v1", json={
        'token': register_info2['token'],
        'message_id': message_id['message_id'],
        'react_id': 1
    }).status_code == 403
def test_message_react_invalid_token(clear, register_info, channel, message_id):
    assert requests.post(f"{url}/message/react/v1", json={
        'token': 10,
        'message_id': message_id['message_id'],
        'react_id': 1
    }).status_code == 400


def test_message_unreact_channel(clear, register_info, channel, message_id):
    requests.post(f"{url}/message/react/v1", json={
        'token': register_info['token'],
        'message_id': message_id['message_id'],
        'react_id': 1
    })
    requests.post(f"{url}/message/unreact/v1", json={
        'token': register_info['token'],
        'message_id': message_id['message_id'],
        'react_id': 1
    })
    messages = requests.get(f"{url}/channel/messages/v2?token={register_info['token']}&channel_id={channel['channel_id']}&start=0")
    messages = messages.json()
    assert messages['messages'][0]['reacts'][0]['react_id'] == 1
    assert messages['messages'][0]['reacts'][0]['u_ids'] == []
    assert messages['messages'][0]['reacts'][0]['is_this_user_reacted'] == False
def test_message_unreact_dm(clear, register_info, register_info2, dm_info, dm_message_id):
    requests.post(f"{url}/message/react/v1", json={
        'token': register_info['token'],
        'message_id': dm_message_id['message_id'],
        'react_id': 1
    })
    requests.post(f"{url}/message/unreact/v1", json={
        'token': register_info['token'],
        'message_id': dm_message_id['message_id'],
        'react_id': 1
    })
    dm_messages = requests.get(f"{url}/dm/messages/v1?token={register_info['token']}&dm_id={dm_info['dm_id']}&start=0")
    dm_messages = dm_messages.json()
    assert dm_messages['messages'][0]['reacts'][0]['react_id'] == 1
    assert dm_messages['messages'][0]['reacts'][0]['u_ids'] == []
    assert dm_messages['messages'][0]['reacts'][0]['is_this_user_reacted'] == False
def test_message_unreact_invalid_message_id(clear, register_info, channel, message_id):
    requests.post(f"{url}/message/react/v1", json={
        'token': register_info['token'],
        'message_id': message_id['message_id'],
        'react_id': 1
    })
    assert requests.post(f"{url}/message/unreact/v1", json={
        'token': register_info['token'],
        'message_id': 10,
        'react_id': 1
    }).status_code == 400
def test_message_unreact_invalid_react_id(clear, register_info, channel, message_id):
    requests.post(f"{url}/message/react/v1", json={
        'token': register_info['token'],
        'message_id': message_id['message_id'],
        'react_id': 1
    })
    assert requests.post(f"{url}/message/unreact/v1", json={
        'token': register_info['token'],
        'message_id': message_id['message_id'],
        'react_id': 10
    }).status_code == 400
def test_message_unreact_already_unreacted(clear, register_info, channel, message_id):
    assert requests.post(f"{url}/message/unreact/v1", json={
        'token': register_info['token'],
        'message_id': message_id['message_id'],
        'react_id': 1
    }).status_code == 400
def test_message_unreact_access_error(clear, register_info, register_info2, channel, message_id):
    requests.post(f"{url}/message/react/v1", json={
        'token': register_info['token'],
        'message_id': message_id['message_id'],
        'react_id': 1
    })
    assert requests.post(f"{url}/message/unreact/v1", json={
        'token': register_info2['token'],
        'message_id': message_id['message_id'],
        'react_id': 1
    }).status_code == 403
def test_message_unreact_invalid_token(clear, register_info, channel, message_id):
    requests.post(f"{url}/message/react/v1", json={
        'token': register_info['token'],
        'message_id': message_id['message_id'],
        'react_id': 1
    })
    assert requests.post(f"{url}/message/unreact/v1", json={
        'token': 10,
        'message_id': message_id['message_id'],
        'react_id': 1
    }).status_code == 400


def test_message_pin_channel(clear, register_info, channel, message_id):
    requests.post(f"{url}/message/pin/v1", json={
        'token': register_info['token'],
        'message_id': message_id['message_id']
    })
    messages = requests.get(f"{url}/channel/messages/v2?token={register_info['token']}&channel_id={channel['channel_id']}&start=0")
    messages = messages.json()
    assert messages['messages'][0]['is_pinned'] == True
def test_message_pin_dm(clear, register_info, register_info2, dm_info, dm_message_id):
    requests.post(f"{url}/message/pin/v1", json={
        'token': register_info['token'],
        'message_id': dm_message_id['message_id']
    })
    dm_messages = requests.get(f"{url}/dm/messages/v1?token={register_info['token']}&dm_id={dm_info['dm_id']}&start=0")
    dm_messages = dm_messages.json()
    assert dm_messages['messages'][0]['is_pinned'] == True
def test_message_pin_invalid_message_id(clear, register_info, channel, message_id):
    assert requests.post(f"{url}/message/pin/v1", json={
        'token': register_info['token'],
        'message_id': 10
    }).status_code == 400
def test_message_pin_already_pinned(clear, register_info, channel, message_id):
    requests.post(f"{url}/message/pin/v1", json={
        'token': register_info['token'],
        'message_id': message_id['message_id']
    })
    assert requests.post(f"{url}/message/pin/v1", json={
        'token': register_info['token'],
        'message_id': message_id['message_id']
    }).status_code == 400
def test_message_pin_access_error(clear, register_info, register_info2, channel, join, message_id):
    assert requests.post(f"{url}/message/pin/v1", json={
        'token': register_info2['token'],
        'message_id': message_id['message_id']
    }).status_code == 403
def test_message_pin_invalid_token(clear, register_info, channel, message_id):
    assert requests.post(f"{url}/message/pin/v1", json={
        'token': 10,
        'message_id': message_id['message_id']
    }).status_code == 400


def test_message_unpin_channel(clear, register_info, channel, message_id):
    requests.post(f"{url}/message/pin/v1", json={
        'token': register_info['token'],
        'message_id': message_id['message_id']
    })
    requests.post(f"{url}/message/unpin/v1", json={
        'token':register_info['token'],
        'message_id': message_id['message_id']
    })
    messages = requests.get(f"{url}/channel/messages/v2?token={register_info['token']}&channel_id={channel['channel_id']}&start=0")
    messages = messages.json()
    assert messages['messages'][0]['is_pinned'] == False
def test_message_unpin_dm(clear, register_info, register_info2, dm_info, dm_message_id):
    requests.post(f"{url}/message/pin/v1", json={
        'token': register_info['token'],
        'message_id': dm_message_id['message_id']
    })
    requests.post(f"{url}/message/unpin/v1", json={
        'token':register_info['token'],
        'message_id': dm_message_id['message_id']
    })
    dm_messages = requests.get(f"{url}/dm/messages/v1?token={register_info['token']}&dm_id={dm_info['dm_id']}&start=0")
    dm_messages = dm_messages.json()
    assert dm_messages['messages'][0]['is_pinned'] == False
def test_message_unpin_invalid_message_id(clear, register_info, channel, message_id):
    requests.post(f"{url}/message/pin/v1", json={
        'token': register_info['token'],
        'message_id': message_id['message_id']
    })
    assert requests.post(f"{url}/message/unpin/v1", json={
        'token':register_info['token'],
        'message_id': 10
    }).status_code == 400
def test_message_already_unpinned(clear, register_info, channel, message_id):
    requests.post(f"{url}/message/pin/v1", json={
        'token': register_info['token'],
        'message_id': message_id['message_id']
    })
    requests.post(f"{url}/message/unpin/v1", json={
        'token':register_info['token'],
        'message_id': message_id['message_id']
    })
    assert requests.post(f"{url}/message/unpin/v1", json={
        'token':register_info['token'],
        'message_id': message_id['message_id']
    }).status_code == 400
def test_message_unpin_access_error(clear, register_info, register_info2, channel, join, message_id):
    requests.post(f"{url}/message/pin/v1", json={
        'token': register_info['token'],
        'message_id': message_id['message_id']
    })
    assert requests.post(f"{url}/message/unpin/v1", json={
        'token':register_info2['token'],
        'message_id': message_id['message_id']
    }).status_code == 403
def test_message_unpin_invalid_token(clear, register_info, channel, message_id):
    requests.post(f"{url}/message/pin/v1", json={
        'token': register_info['token'],
        'message_id': message_id['message_id']
    })
    assert requests.post(f"{url}/message/unpin/v1", json={
        'token': 10,
        'message_id': message_id['message_id']
    }).status_code == 400