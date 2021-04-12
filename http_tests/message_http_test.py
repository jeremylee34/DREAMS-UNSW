'''
Http tests for message functions
Written by Gordon Liang
'''
import pytest
import requests
from src.config import url

@pytest.fixture
def clear():
    '''
    Clears data in data file
    '''
    requests.delete(f"{url}/clear/v1")
def test_message_send(clear):
    '''
    Basic test for functionality of message/send/v2
    '''
    register_info = requests.post(f"{url}/auth/register/v2", json={
        'email': 'gordon@gmail.com',
        'password': '12345678',
        'name_first': 'Gordon',
        'name_last': 'Liang'
    })
    register_info = register_info.json()
    channel = requests.post(f"{url}/channels/create/v2", json={
        'token': register_info['token'],
        'name': 'Channel1',
        'is_public': True
    })
    channel = channel.json()
    requests.post(f"{url}/message/send/v2", json={
        'token': register_info['token'],
        'channel_id': channel['channel_id'],
        'message': 'Hello'
    })
    messages = requests.get(f"{url}/channel/messages/v2?token={register_info['token']}&channel_id={channel['channel_id']}&start=0")
    messages = messages.json()
    assert messages['messages'][0]['message'] == 'Hello'
def test_message_send_input_error(clear):
    '''
    Tests for when message is over 1000 characters
    '''
    register_info = requests.post(f"{url}/auth/register/v2", json={
        'email': 'gordon@gmail.com',
        'password': '12345678',
        'name_first': 'Gordon',
        'name_last': 'Liang'
    })
    register_info = register_info.json()
    channel = requests.post(f"{url}/channels/create/v2", json={
        'token': register_info['token'],
        'name': 'Channel1',
        'is_public': True
    })
    channel = channel.json()
    assert requests.post(f"{url}/message/send/v2", json={
        'token': register_info['token'],
        'channel_id': channel['channel_id'],
        'message': 'Hello' * 500
    }).status_code == 400
def test_message_send_input_error2(clear):
    '''
    Tests for when no message is put in
    '''
    register_info = requests.post(f"{url}/auth/register/v2", json={
        'email': 'gordon@gmail.com',
        'password': '12345678',
        'name_first': 'Gordon',
        'name_last': 'Liang'
    })
    register_info = register_info.json()
    channel = requests.post(f"{url}/channels/create/v2", json={
        'token': register_info['token'],
        'name': 'Channel1',
        'is_public': True
    })
    channel = channel.json()
    assert requests.post(f"{url}/message/send/v2", json={
        'token': register_info['token'],
        'channel_id': channel['channel_id'],
        'message': ''
    }).status_code == 400
def test_message_send_access_error(clear):
    '''
    Tests for when a user hasn't joined the channel and tries to send message
    '''
    register_info = requests.post(f"{url}/auth/register/v2", json={
        'email': 'gordon@gmail.com',
        'password': '12345678',
        'name_first': 'Gordon',
        'name_last': 'Liang'
    })
    register_info = register_info.json()
    register_info2 = requests.post(f"{url}/auth/register/v2", json={
        'email': 'roland@gmail.com',
        'password': '12345678',
        'name_first': 'Roland',
        'name_last': 'Lin'
    })
    register_info2 = register_info2.json()
    channel = requests.post(f"{url}/channels/create/v2", json={
        'token': register_info2['token'],
        'name': 'Channel1',
        'is_public': True
    })
    channel = channel.json()
    assert requests.post(f"{url}/message/send/v2", json={
        'token': register_info['token'],
        'channel_id': channel['channel_id'],
        'message': 'Hello'
    }).status_code == 403
def test_message_send_invalid_token(clear):
    '''
    Tests for invalid token
    '''
    register_info = requests.post(f"{url}/auth/register/v2", json={
        'email': 'gordon@gmail.com',
        'password': '12345678',
        'name_first': 'Gordon',
        'name_last': 'Liang'
    })
    register_info = register_info.json()
    channel = requests.post(f"{url}/channels/create/v2", json={
        'token': register_info['token'],
        'name': 'Channel1',
        'is_public': True
    })
    channel = channel.json()
    assert requests.post(f"{url}/message/send/v2", json={
        'token': 4,
        'channel_id': channel['channel_id'],
        'message': 'Hello'
    }).status_code == 400

def test_message_edit(clear):
    '''
    Basic test for functionality of message/edit/v2
    '''
    register_info = requests.post(f"{url}/auth/register/v2", json={
        'email': 'gordon@gmail.com',
        'password': '12345678',
        'name_first': 'Gordon',
        'name_last': 'Liang'
    })
    register_info = register_info.json()
    channel = requests.post(f"{url}/channels/create/v2", json={
        'token': register_info['token'],
        'name': 'Channel1',
        'is_public': True
    })
    channel = channel.json()
    message_id = requests.post(f"{url}/message/send/v2", json={
        'token': register_info['token'],
        'channel_id': channel['channel_id'],
        'message': 'Hello'
    })
    message_id = message_id.json()
    print(message_id)
    requests.put(f"{url}/message/edit/v2", json={
        'token': register_info['token'],
        'message_id': message_id['message_id'],
        'message': '123'
    })
    messages = requests.get(f"{url}/channel/messages/v2?token={register_info['token']}&channel_id={channel['channel_id']}&start=0")
    messages = messages.json()
    assert messages['messages'][0]['message'] == '123'
def test_message_edit_input_error(clear):
    '''
    Tests for when message is more than 1000 characters
    '''
    register_info = requests.post(f"{url}/auth/register/v2", json={
        'email': 'gordon@gmail.com',
        'password': '12345678',
        'name_first': 'Gordon',
        'name_last': 'Liang'
    })
    register_info = register_info.json()
    channel = requests.post(f"{url}/channels/create/v2", json={
        'token': register_info['token'],
        'name': 'Channel1',
        'is_public': True
    })
    channel = channel.json()
    message_id = requests.post(f"{url}/message/send/v2", json={
        'token': register_info['token'],
        'channel_id': channel['channel_id'],
        'message': 'Hello'
    })
    message_id = message_id.json()
    assert requests.put(f"{url}/message/edit/v2", json={
        'token': register_info['token'],
        'message_id': message_id['message_id'],
        'message': '123' * 1000
    }).status_code == 400
def test_message_edit_input_error2(clear):
    '''
    Tests for when a message has already been deleted
    '''
    register_info = requests.post(f"{url}/auth/register/v2", json={
        'email': 'gordon@gmail.com',
        'password': '12345678',
        'name_first': 'Gordon',
        'name_last': 'Liang'
    })
    register_info = register_info.json()
    channel = requests.post(f"{url}/channels/create/v2", json={
        'token': register_info['token'],
        'name': 'Channel1',
        'is_public': True
    })
    channel = channel.json()
    message_id = requests.post(f"{url}/message/send/v2", json={
        'token': register_info['token'],
        'channel_id': channel['channel_id'],
        'message': 'Hello'
    })
    message_id = message_id.json()
    requests.delete(f"{url}/message/remove/v1", json={
        'token': register_info['token'],
        'message_id': message_id['message_id']
    })
    assert requests.put(f"{url}/message/edit/v2", json={
        'token': register_info['token'],
        'message_id': message_id['message_id'],
        'message': '123'
    }).status_code == 400
def test_message_edit_access_error(clear):
    '''
    Tests for when the message was not sent by user and user is not an owner
    '''
    register_info = requests.post(f"{url}/auth/register/v2", json={
        'email': 'gordon@gmail.com',
        'password': '12345678',
        'name_first': 'Gordon',
        'name_last': 'Liang'
    })
    register_info = register_info.json()
    register_info2 = requests.post(f"{url}/auth/register/v2", json={
        'email': 'roland@gmail.com',
        'password': '12345678',
        'name_first': 'Roland',
        'name_last': 'Lin'
    })
    register_info2 = register_info2.json()
    channel = requests.post(f"{url}/channels/create/v2", json={
        'token': register_info['token'],
        'name': 'Channel1',
        'is_public': True
    })
    channel = channel.json()
    requests.post(f"{url}/channel/join/v2", json={
        'token': register_info2['token'],
        'channel_id': channel['channel_id']
    })
    message_id = requests.post(f"{url}/message/send/v2", json={
        'token': register_info['token'],
        'channel_id': channel['channel_id'],
        'message': 'Hello'
    })
    message_id = message_id.json()
    assert requests.put(f"{url}/message/edit/v2", json={
        'token': register_info2['token'],
        'message_id': message_id['message_id'],
        'message': '1'
    }).status_code == 403
def test_edit_message_no_error(clear):
    '''
    Checks to see if regular member can edit their message
    '''
    register_info = requests.post(f"{url}/auth/register/v2", json={
        'email': 'gordon@gmail.com',
        'password': '12345678',
        'name_first': 'Gordon',
        'name_last': 'Liang'
    })
    register_info = register_info.json()
    register_info2 = requests.post(f"{url}/auth/register/v2", json={
        'email': 'roland@gmail.com',
        'password': '12345678',
        'name_first': 'Roland',
        'name_last': 'Lin'
    })
    register_info2 = register_info2.json()
    channel = requests.post(f"{url}/channels/create/v2", json={
        'token': register_info['token'],
        'name': 'Channel1',
        'is_public': True
    })
    channel = channel.json()
    requests.post(f"{url}/channel/join/v2", json={
        'token': register_info2['token'],
        'channel_id': channel['channel_id']
    })
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

def test_message_remove(clear):
    '''
    Basic test for message/remove/v2
    '''
    register_info = requests.post(f"{url}/auth/register/v2", json={
        'email': 'gordon@gmail.com',
        'password': '12345678',
        'name_first': 'Gordon',
        'name_last': 'Liang'
    })
    register_info = register_info.json()
    channel = requests.post(f"{url}/channels/create/v2", json={
        'token': register_info['token'],
        'name': 'Channel1',
        'is_public': True
    })
    channel = channel.json()
    message_id = requests.post(f"{url}/message/send/v2", json={
        'token': register_info['token'],
        'channel_id': channel['channel_id'],
        'message': 'Hello'
    })
    message_id = message_id.json()
    requests.delete(f"{url}/message/remove/v1", json={
        'token': register_info['token'],
        'message_id': message_id['message_id']
    })
    messages = requests.get(f"{url}/channel/messages/v2?token={register_info['token']}&channel_id={channel['channel_id']}&start=0")
    messages = messages.json()
    assert messages['messages'][0]['message'] == ''
def test_message_remove_input_error(clear):
    '''
    Tests for when message has already been removed
    '''
    register_info = requests.post(f"{url}/auth/register/v2", json={
        'email': 'gordon@gmail.com',
        'password': '12345678',
        'name_first': 'Gordon',
        'name_last': 'Liang'
    })
    register_info = register_info.json()
    channel = requests.post(f"{url}/channels/create/v2", json={
        'token': register_info['token'],
        'name': 'Channel1',
        'is_public': True
    })
    channel = channel.json()
    message_id = requests.post(f"{url}/message/send/v2", json={
        'token': register_info['token'],
        'channel_id': channel['channel_id'],
        'message': 'Hello'
    })
    message_id = message_id.json()
    requests.delete(f"{url}/message/remove/v1", json={
        'token': register_info['token'],
        'message_id': message_id['message_id']
    })
    assert requests.delete(f"{url}/message/remove/v1", json={
        'token': register_info['token'],
        'message_id': message_id['message_id']
    }).status_code == 400
def test_message_remove_access_error(clear):
    '''
    Tests for when the message was not sent by the user and user is not an owner
    '''
    register_info = requests.post(f"{url}/auth/register/v2", json={
        'email': 'gordon@gmail.com',
        'password': '12345678',
        'name_first': 'Gordon',
        'name_last': 'Liang'
    })
    register_info = register_info.json()
    register_info2 = requests.post(f"{url}/auth/register/v2", json={
        'email': 'roland@gmail.com',
        'password': '12345678',
        'name_first': 'Roland',
        'name_last': 'Lin'
    })
    register_info2 = register_info2.json()
    channel = requests.post(f"{url}/channels/create/v2", json={
        'token': register_info['token'],
        'name': 'Channel1',
        'is_public': True
    })
    channel = channel.json()
    requests.post(f"{url}/channel/join/v2", json={
        'token': register_info2['token'],
        'channel_id': channel['channel_id']
    })
    message_id = requests.post(f"{url}/message/send/v2", json={
        'token': register_info['token'],
        'channel_id': channel['channel_id'],
        'message': 'Hello'
    })
    message_id = message_id.json()
    assert requests.delete(f"{url}/message/remove/v1", json={
        'token': register_info2['token'],
        'message_id': message_id['message_id'],
    }).status_code == 403
def test_message_remove_dm(clear):
    '''
    Tests removing a message from a dm
    '''
    register_info = requests.post(f"{url}/auth/register/v2", json={
        'email': 'gordon@gmail.com',
        'password': '12345678',
        'name_first': 'Gordon',
        'name_last': 'Liang'
    })
    register_info = register_info.json()
    register_info2 = requests.post(f"{url}/auth/register/v2", json={
        'email': 'roland@gmail.com',
        'password': '12345678',
        'name_first': 'Roland',
        'name_last': 'Lin'
    })
    register_info2 = register_info2.json()
    dm_info = requests.post(f"{url}/dm/create/v1", json={
        'token': register_info['token'],
        'u_ids': [register_info2['auth_user_id']]
    })
    dm_info = dm_info.json()
    message_info = requests.post(f"{url}/message/senddm/v1", json={
        'token': register_info['token'],
        'dm_id': dm_info['dm_id'],
        'message': 'Hello'
    })
    message_info = message_info.json()
    requests.delete(f"{url}/message/remove/v1", json={
        'token': register_info['token'],
        'message_id': message_info['message_id'],
    })
    messages = requests.get(f"{url}/dm/messages/v1?token={register_info['token']}&dm_id={dm_info['dm_id']}&start=0")
    messages = messages.json()
    assert messages['messages'][0]['message'] == ''

def test_message_share(clear):
    '''
    Basic testfor message/share/v2
    '''
    register_info = requests.post(f"{url}/auth/register/v2", json={
        'email': 'gordon@gmail.com',
        'password': '12345678',
        'name_first': 'Gordon',
        'name_last': 'Liang'
    })
    register_info = register_info.json()
    channel = requests.post(f"{url}/channels/create/v2", json={
        'token': register_info['token'],
        'name': 'Channel1',
        'is_public': True
    })
    channel = channel.json()
    channel2 = requests.post(f"{url}/channels/create/v2", json={
        'token': register_info['token'],
        'name': 'Channel2',
        'is_public': True
    })
    channel2 = channel2.json()
    message_info = requests.post(f"{url}/message/send/v2", json={
        'token': register_info['token'],
        'channel_id': channel['channel_id'],
        'message': 'Hello'
    })
    message_info = message_info.json()
    requests.post(f"{url}/message/share/v1", json={
        'token': register_info['token'],
        'og_message_id': message_info['message_id'],
        'message': '123',
        'channel_id': channel2['channel_id'],
        'dm_id': -1
    })
    messages = requests.get(f"{url}/channel/messages/v2?token={register_info['token']}&channel_id={channel2['channel_id']}&start=0")
    messages = messages.json()
    assert messages['messages'][0]['message'] == 'Hello123'
def test_message_share_access_error(clear):
    '''
    Tests for when the user has not joined the channel they are sharing to
    '''
    register_info = requests.post(f"{url}/auth/register/v2", json={
        'email': 'gordon@gmail.com',
        'password': '12345678',
        'name_first': 'Gordon',
        'name_last': 'Liang'
    })
    register_info = register_info.json()
    register_info2 = requests.post(f"{url}/auth/register/v2", json={
        'email': 'roland@gmail.com',
        'password': '12345678',
        'name_first': 'Roland',
        'name_last': 'Lin'
    })
    register_info2 = register_info2.json()
    channel = requests.post(f"{url}/channels/create/v2", json={
        'token': register_info['token'],
        'name': 'Channel1',
        'is_public': True
    })
    channel = channel.json()
    channel2 = requests.post(f"{url}/channels/create/v2", json={
        'token': register_info2['token'],
        'name': 'Channel2',
        'is_public': True
    })
    channel2 = channel2.json()
    message_info = requests.post(f"{url}/message/send/v2", json={
        'token': register_info['token'],
        'channel_id': channel['channel_id'],
        'message': 'Hello'
    })
    message_info = message_info.json()
    assert requests.post(f"{url}/message/share/v1", json={
        'token': register_info['token'],
        'og_message_id': message_info['message_id'],
        'message': '123',
        'channel_id': channel2['channel_id'],
        'dm_id': -1
    }).status_code == 403
def test_message_share_invalid_token(clear):
    '''
    Tests for invalid token
    '''
    register_info = requests.post(f"{url}/auth/register/v2", json={
        'email': 'gordon@gmail.com',
        'password': '12345678',
        'name_first': 'Gordon',
        'name_last': 'Liang'
    })
    register_info = register_info.json()
    channel = requests.post(f"{url}/channels/create/v2", json={
        'token': register_info['token'],
        'name': 'Channel1',
        'is_public': True
    })
    channel = channel.json()
    channel2 = requests.post(f"{url}/channels/create/v2", json={
        'token': register_info['token'],
        'name': 'Channel2',
        'is_public': True
    })
    channel2 = channel2.json()
    message_info = requests.post(f"{url}/message/send/v2", json={
        'token': register_info['token'],
        'channel_id': channel['channel_id'],
        'message': 'Hello'
    })
    message_info = message_info.json()
    assert requests.post(f"{url}/message/share/v1", json={
        'token': 1,
        'og_message_id': message_info['message_id'],
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

def test_message_senddm(clear):
    '''
    Basic test for functionality of message/senddm/v2
    '''
    register_info = requests.post(f"{url}/auth/register/v2", json={
        'email': 'gordon@gmail.com',
        'password': '12345678',
        'name_first': 'Gordon',
        'name_last': 'Liang'
    })
    register_info = register_info.json()
    register_info2 = requests.post(f"{url}/auth/register/v2", json={
        'email': 'roland@gmail.com',
        'password': '12345678',
        'name_first': 'Roland',
        'name_last': 'Lin'
    })
    register_info2 = register_info2.json()
    dm_info = requests.post(f"{url}/dm/create/v1", json={
        'token': register_info['token'],
        'u_ids': [register_info2['auth_user_id']]
    })
    dm_info = dm_info.json()
    requests.post(f"{url}/message/senddm/v1", json={
        'token': register_info['token'],
        'dm_id': dm_info['dm_id'],
        'message': 'Hello'
    })
    messages = requests.get(f"{url}/dm/messages/v1?token={register_info['token']}&dm_id={dm_info['dm_id']}&start=0")
    messages = messages.json()
    assert messages['messages'][0]['message'] == 'Hello'
def test_message_senddm_input_error(clear):
    '''
    Tests for when message is over 1000 characters
    '''
    register_info = requests.post(f"{url}/auth/register/v2", json={
        'email': 'gordon@gmail.com',
        'password': '12345678',
        'name_first': 'Gordon',
        'name_last': 'Liang'
    })
    register_info = register_info.json()
    register_info2 = requests.post(f"{url}/auth/register/v2", json={
        'email': 'roland@gmail.com',
        'password': '12345678',
        'name_first': 'Roland',
        'name_last': 'Lin'
    })
    register_info2 = register_info2.json()
    dm_info = requests.post(f"{url}/dm/create/v1", json={
        'token': register_info['token'],
        'u_ids': [register_info2['auth_user_id']]
    })
    dm_info = dm_info.json()
    assert requests.post(f"{url}/message/senddm/v1", json={
        'token': register_info['token'],
        'dm_id': dm_info['dm_id'],
        'message': 'Hello' * 500
    }).status_code == 400
def test_message_senddm_access_error(clear):
    '''
    Tests for when user is not part of the dm
    '''
    register_info = requests.post(f"{url}/auth/register/v2", json={
        'email': 'gordon@gmail.com',
        'password': '12345678',
        'name_first': 'Gordon',
        'name_last': 'Liang'
    })
    register_info = register_info.json()
    register_info2 = requests.post(f"{url}/auth/register/v2", json={
        'email': 'roland@gmail.com',
        'password': '12345678',
        'name_first': 'Roland',
        'name_last': 'Lin'
    })
    register_info2 = register_info2.json()
    register_info3 = requests.post(f"{url}/auth/register/v2", json={
        'email': 'jeremy@gmail.com',
        'password': '12345678',
        'name_first': 'Jeremy',
        'name_last': 'Lee'
    })
    register_info3 = register_info3.json()
    dm_info = requests.post(f"{url}/dm/create/v1", json={
        'token': register_info2['token'],
        'u_ids': [register_info3['auth_user_id']]
    })
    dm_info = dm_info.json()
    assert requests.post(f"{url}/message/senddm/v1", json={
        'token': register_info['token'],
        'dm_id': dm_info['dm_id'],
        'message': 'Hello'
    }).status_code == 403
def test_message_senddm_invalid_token(clear):
    '''
    Tests for invalid token
    '''
    register_info = requests.post(f"{url}/auth/register/v2", json={
        'email': 'gordon@gmail.com',
        'password': '12345678',
        'name_first': 'Gordon',
        'name_last': 'Liang'
    })
    register_info = register_info.json()
    register_info2 = requests.post(f"{url}/auth/register/v2", json={
        'email': 'roland@gmail.com',
        'password': '12345678',
        'name_first': 'Roland',
        'name_last': 'Lin'
    })
    register_info2 = register_info2.json()
    dm_info = requests.post(f"{url}/dm/create/v1", json={
        'token': register_info['token'],
        'u_ids': [register_info2['auth_user_id']]
    })
    dm_info = dm_info.json()
    assert requests.post(f"{url}/message/senddm/v1", json={
        'token': 1,
        'dm_id': dm_info['dm_id'],
        'message': 'Hello'
    }).status_code == 400
