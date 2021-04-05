import pytest

from src.auth import auth_register_v1
from src.other import clear_v1
from src.channel import channel_messages_v1
from src.channel import channel_join_v1
from src.channels import channels_create_v1
from src.message import message_send_v1
from src.message import message_edit_v1
from src.message import message_remove_v1
from src.message import message_senddm_v1
from src.message import message_share_v1
from src.error import InputError
from src.error import AccessError
from src.dm import dm_create_v1
from src.dm import dm_messages_v1


@pytest.fixture
def clear():
    clear_v1()
# Tests for message_send_v1
def test_message_send(clear):
    '''
    Basic test for functionality of message_send_v1
    '''
    user = auth_register_v1("gordonl@gmail.com", "1234567", "Gordon", "Liang")
    channel = channels_create_v1(user['token'], "Channel1", True)
    message = message_send_v1(user['token'], channel['channel_id'], 'Hello')
    messages = channel_messages_v1(user['token'], channel['channel_id'], message['message_id'])
    assert messages['messages'][0]['message'] == 'Hello'
def test_message_send_input_error(clear):
    '''
    Testing for messages more than 1000 characters
    '''
    token = auth_register_v1("gordonl@gmail.com", "1234567", "Gordon", "Liang")
    channel_id = channels_create_v1(token['token'], "Channel1", True)
    with pytest.raises(InputError):
        assert message_send_v1(token['token'], channel_id['channel_id'], 'Hello' * 1000)
def test_message_send_access_error(clear):
    '''
    Tests if an AccessError is raised when user trying to send message has not
    joined the channel
    '''
    token = auth_register_v1("gordonl@gmail.com", "1234567", "Gordon", "Liang")
    token2 = auth_register_v1("roland@gmail.com", "1234567", "Roland", "Lin")
    channel_id = channels_create_v1(token['token'], "Channel1", True)
    with pytest.raises(AccessError):
        assert message_send_v1(token2['token'], channel_id['channel_id'], 'Hello')
def test_message_send_multiple(clear):
    '''
    Tests sending messages to multiple channels
    '''
    user = auth_register_v1("gordonl@gmail.com", "1234567", "Gordon", "Liang")
    channel = channels_create_v1(user['token'], "Channel1", True)
    channel2 = channels_create_v1(user['token'], "Channel2", True)
    message_send_v1(user['token'], channel['channel_id'], 'Hello')
    message_send_v1(user['token'], channel2['channel_id'], 'Hello123')
    messages = channel_messages_v1(user['token'], channel['channel_id'], 0)
    messages2 = channel_messages_v1(user['token'], channel2['channel_id'], 0)
    assert messages['messages'][0]['message'] == 'Hello'
    assert messages2['messages'][0]['message'] == 'Hello123'
def test_message_send_multiple_messages(clear):
    '''
    Tests sending multiple messages to a channel
    '''
    user = auth_register_v1("gordonl@gmail.com", "1234567", "Gordon", "Liang")
    channel = channels_create_v1(user['token'], "Channel1", True)
    message_send_v1(user['token'], channel['channel_id'], 'Hello')
    message_send_v1(user['token'], channel['channel_id'], 'Hello123')
    message_send_v1(user['token'], channel['channel_id'], 'Goodbye')
    message_send_v1(user['token'], channel['channel_id'], 'Goodbye123')
    messages = channel_messages_v1(user['token'], channel['channel_id'], 0)
    assert messages['messages'][3]['message'] == 'Hello'
    assert messages['messages'][2]['message'] == 'Hello123'
    assert messages['messages'][1]['message'] == 'Goodbye'
    assert messages['messages'][0]['message'] == 'Goodbye123'
def test_message_send_input_error2(clear):
    '''
    Tests for invalid token
    '''
    user = auth_register_v1("gordonl@gmail.com", "1234567", "Gordon", "Liang")
    channel = channels_create_v1(user['token'], "Channel1", True)
    with pytest.raises(InputError):
        assert message_send_v1(user['token'], channel['channel_id'], '')

# Tests for message_edit_v1
def test_message_edit(clear):
    '''
    Basic test for functionality of message_edit_v1
    '''
    token = auth_register_v1("gordonl@gmail.com", "1234567", "Gordon", "Liang")
    channel_id = channels_create_v1(token['token'], "Channel1", True)
    message_id = message_send_v1(token['token'], channel_id['channel_id'], 'Hello')
    message_edit_v1(token['token'], message_id['message_id'], 'Goodbye')
    messages = channel_messages_v1(token['token'], channel_id['channel_id'], 0)
    assert messages['messages'][0]['message'] == 'Goodbye'
def test_message_edit_input_error(clear):
    '''
    Tests for when message is over 1000 characters
    '''
    token = auth_register_v1("gordonl@gmail.com", "1234567", "Gordon", "Liang")
    channel_id = channels_create_v1(token['token'], "Channel1", True)
    message_id = message_send_v1(token['token'], channel_id['channel_id'], 'Hello')
    with pytest.raises(InputError):
        assert message_edit_v1(token['token'], message_id['message_id'], 'Goodbye' * 1000)
def test_message_edit_input_error2(clear):
    '''
    Tests if an InputError is raised when message is already deleted
    '''
    token = auth_register_v1("gordonl@gmail.com", "1234567", "Gordon", "Liang")
    channel_id = channels_create_v1(token['token'], "Channel1", True)
    message_id = message_send_v1(token['token'], channel_id['channel_id'], 'Hello')
    message_remove_v1(token['token'], message_id['message_id'])
    with pytest.raises(InputError):
        assert message_edit_v1(token['token'], message_id['message_id'], 'Goodbye')
def test_message_edit_access_error(clear):
    '''
    Tests for when user has not created the message and is not an owner
    '''
    user = auth_register_v1("gordonl@gmail.com", "1234567", "Gordon", "Liang")
    user2 = auth_register_v1("roland@gmail.com", "1234567", "Roland", "Lin")
    channel = channels_create_v1(user['token'], "Channel1", True)
    channel_join_v1(user2['token'], channel['channel_id'])
    message = message_send_v1(user['token'], channel['channel_id'], 'Hello')
    with pytest.raises(AccessError):
        assert message_edit_v1(user2['token'], message['message_id'], 'Goodbye')
# Tests for message_remove_v1
def test_message_remove(clear):
    '''
    Basic test for functionality of message_remove_v1
    '''
    token = auth_register_v1("gordonl@gmail.com", "1234567", "Gordon", "Liang")
    channel_id = channels_create_v1(token['token'], "Channel1", True)
    message_id = message_send_v1(token['token'], channel_id['channel_id'], 'Hello')
    message_remove_v1(token['token'], message_id['message_id'])
    messages = channel_messages_v1(token['token'], channel_id['channel_id'], 0)
    assert messages['messages'][0]['message'] == ''
def test_message_remove_input_error(clear):
    '''
    Tests if an InputError is raised when message is already deleted
    '''
    token = auth_register_v1("gordonl@gmail.com", "1234567", "Gordon", "Liang")
    channel_id = channels_create_v1(token['token'], "Channel1", True)
    message_id = message_send_v1(token['token'], channel_id['channel_id'], 'Hello')
    message_remove_v1(token['token'], message_id['message_id'])
    with pytest.raises(InputError):
        assert message_remove_v1(token['token'], message_id['message_id'])
def test_message_remove_access_error(clear):
    '''
    Tests for when user has not created the message and is not an owner
    '''
    user = auth_register_v1("gordonl@gmail.com", "1234567", "Gordon", "Liang")
    user2 = auth_register_v1("roland@gmail.com", "1234567", "Roland", "Lin")
    channel = channels_create_v1(user['token'], "Channel1", True)
    channel_join_v1(user2['token'], channel['channel_id'])
    message = message_send_v1(user['token'], channel['channel_id'], 'Hello')
    with pytest.raises(AccessError):
        assert message_remove_v1(user2['token'], message['message_id'])
def test_message_remove_multiple(clear):
    '''
    Tests for multiple removed messages
    '''
    user = auth_register_v1("gordonl@gmail.com", "1234567", "Gordon", "Liang")
    channel = channels_create_v1(user['token'], "Channel1", True)
    message = message_send_v1(user['token'], channel['channel_id'], 'Hello')
    message2 = message_send_v1(user['token'], channel['channel_id'], 'Hello123')
    message3 = message_send_v1(user['token'], channel['channel_id'], 'Goodbye')
    message4 = message_send_v1(user['token'], channel['channel_id'], 'Three')
    message_remove_v1(user['token'], message['message_id'])
    message_remove_v1(user['token'], message2['message_id'])
    message_remove_v1(user['token'], message3['message_id'])
    message_remove_v1(user['token'], message4['message_id'])
    messages = channel_messages_v1(user['token'], channel['channel_id'], 0)
    assert messages['messages'][0]['message'] == ''
    assert messages['messages'][1]['message'] == ''
    assert messages['messages'][2]['message'] == ''
    assert messages['messages'][3]['message'] == ''
# Tests for message_share_v1
def test_message_share_channel(clear):
    '''
    Basic test for functionality of message_share_v1
    '''
    token = auth_register_v1("gordonl@gmail.com", "1234567", "Gordon", "Liang")
    channel_id = channels_create_v1(token['token'], "Channel1", True)
    channel_id2 = channels_create_v1(token['token'], "Channel2", True)
    message_id = message_send_v1(token['token'], channel_id['channel_id'], 'Hello')
    message_share_v1(token['token'], message_id['message_id'], '', channel_id2['channel_id'], -1)
    messages = channel_messages_v1(token['token'], channel_id2['channel_id'], 0)
    assert messages['messages'][0]['message'] == 'Hello'
def test_message_share_access_error(clear):
    '''
    Tests for when the user has not joined the channel they are trying to share to
    '''
    token = auth_register_v1("gordonl@gmail.com", "1234567", "Gordon", "Liang")
    token2 = auth_register_v1("roland@gmail.com", "1234567", "Roland", "Lin")
    channel_id = channels_create_v1(token['token'], "Channel1", True)
    channel_id2 = channels_create_v1(token2['token'], "Channel2", True)
    message_id = message_send_v1(token['token'], channel_id['channel_id'], 'Hello')
    with pytest.raises(AccessError):
        assert message_share_v1(token['token'], message_id['message_id'], '', channel_id2['channel_id'], -1)
def test_message_share_dm(clear):
    '''
    Tests for when the user has not joined the dm they are trying to share to
    '''
    token = auth_register_v1("gordonl@gmail.com", "1234567", "Gordon", "Liang")
    token2 = auth_register_v1("roland@gmail.com", "1234567", "Roland", "Lin")
    dms = dm_create_v1(token['token'], [token2['auth_user_id']])
    channel_id = channels_create_v1(token['token'], "Channel1", True)
    message_id = message_send_v1(token['token'], channel_id['channel_id'], 'Hello')
    message_share_v1(token['token'], message_id['message_id'], '', -1, dms['dm_id'])
    messages = dm_messages_v1(token['token'], dms['dm_id'], 0)
    assert messages['messages'][0]['message'] == 'Hello'
def test_message_share_multiple(clear):
    '''
    Tests multiple shares to a channel
    '''
    user = auth_register_v1("gordonl@gmail.com", "1234567", "Gordon", "Liang")
    channel = channels_create_v1(user['token'], "Channel1", True)
    channel2 = channels_create_v1(user['token'], "Channel2", True)
    message = message_send_v1(user['token'], channel['channel_id'], 'Hello')
    message2 = message_send_v1(user['token'], channel['channel_id'], 'Hello2')
    message3 = message_send_v1(user['token'], channel['channel_id'], 'Hello3')
    message_share_v1(user['token'], message['message_id'], '', channel2['channel_id'], -1)
    message_share_v1(user['token'], message2['message_id'], '', channel2['channel_id'], -1)
    message_share_v1(user['token'], message3['message_id'], '', channel2['channel_id'], -1)
    messages = channel_messages_v1(user['token'], channel2['channel_id'], 0)
    assert messages['messages'][0]['message'] == 'Hello3'
    assert messages['messages'][1]['message'] == 'Hello2'
    assert messages['messages'][2]['message'] == 'Hello'
def test_message_share_message_addition(clear):
    '''
    Tests if function works when only one condition of AccessError is not true
    '''
    user = auth_register_v1("gordonl@gmail.com", "1234567", "Gordon", "Liang")
    channel = channels_create_v1(user['token'], "Channel1", True)
    channel2 = channels_create_v1(user['token'], "Channel2", True)
    message = message_send_v1(user['token'], channel['channel_id'], 'Hello')
    message_share_v1(user['token'], message['message_id'], 'Goodbye', channel2['channel_id'], -1)
    messages = channel_messages_v1(user['token'], channel2['channel_id'], 0)
    assert messages['messages'][0]['message'] == 'HelloGoodbye'
# Tests for message_senddm_v1
def test_message_senddm_v1(clear):
    '''
    Basic test for functionality of message_senddm_v1
    '''
    user = auth_register_v1("gordonl@gmail.com", "1234567", "Gordon", "Liang")
    user2 = auth_register_v1("roland@gmail.com", "1234567", "Roland", "Lin")
    dms = dm_create_v1(user['token'], [user2['auth_user_id']])
    message = message_senddm_v1(user['token'], dms['dm_id'], 'Hello')
    messages = dm_messages_v1(user['token'], dms['dm_id'], 0)
    assert messages['messages'][0]['message'] == 'Hello'
def test_message_senddm_input_error(clear):
    '''
    Tests if an InputError is raised when message is more than 1000 characters
    '''
    user = auth_register_v1("gordonl@gmail.com", "1234567", "Gordon", "Liang")
    user2 = auth_register_v1("roland@gmail.com", "1234567", "Roland", "Lin")
    dms = dm_create_v1(user['token'], [user2['auth_user_id']])
    with pytest.raises(InputError):
        assert message_senddm_v1(user['token'], dms['dm_id'], 'Hello' * 1000)
def test_message_senddm_access_error(clear):
    '''
    Tests for when the user has not joined the dm
    '''
    user = auth_register_v1("gordonl@gmail.com", "1234567", "Gordon", "Liang")
    user2 = auth_register_v1("roland@gmail.com", "1234567", "Roland", "Lin")
    user3 = auth_register_v1("jeremy@gmail.com", "1234567", "Jeremy", "Lee")
    dms = dm_create_v1(user2['token'], [user3['auth_user_id']])
    with pytest.raises(AccessError):
        assert message_senddm_v1(user['token'], dms['dm_id'], 'Hello')
def test_message_senddm_multiple(clear):
    '''
    Tests for multiple dms sent
    '''
    user = auth_register_v1("gordonl@gmail.com", "1234567", "Gordon", "Liang")
    user2 = auth_register_v1("roland@gmail.com", "1234567", "Roland", "Lin")
    dms = dm_create_v1(user['token'], [user2['auth_user_id']])
    message_senddm_v1(user['token'], dms['dm_id'], 'Hello')
    message_senddm_v1(user['token'], dms['dm_id'], 'Hello2')
    message_senddm_v1(user['token'], dms['dm_id'], 'Hello3')
    messages = dm_messages_v1(user['token'], dms['dm_id'], 0)
    assert messages['messages'][0]['message'] == 'Hello3'
    assert messages['messages'][1]['message'] == 'Hello2'
    assert messages['messages'][2]['message'] == 'Hello'