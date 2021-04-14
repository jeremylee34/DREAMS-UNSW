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
from src.admin import admin_userpermission_change_v1
from src.admin import admin_user_remove_v1


@pytest.fixture
def clear():
    '''
    Clears data
    '''
    clear_v1()
@pytest.fixture
def user():
    '''
    Registers a user 
    '''
    user = auth_register_v1("gordonl@gmail.com", "1234567", "Gordon", "Liang")
    return user
@pytest.fixture
def user2():
    '''
    Registers another user
    '''
    user2 = auth_register_v1("roland@gmail.com", "1234567", "Roland", "Lin")
    return user2
@pytest.fixture
def channel(user):
    '''
    Creates a channel
    '''
    channel = channels_create_v1(user['token'], "Channel1", True)
    return channel
@pytest.fixture
def message(user, channel):
    '''
    Sends a message to the first channel made
    '''
    message = message_send_v1(user['token'], channel['channel_id'], 'Hello')
    return message
@pytest.fixture
def messages(user, channel):
    '''
    Gets the messages of a channel
    '''
    messages = channel_messages_v1(user['token'], channel['channel_id'], 0)
    return messages
@pytest.fixture
def dm_info(user, user2):
    dm_info = dm_create_v1(user['token'], [user2['auth_user_id']])
    return dm_info
# Tests for message_send_v1
def test_message_send(clear, user, channel, message, messages):
    '''
    Basic test for functionality of message_send_v1
    '''
    assert messages['messages'][0]['message'] == 'Hello'
def test_message_send_input_error(clear, user, channel):
    '''
    Testing for messages more than 1000 characters
    '''
    with pytest.raises(InputError):
        assert message_send_v1(user['token'], channel['channel_id'], 'Hello' * 1000)
def test_message_send_access_error(clear, user, user2, channel):
    '''
    Tests if an AccessError is raised when user trying to send message has not
    joined the channel
    '''
    with pytest.raises(AccessError):
        assert message_send_v1(user2['token'], channel['channel_id'], 'Hello')
def test_message_send_multiple(clear, user, channel, message, messages):
    '''
    Tests sending messages to multiple channels
    '''
    channel2 = channels_create_v1(user['token'], "Channel2", True)
    message_send_v1(user['token'], channel2['channel_id'], 'Hello123')
    messages2 = channel_messages_v1(user['token'], channel2['channel_id'], 0)
    assert messages['messages'][0]['message'] == 'Hello'
    assert messages2['messages'][0]['message'] == 'Hello123'
def test_message_send_multiple_messages(clear, user, channel, message):
    '''
    Tests sending multiple messages to a channel
    '''
    message_send_v1(user['token'], channel['channel_id'], 'Hello123')
    message_send_v1(user['token'], channel['channel_id'], 'Goodbye')
    message_send_v1(user['token'], channel['channel_id'], 'Goodbye123')
    messages = channel_messages_v1(user['token'], channel['channel_id'], 0)
    assert messages['messages'][3]['message'] == 'Hello'
    assert messages['messages'][2]['message'] == 'Hello123'
    assert messages['messages'][1]['message'] == 'Goodbye'
    assert messages['messages'][0]['message'] == 'Goodbye123'
def test_message_send_input_error2(clear, user, channel):
    '''
    Tests for when no message is given
    '''
    with pytest.raises(InputError):
        assert message_send_v1(user['token'], channel['channel_id'], '')
def test_message_send_invalid_token(clear, user, channel):
    '''
    Tests for when token is invalid
    '''
    with pytest.raises(InputError):
        assert message_send_v1(5, channel['channel_id'], 'Hello')
# Tests for message_edit_v1
def test_message_edit(clear, user, channel, message):
    '''
    Basic test for functionality of message_edit_v1
    '''
    message_send_v1(user['token'], channel['channel_id'], '3333')
    message_edit_v1(user['token'], message['message_id'], 'Goodbye')
    messages = channel_messages_v1(user['token'], channel['channel_id'], 0)
    assert messages['messages'][1]['message'] == 'Goodbye'
    assert messages['messages'][0]['message'] == '3333'
def test_message_edit_input_error(clear, user, channel, message):
    '''
    Tests for when message is over 1000 characters
    '''
    with pytest.raises(InputError):
        assert message_edit_v1(user['token'], message['message_id'], 'Goodbye' * 1000)
def test_message_edit_input_error2(clear, user, channel, message):
    '''
    Tests if an InputError is raised when message is already deleted
    '''
    message_remove_v1(user['token'], message['message_id'])
    with pytest.raises(InputError):
        assert message_edit_v1(user['token'], message['message_id'], 'Goodbye')
def test_message_edit_access_error(clear, user, user2, channel, message):
    '''
    Tests for when user has not created the message and is not an owner
    '''
    channel_join_v1(user2['token'], channel['channel_id'])
    with pytest.raises(AccessError):
        assert message_edit_v1(user2['token'], message['message_id'], 'Goodbye')
def test_message_edit_invalid_token(clear, user, channel, message):
    '''
    Tests for invalid token
    '''
    with pytest.raises(InputError):
        assert message_edit_v1(5, message['message_id'], 'Goodbye')
def test_message_edit_dm(clear, user, user2, dm_info):
    '''
    Tests message editing in a dm
    '''
    message_info = message_senddm_v1(user['token'], dm_info['dm_id'], 'Hello')
    message_senddm_v1(user['token'], dm_info['dm_id'], 'Goodbye')
    message_edit_v1(user['token'], message_info['message_id'], '123')
    messages = dm_messages_v1(user['token'], dm_info['dm_id'], 0)
    assert messages['messages'][0]['message'] == 'Goodbye'
    assert messages['messages'][1]['message'] == '123'
def test_message_edit_dm_input_error(clear, user, user2, dm_info):
    '''
    Tests for when a message is already removed
    '''
    message_info = message_senddm_v1(user['token'], dm_info['dm_id'], 'Hello')
    message_remove_v1(user['token'], message_info['message_id'])
    with pytest.raises(InputError):
        assert message_edit_v1(user['token'], message_info['message_id'], '123')
def test_message_edit_access_error2(clear, user, user2, channel, message):
    '''
    Tests for when a user is not an owner or the user who posted the message
    '''
    channel_join_v1(user2['token'], channel['channel_id'])
    with pytest.raises(AccessError):
        assert message_edit_v1(user2['token'], message['message_id'], '123')
def test_message_edit_no_error(clear, user, user2, channel):
    channel_join_v1(user2['token'], channel['channel_id'])
    message_info = message_send_v1(user2['token'], channel['channel_id'], 'Hello')
    message_edit_v1(user2['token'], message_info['message_id'], '123')
    messages = channel_messages_v1(user2['token'], channel['channel_id'], 0)
    assert messages['messages'][0]['message'] == '123'
# Tests for message_remove_v1
def test_message_remove(clear, user, channel, message):
    '''
    Basic test for functionality of message_remove_v1
    '''
    message_remove_v1(user['token'], message['message_id'])
    messages = channel_messages_v1(user['token'], channel['channel_id'], 0)
    assert messages['messages'][0]['message'] == ''
def test_message_remove_input_error(clear, user, channel, message):
    '''
    Tests if an InputError is raised when message is already deleted
    '''
    message_remove_v1(user['token'], message['message_id'])
    with pytest.raises(InputError):
        assert message_remove_v1(user['token'], message['message_id'])
def test_message_remove_access_error(clear, user, user2, channel, message):
    '''
    Tests for when user has not created the message and is not an owner
    '''
    channel_join_v1(user2['token'], channel['channel_id'])
    with pytest.raises(AccessError):
        assert message_remove_v1(user2['token'], message['message_id'])
def test_message_remove_multiple(clear, user, channel, message):
    '''
    Tests for multiple removed messages
    '''
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
def test_message_remove_invalid_token(clear, user, channel, message):
    '''
    Tests for invalid token
    '''
    with pytest.raises(InputError):
        assert message_remove_v1(6, message['message_id'])
def test_message_remove_dm_input_error(clear, user, user2, dm_info):
    '''
    Tests for when message has already been removed
    '''
    message = message_senddm_v1(user['token'], dm_info['dm_id'], 'Hello')
    message_senddm_v1(user['token'], dm_info['dm_id'], 'Hello2')
    message_senddm_v1(user['token'], dm_info['dm_id'], 'Hello3')
    message_remove_v1(user['token'], message['message_id'])
    with pytest.raises(InputError):
        assert message_remove_v1(user['token'], message['message_id'])
# Tests for message_share_v1
def test_message_share_channel(clear, user, channel, message):
    '''
    Basic test for functionality of message_share_v1
    '''
    channel_id2 = channels_create_v1(user['token'], "Channel2", True)
    message_share_v1(user['token'], message['message_id'], '', channel_id2['channel_id'], -1)
    messages = channel_messages_v1(user['token'], channel_id2['channel_id'], 0)
    assert messages['messages'][0]['message'] == 'Hello'
def test_message_share_access_error(clear, user, user2, channel, message):
    '''
    Tests for when the user has not joined the channel they are trying to share to
    '''
    channel_id2 = channels_create_v1(user2['token'], "Channel2", True)
    with pytest.raises(AccessError):
        assert message_share_v1(user['token'], message['message_id'], '', channel_id2['channel_id'], -1)
def test_message_share_dm(clear, user, user2, channel, message, dm_info):
    '''
    Tests for sharing message to a dm
    '''
    message_share_v1(user['token'], message['message_id'], '', -1, dm_info['dm_id'])
    messages = dm_messages_v1(user['token'], dm_info['dm_id'], 0)
    assert messages['messages'][0]['message'] == 'Hello'
def test_message_share_dm_access_error(clear, user, user2, dm_info):
    '''
    Tests for when the user has not joined the dm they are trying to share to
    '''
    user3 = auth_register_v1("jeremy@gmail.com", "1234567", "Jeremy", "Lee")
    dms2 = dm_create_v1(user2['token'], [user3['auth_user_id']])
    message_id = message_senddm_v1(user['token'], dm_info['dm_id'], 'Hello')
    with pytest.raises(AccessError):
        assert message_share_v1(user['token'], message_id['message_id'], '', -1, dms2['dm_id'])

def test_message_share_multiple(clear, user, channel, message):
    '''
    Tests multiple shares to a channel
    '''
    channel2 = channels_create_v1(user['token'], "Channel2", True)
    message2 = message_send_v1(user['token'], channel['channel_id'], 'Hello2')
    message3 = message_send_v1(user['token'], channel['channel_id'], 'Hello3')
    message_share_v1(user['token'], message['message_id'], '', channel2['channel_id'], -1)
    message_share_v1(user['token'], message2['message_id'], '', channel2['channel_id'], -1)
    message_share_v1(user['token'], message3['message_id'], '', channel2['channel_id'], -1)
    messages = channel_messages_v1(user['token'], channel2['channel_id'], 0)
    assert messages['messages'][0]['message'] == 'Hello3'
    assert messages['messages'][1]['message'] == 'Hello2'
    assert messages['messages'][2]['message'] == 'Hello'
def test_message_share_message_addition(clear, user, channel):
    '''
    Tests if function works when only one condition of AccessError is not true
    '''
    channel2 = channels_create_v1(user['token'], "Channel2", True)
    message = message_send_v1(user['token'], channel['channel_id'], 'Hello')
    message_share_v1(user['token'], message['message_id'], 'Goodbye', channel2['channel_id'], -1)
    messages = channel_messages_v1(user['token'], channel2['channel_id'], 0)
    assert messages['messages'][0]['message'] == 'HelloGoodbye'
def test_message_share_invalid_token(clear, user, channel):
    '''
    Tests for invalid token
    '''
    message = message_send_v1(user['token'], channel['channel_id'], 'Hello')
    with pytest.raises(InputError):
        assert message_share_v1(7, message['message_id'], 'Goodbye', channel['channel_id'], -1)
def test_message_share_input_error(clear, user, channel):
    '''
    Tests for when message is greater than 1000 characters
    '''
    message = message_send_v1(user['token'], channel['channel_id'], 'Hello')
    with pytest.raises(InputError):
        assert message_share_v1(user['token'], message['message_id'], 'Goodbye' * 1000, channel['channel_id'], -1)
# Tests for message_senddm_v1
def test_message_senddm_v1(clear, user, user2, dm_info):
    '''
    Basic test for functionality of message_senddm_v1
    '''
    message_senddm_v1(user['token'], dm_info['dm_id'], 'Hello')
    messages = dm_messages_v1(user['token'], dm_info['dm_id'], 0)
    assert messages['messages'][0]['message'] == 'Hello'
def test_message_senddm_input_error(clear, user, user2, dm_info):
    '''
    Tests if an InputError is raised when message is more than 1000 characters
    '''
    with pytest.raises(InputError):
        assert message_senddm_v1(user['token'], dm_info['dm_id'], 'Hello' * 1000)
def test_message_senddm_access_error(clear, user, user2):
    '''
    Tests for when the user has not joined the dm
    '''
    user3 = auth_register_v1("jeremy@gmail.com", "1234567", "Jeremy", "Lee")
    dms = dm_create_v1(user2['token'], [user3['auth_user_id']])
    with pytest.raises(AccessError):
        assert message_senddm_v1(user['token'], dms['dm_id'], 'Hello')
def test_message_senddm_multiple(clear, user, user2, dm_info):
    '''
    Tests for multiple dms sent
    '''
    message_senddm_v1(user['token'], dm_info['dm_id'], 'Hello')
    message_senddm_v1(user['token'], dm_info['dm_id'], 'Hello2')
    message_senddm_v1(user['token'], dm_info['dm_id'], 'Hello3')
    messages = dm_messages_v1(user['token'], dm_info['dm_id'], 0)
    assert messages['messages'][0]['message'] == 'Hello3'
    assert messages['messages'][1]['message'] == 'Hello2'
    assert messages['messages'][2]['message'] == 'Hello'
def test_message_senddm_invalid_token(clear, user, user2, dm_info):
    '''
    Tests for invalid token
    '''
    with pytest.raises(InputError):
        assert message_senddm_v1(6, dm_info['dm_id'], 'Hello')
