import pytest
import requests
from src.config import port
from src.config import url
from src.other import clear_v1
from src.error import InputError
from src.error import AccessError

@pytest.fixture
def clear():
    requests.delete(f"{url}/clear/v1")
def test_message_send(clear):
    register_info = requests.post(f"{url}/auth/register/v2", json={
        'email': 'gordon@gmail.com',
        'password': '12345678',
        'name_first': 'Gordon',
        'name_last': 'Liang'
    })
    channel = requests.post(f"{url}/channels/create/v2", json={
        'token': register_info['token'],
        'name': 'Channel1',
        'is_public': True
    })
    message_id = requests.post(f"{url}/message/send/v2", json={
        'token': register_info['token'],
        'channel_id': channel['channel_id'],
        'message': 'Hello'
    })
    messages = requests.get(f"{url}/channel/messages/v2", json={
        'token': register_info['token'],
        'channel_id': channel['channel_id'],
        'start': 0
    })
    messages = messages.json()
    assert messages['messages'][0]['message'] == 'Hello'
def test_message_send_input_error(clear):
    register_info = requests.post(f"{url}/auth/register/v2", json={
        'email': 'gordon@gmail.com',
        'password': '12345678',
        'name_first': 'Gordon',
        'name_last': 'Liang'
    })
    channel = requests.post(f"{url}/channels/create/v2", json={
        'token': register_info['token'],
        'name': 'Channel1',
        'is_public': True
    })
    assert requests.post(f"{url}/message/send/v2", json={
        'token': register_info['token'],
        'channel_id': channel['channel_id'],
        'message': 'Hello' * 500
    }).status_code == 400
def test_message_send_input_error2(clear):
    register_info = requests.post(f"{url}/auth/register/v2", json={
        'email': 'gordon@gmail.com',
        'password': '12345678',
        'name_first': 'Gordon',
        'name_last': 'Liang'
    })
    channel = requests.post(f"{url}/channels/create/v2", json={
        'token': register_info['token'],
        'name': 'Channel1',
        'is_public': True
    })
    assert requests.post(f"{url}/message/send/v2", json={
        'token': register_info['token'],
        'channel_id': channel['channel_id'],
        'message': ''
    }).status_code == 400
def test_message_send_access_error(clear):
    register_info = requests.post(f"{url}/auth/register/v2", json={
        'email': 'gordon@gmail.com',
        'password': '12345678',
        'name_first': 'Gordon',
        'name_last': 'Liang'
    })
    register_info2 = requests.post(f"{url}/auth/register/v2", json={
        'email': 'roland@gmail.com',
        'password': '12345678',
        'name_first': 'Roland',
        'name_last': 'Lin'
    })
    channel = requests.post(f"{url}/channels/create/v2", json={
        'token': register_info2['token'],
        'name': 'Channel1',
        'is_public': True
    })
    assert requests.post(f"{url}/message/send/v2", json={
        'token': register_info['token'],
        'channel_id': channel['channel_id'],
        'message': 'Hello'
    }).status_code == 403
def test_message_send_invalid_token(clear):
    register_info = requests.post(f"{url}/auth/register/v2", json={
        'email': 'gordon@gmail.com',
        'password': '12345678',
        'name_first': 'Gordon',
        'name_last': 'Liang'
    })
    channel = requests.post(f"{url}/channels/create/v2", json={
        'token': register_info['token'],
        'name': 'Channel1',
        'is_public': True
    })
    assert requests.post(f"{url}/message/send/v2", json={
        'token': 4,
        'channel_id': channel['channel_id'],
        'message': 'Hello'
    }).status_code == 403

def test_message_edit(clear):
    register_info = requests.post(f"{url}/auth/register/v2", json={
        'email': 'gordon@gmail.com',
        'password': '12345678',
        'name_first': 'Gordon',
        'name_last': 'Liang'
    })
    channel = requests.post(f"{url}/channels/create/v2", json={
        'token': register_info['token'],
        'name': 'Channel1',
        'is_public': True
    })
    message_id = requests.post(f"{url}/message/send/v2", json={
        'token': register_info['token'],
        'channel_id': channel['channel_id'],
        'message': 'Hello'
    })
    requests.put(f"{url}/message/edit/v2", json={
        'token': register_info['token'],
        'message_id': message_id['message_id'],
        'message': '123'
    })
    messages = requests.get(f"{url}/channel/messages/v2", json={
        'token': register_info['token'],
        'channel_id': channel['channel_id'],
        'start': 0
    })
    messages = messages.json()
    assert messages['messages'][0]['message'] == '123'
def test_message_edit_input_error(clear):
    register_info = requests.post(f"{url}/auth/register/v2", json={
        'email': 'gordon@gmail.com',
        'password': '12345678',
        'name_first': 'Gordon',
        'name_last': 'Liang'
    })
    channel = requests.post(f"{url}/channels/create/v2", json={
        'token': register_info['token'],
        'name': 'Channel1',
        'is_public': True
    })
    message_id = requests.post(f"{url}/message/send/v2", json={
        'token': register_info['token'],
        'channel_id': channel['channel_id'],
        'message': 'Hello'
    })
    assert requests.put(f"{url}/message/edit/v2", json={
        'token': register_info['token'],
        'message_id': message_id['message_id'],
        'message': '123' * 1000
    }).status_code == 400
def test_message_edit_input_error2(clear):
    register_info = requests.post(f"{url}/auth/register/v2", json={
        'email': 'gordon@gmail.com',
        'password': '12345678',
        'name_first': 'Gordon',
        'name_last': 'Liang'
    })
    channel = requests.post(f"{url}/channels/create/v2", json={
        'token': register_info['token'],
        'name': 'Channel1',
        'is_public': True
    })
    message_id = requests.post(f"{url}/message/send/v2", json={
        'token': register_info['token'],
        'channel_id': channel['channel_id'],
        'message': 'Hello'
    })
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
    register_info = requests.post(f"{url}/auth/register/v2", json={
        'email': 'gordon@gmail.com',
        'password': '12345678',
        'name_first': 'Gordon',
        'name_last': 'Liang'
    })
    register_info2 = requests.post(f"{url}/auth/register/v2", json={
        'email': 'roland@gmail.com',
        'password': '12345678',
        'name_first': 'Roland',
        'name_last': 'Lin'
    })
    channel = requests.post(f"{url}/channels/create/v2", json={
        'token': register_info['token'],
        'name': 'Channel1',
        'is_public': True
    })
    requests.post(f"{url}/channel/join/v2", json={
        'token': register_info2['token'],
        'channel_id': channel['channel_id']
    })
    message_id = requests.post(f"{url}/message/send/v2", json={
        'token': register_info['token'],
        'channel_id': channel['channel_id'],
        'message': 'Hello'
    })
    assert requests.put(f"{url}/message/edit/v2", json={
        'token': register_info2['token'],
        'message_id': message_id['message_id'],
        'message': '1'
    }).status_code == 403
def test_edit_message_no_error(clear):
    register_info = requests.post(f"{url}/auth/register/v2", json={
        'email': 'gordon@gmail.com',
        'password': '12345678',
        'name_first': 'Gordon',
        'name_last': 'Liang'
    })
    register_info2 = requests.post(f"{url}/auth/register/v2", json={
        'email': 'roland@gmail.com',
        'password': '12345678',
        'name_first': 'Roland',
        'name_last': 'Lin'
    })
    channel = requests.post(f"{url}/channels/create/v2", json={
        'token': register_info['token'],
        'name': 'Channel1',
        'is_public': True
    })
    requests.post(f"{url}/channel/join/v2", json={
        'token': register_info2['token'],
        'channel_id': channel['channel_id']
    })
    message_id = requests.post(f"{url}/message/send/v2", json={
        'token': register_info2['token'],
        'channel_id': channel['channel_id'],
        'message': 'Hello'
    })
    requests.put(f"{url}/message/edit/v2", json={
        'token': register_info['token'],
        'message_id': message_id['message_id'],
        'message': '123'
    })
    messages = requests.get(f"{url}/channel/messages/v2", json={
        'token': register_info['token'],
        'channel_id': channel['channel_id'],
        'start': 0
    })
    messages = messages.json()
    assert messages['messages'][0]['message'] == '123'

def test_message_remove(clear):
    register_info = requests.post(f"{url}/auth/register/v2", json={
        'email': 'gordon@gmail.com',
        'password': '12345678',
        'name_first': 'Gordon',
        'name_last': 'Liang'
    })
    channel = requests.post(f"{url}/channels/create/v2", json={
        'token': register_info['token'],
        'name': 'Channel1',
        'is_public': True
    })
    message_id = requests.post(f"{url}/message/send/v2", json={
        'token': register_info['token'],
        'channel_id': channel['channel_id'],
        'message': 'Hello'
    })
    requests.delete(f"{url}/message/remove/v1", json={
        'token': register_info['token'],
        'message_id': message_id['message_id']
    })
    messages = requests.get(f"{url}/channel/messages/v2", json={
        'token': register_info['token'],
        'channel_id': channel['channel_id'],
        'start': 0
    })
    messages = messages.json()
    assert messages['messages'][0]['message'] == ''
def test_message_remove_input_error(clear):
    register_info = requests.post(f"{url}/auth/register/v2", json={
        'email': 'gordon@gmail.com',
        'password': '12345678',
        'name_first': 'Gordon',
        'name_last': 'Liang'
    })
    channel = requests.post(f"{url}/channels/create/v2", json={
        'token': register_info['token'],
        'name': 'Channel1',
        'is_public': True
    })
    message_id = requests.post(f"{url}/message/send/v2", json={
        'token': register_info['token'],
        'channel_id': channel['channel_id'],
        'message': 'Hello'
    })
    requests.delete(f"{url}/message/remove/v1", json={
        'token': register_info['token'],
        'message_id': message_id['message_id']
    })
    assert requests.delete(f"{url}/message/remove/v1", json={
        'token': register_info['token'],
        'message_id': message_id['message_id']
    }).status_code == 400
def test_message_remove_access_error(clear):
    register_info = requests.post(f"{url}/auth/register/v2", json={
        'email': 'gordon@gmail.com',
        'password': '12345678',
        'name_first': 'Gordon',
        'name_last': 'Liang'
    })
    register_info2 = requests.post(f"{url}/auth/register/v2", json={
        'email': 'roland@gmail.com',
        'password': '12345678',
        'name_first': 'Roland',
        'name_last': 'Lin'
    })
    channel = requests.post(f"{url}/channels/create/v2", json={
        'token': register_info['token'],
        'name': 'Channel1',
        'is_public': True
    })
    requests.post(f"{url}/channel/join/v2", json={
        'token': register_info2['token'],
        'channel_id': channel['channel_id']
    })
    message_id = requests.post(f"{url}/message/send/v2", json={
        'token': register_info['token'],
        'channel_id': channel['channel_id'],
        'message': 'Hello'
    })
    assert requests.put(f"{url}/message/remove/v1", json={
        'token': register_info2['token'],
        'message_id': message_id['message_id'],
    }).status_code == 403
def test_message_remove_dm(clear):
    register_info = requests.post(f"{url}/auth/register/v2", json={
        'email': 'gordon@gmail.com',
        'password': '12345678',
        'name_first': 'Gordon',
        'name_last': 'Liang'
    })
    register_info2 = requests.post(f"{url}/auth/register/v2", json={
        'email': 'roland@gmail.com',
        'password': '12345678',
        'name_first': 'Roland',
        'name_last': 'Lin'
    })
    dm_info = requests.post(f"{url}/dm/create/v1", json={
        'token': register_info['token'],
        'u_ids': [register_info2['auth_user_id']]
    })
    message_info = requests.post(f"{url}/message/senddm/v1", json={
        'token': register_info['token'],
        'dm_id': dm_info['dm_id'],
        'message': 'Hello'
    })
    requests.put(f"{url}/message/remove/v1", json={
        'token': register_info['token'],
        'message_id': message_info['message_id'],
    })
    messages = requests.get(f"{url}/dm/messages/v1", json={
        'token': register_info['token'],
        'dm_id': dm_info['dm_id'],
        'start': 0
    })
    messages = messages.json()
    assert messages['messages'][0]['message'] == ''

def test_message_share(clear):
    register_info = requests.post(f"{url}/auth/register/v2", json={
        'email': 'gordon@gmail.com',
        'password': '12345678',
        'name_first': 'Gordon',
        'name_last': 'Liang'
    })
    channel = requests.post(f"{url}/channels/create/v2", json={
        'token': register_info['token'],
        'name': 'Channel1',
        'is_public': True
    })
    channel2 = requests.post(f"{url}/channels/create/v2", json={
        'token': register_info['token'],
        'name': 'Channel2',
        'is_public': True
    })
    message_info = requests.post(f"{url}/message/send/v2", json={
        'token': register_info['token'],
        'channel_id': channel['channel_id'],
        'message': 'Hello'
    })
    requests.post(f"{url}/message/share/v1", json={
        'token': register_info['token'],
        'og_message_id': message_info['message_id'],
        'message': '123',
        'channel_id': channel2['channel_id'],
        'dm_id': -1
    })
    messages = requests.get(f"{url}/channel/messages/v2", json={
        'token': register_info['token'],
        'channel_id': channel2['channel_id'],
        'start': 0
    })
    messages = messages.json()
    assert messages['messages'][0]['message'] == 'Hello123'
def test_message_share_access_error(clear):
    register_info = requests.post(f"{url}/auth/register/v2", json={
        'email': 'gordon@gmail.com',
        'password': '12345678',
        'name_first': 'Gordon',
        'name_last': 'Liang'
    })
    channel = requests.post(f"{url}/channels/create/v2", json={
        'token': register_info['token'],
        'name': 'Channel1',
        'is_public': True
    })
    channel2 = requests.post(f"{url}/channels/create/v2", json={
        'token': register_info['token'],
        'name': 'Channel2',
        'is_public': True
    })
    message_info = requests.post(f"{url}/message/send/v2", json={
        'token': register_info['token'],
        'channel_id': channel['channel_id'],
        'message': 'Hello'
    })
    assert requests.post(f"{url}/message/share/v1", json={
        'token': register_info['token'],
        'og_message_id': message_info['message_id'],
        'message': '123',
        'channel_id': channel2['channel_id'],
        'dm_id': -1
    }).status_code == 403
def test_message_share_invalid_token(clear):
    register_info = requests.post(f"{url}/auth/register/v2", json={
        'email': 'gordon@gmail.com',
        'password': '12345678',
        'name_first': 'Gordon',
        'name_last': 'Liang'
    })
    channel = requests.post(f"{url}/channels/create/v2", json={
        'token': register_info['token'],
        'name': 'Channel1',
        'is_public': True
    })
    channel2 = requests.post(f"{url}/channels/create/v2", json={
        'token': register_info['token'],
        'name': 'Channel2',
        'is_public': True
    })
    message_info = requests.post(f"{url}/message/send/v2", json={
        'token': register_info['token'],
        'channel_id': channel['channel_id'],
        'message': 'Hello'
    })
    assert requests.post(f"{url}/message/share/v1", json={
        'token': 1,
        'og_message_id': message_info['message_id'],
        'message': '123',
        'channel_id': channel2['channel_id'],
        'dm_id': -1
    }).status_code == 403
def test_message_share_deleted_message(clear):
    register_info = requests.post(f"{url}/auth/register/v2", json={
        'email': 'gordon@gmail.com',
        'password': '12345678',
        'name_first': 'Gordon',
        'name_last': 'Liang'
    })
    channel = requests.post(f"{url}/channels/create/v2", json={
        'token': register_info['token'],
        'name': 'Channel1',
        'is_public': True
    })
    channel2 = requests.post(f"{url}/channels/create/v2", json={
        'token': register_info['token'],
        'name': 'Channel2',
        'is_public': True
    })
    message_info = requests.post(f"{url}/message/send/v2", json={
        'token': register_info['token'],
        'channel_id': channel['channel_id'],
        'message': 'Hello'
    })
    requests.delete(f"{url}/message/remove/v1", json={
        'token': register_info['token'],
        'message_id': message_info['message_id']
    })
    assert requests.post(f"{url}/message/share/v1", json={
        'token': register_info['token'],
        'og_message_id': message_info['message_id'],
        'message': '123',
        'channel_id': channel2['channel_id'],
        'dm_id': -1
    }).status_code == 403

def test_message_senddm(clear):
    register_info = requests.post(f"{url}/auth/register/v2", json={
        'email': 'gordon@gmail.com',
        'password': '12345678',
        'name_first': 'Gordon',
        'name_last': 'Liang'
    })
    register_info2 = requests.post(f"{url}/auth/register/v2", json={
        'email': 'roland@gmail.com',
        'password': '12345678',
        'name_first': 'Roland',
        'name_last': 'Lin'
    })
    dm_info = requests.post(f"{url}/dm/create/v1", json={
        'token': register_info['token'],
        'u_ids': [register_info2['auth_user_id']]
    })
    requests.post(f"{url}/message/senddm/v1", json={
        'token': register_info['token'],
        'dm_id': dm_info['dm_id'],
        'message': 'Hello'
    })
    messages = requests.get(f"{url}/dm/messages/v1", json={
        'token': register_info['token'],
        'dm_id': dm_info['dm_id'],
        'start': 0
    })
    messages = messages.json()
    assert messages['messages'][0]['message'] == 'Hello'
def test_message_senddm_input_error(clear):
    register_info = requests.post(f"{url}/auth/register/v2", json={
        'email': 'gordon@gmail.com',
        'password': '12345678',
        'name_first': 'Gordon',
        'name_last': 'Liang'
    })
    register_info2 = requests.post(f"{url}/auth/register/v2", json={
        'email': 'roland@gmail.com',
        'password': '12345678',
        'name_first': 'Roland',
        'name_last': 'Lin'
    })
    dm_info = requests.post(f"{url}/dm/create/v1", json={
        'token': register_info['token'],
        'u_ids': [register_info2['auth_user_id']]
    })
    assert requests.post(f"{url}/message/senddm/v1", json={
        'token': register_info['token'],
        'dm_id': dm_info['dm_id'],
        'message': 'Hello' * 500
    }).status_code == 400
def test_message_senddm_access_error(clear):
    register_info = requests.post(f"{url}/auth/register/v2", json={
        'email': 'gordon@gmail.com',
        'password': '12345678',
        'name_first': 'Gordon',
        'name_last': 'Liang'
    })
    register_info2 = requests.post(f"{url}/auth/register/v2", json={
        'email': 'roland@gmail.com',
        'password': '12345678',
        'name_first': 'Roland',
        'name_last': 'Lin'
    })
    register_info3 = requests.post(f"{url}/auth/register/v2", json={
        'email': 'jeremy@gmail.com',
        'password': '12345678',
        'name_first': 'Jeremy',
        'name_last': 'Lee'
    })
    dm_info = requests.post(f"{url}/dm/create/v1", json={
        'token': register_info2['token'],
        'u_ids': [register_info3['auth_user_id']]
    })
    assert requests.post(f"{url}/message/senddm/v1", json={
        'token': register_info['token'],
        'dm_id': dm_info['dm_id'],
        'message': 'Hello'
    }).status_code == 403
def test_message_senddm_invalid_token(clear):
    register_info = requests.post(f"{url}/auth/register/v2", json={
        'email': 'gordon@gmail.com',
        'password': '12345678',
        'name_first': 'Gordon',
        'name_last': 'Liang'
    })
    register_info2 = requests.post(f"{url}/auth/register/v2", json={
        'email': 'roland@gmail.com',
        'password': '12345678',
        'name_first': 'Roland',
        'name_last': 'Lin'
    })
    dm_info = requests.post(f"{url}/dm/create/v1", json={
        'token': register_info['token'],
        'u_ids': [register_info2['auth_user_id']]
    })
    assert requests.post(f"{url}/message/senddm/v1", json={
        'token': 1,
        'dm_id': dm_info['dm_id'],
        'message': 'Hello'
    }).status_code == 403

