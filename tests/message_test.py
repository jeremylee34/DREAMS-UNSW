import pytest

from src.auth import auth_register_v1
from src.other import clear_v1
from src.channel import channel_messages_v1
from src.channel import channel_join_v1
from src.channels import channels_create_v1
from src.message import message_send_v1
from src.message import message_edit_v1
from src.message import message_remove_v1
from src.error import InputError
from src.error import AccessError


@pytest.fixture
def clear_data():
    clear_v1()
# Tests for message_send_v1
def test_message_send(clear_data):
    token = auth_register_v1("gordonl@gmail.com", "1234567", "Gordon", "Liang")
    channel_id = channels_create_v1(token['token'], "Channel1", True)
    message_id = message_send_v1(token['token'], channel_id['channel_id'], 'Hello')
    messages = channel_messages_v1(token['token'], channel_id['channel_id'], message_id['message_id'])
    assert messages['messages'][0]['message'] == 'Hello'
def test_message_send_input_error(clear_data):
    token = auth_register_v1("gordonl@gmail.com", "1234567", "Gordon", "Liang")
    channel_id = channels_create_v1(token['token'], "Channel1", True)
    with pytest.raises(InputError):
        assert message_send_v1(token['token'], channel_id['channel_id'], 'HelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHelloHello')
def test_message_send_access_error(clear_data):
    token = auth_register_v1("gordonl@gmail.com", "1234567", "Gordon", "Liang")
    token2 = auth_register_v1("roland@gmail.com", "1234567", "Roland", "Lin")
    channel_id = channels_create_v1(token['token'], "Channel1", True)
    with pytest.raises(AccessError):
        assert message_send_v1(token2['token'], channel_id['channel_id'], 'Hello')
# Tests for message_edit_v1
def test_message_edit(clear_data):
    token = auth_register_v1("gordonl@gmail.com", "1234567", "Gordon", "Liang")
    channel_id = channels_create_v1(token['token'], "Channel1", True)
    message_id = message_send_v1(token['token'], channel_id['channel_id'], 'Hello')
    message_edit_v1(token['token'], message_id['message_id'], 'Goodbye')
    messages = channel_messages_v1(token['token'], channel_id['channel_id'], message_id['message_id'])
    assert messages['messages'][0]['message'] == 'Goodbye'
def test_message_edit_input_error(clear_data):
    token = auth_register_v1("gordonl@gmail.com", "1234567", "Gordon", "Liang")
    channel_id = channels_create_v1(token['token'], "Channel1", True)
    message_id = message_send_v1(token['token'], channel_id['channel_id'], 'Hello')
    with pytest.raises(InputError):
        assert message_edit_v1(token['token'], message_id['message_id'], 'GoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbyeGoodbye')
def test_message_edit_input_error2(clear_data):
    token = auth_register_v1("gordonl@gmail.com", "1234567", "Gordon", "Liang")
    channel_id = channels_create_v1(token['token'], "Channel1", True)
    message_id = message_send_v1(token['token'], channel_id['channel_id'], 'Hello')
    message_remove_v1(token['token'], message_id)
    with pytest.raises(InputError):
        assert message_edit_v1(token['token'], message_id['message_id'], 'Goodbye')
def test_message_edit_access_error(clear_data):
    user = auth_register_v1("gordonl@gmail.com", "1234567", "Gordon", "Liang")
    user2 = auth_register_v1("roland@gmail.com", "1234567", "Roland", "Lin")
    channel = channels_create_v1(user['token'], "Channel1", True)
    channel_join_v1(user2['token'], channel['channel_id'])
    message = message_send_v1(user['token'], channel['channel_id'], 'Hello')
    with pytest.raises(AccessError):
        assert message_edit_v1(user2['token'], message['message_id'], 'Goodbye')
# Tests for message_remove_v1
def test_message_remove(clear_data):
    token = auth_register_v1("gordonl@gmail.com", "1234567", "Gordon", "Liang")
    channel_id = channels_create_v1(token['token'], "Channel1", True)
    message_id = message_send_v1(token['token'], channel_id['channel_id'], 'Hello')
    message_remove_v1(token['token'], message_id['message_id'])
    messages = channel_messages_v1(token['token'], channel_id['channel_id'], message_id['message_id'])
    assert messages['messages'][0] is None
def test_message_remove_input_error(clear_data):
    token = auth_register_v1("gordonl@gmail.com", "1234567", "Gordon", "Liang")
    channel_id = channels_create_v1(token['token'], "Channel1", True)
    message_id = message_send_v1(token['token'], channel_id['channel_id'], 'Hello')
    message_remove_v1(token['token'], message_id['message_id'])
    with pytest.raises(InputError):
        assert message_remove_v1(token['token'], message_id['message_id'])
def test_message_remove_access_error(clear_data):
    user = auth_register_v1("gordonl@gmail.com", "1234567", "Gordon", "Liang")
    user2 = auth_register_v1("roland@gmail.com", "1234567", "Roland", "Lin")
    channel = channels_create_v1(user['token'], "Channel1", True)
    channel_join_v1(user2['token'], channel['channel_id'])
    message = message_send_v1(user['token'], channel['channel_id'], 'Hello')
    with pytest.raises(AccessError):
        assert message_remove_v1(user2['token'], message['message_id'])
# Tests for message_share_v1
def test_message_share_channel(clear_data):
    token = auth_register_v1("gordonl@gmail.com", "1234567", "Gordon", "Liang")
    channel_id = channels_create_v1(token['token'], "Channel1", True)
    channel_id2 = channels_create_v1(token['token'], "Channel2", True)
    message_id = message_send_v1(token['token'], channel_id['channel_id'], 'Hello')
    shared_message = message_share_v1(token['token'], message_id['message_id'], channel_id2['channel_id'], -1)
    messages = channel_messages_v1(token['token'], channel_id2['channel_id'], shared_message['shared_message_id'])
    assert messages['messages'][0]['message'] == 'Hello'
def test_message_share_access_error(clear_data):
    token = auth_register_v1("gordonl@gmail.com", "1234567", "Gordon", "Liang")
    token2 = auth_register_v1("roland@gmail.com", "1234567", "Roland", "Lin")
    channel_id = channels_create_v1(token['token'], "Channel1", True)
    channel_id2 = channels_create_v1(token2['token'], "Channel2", True)
    message_id = message_send_v1(token['token'], channel_id['channel_id'], 'Hello')
    with pytest.raises(AccessError):
        assert message_share_v1(token['token'], message_id['message_id'], channel_id2['channel_id'], -1)
def test_message_share_dm(clear_data):
    token = auth_register_v1("gordonl@gmail.com", "1234567", "Gordon", "Liang")
    token2 = auth_register_v1("roland@gmail.com", "1234567", "Roland", "Lin")
    dms = dm_create_v1(token['token'], [token2['auth_user_id']])
    channel_id = channels_create_v1(token['token'], "Channel1", True)
    message_id = message_send_v1(token['token'], channel_id['channel_id'], 'Hello')
    shared_message = message_share_v1(token['token'], message_id['message_id'], -1, dms['dm_id'])
    messages = dm_messages_v1(token['token'], dms['dm_id'], shared_message['shared_message_id'])
    assert messages['messages'][0]['message'] == 'Hello'

