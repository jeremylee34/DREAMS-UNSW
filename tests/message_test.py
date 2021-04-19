import pytest
from datetime import datetime, timedelta, timezone
import threading
import time
from src.auth import auth_register_v1
from src.auth import auth_login_v1
from src.other import clear_v1
from src.channel import channel_messages_v1
from src.channel import channel_join_v1
from src.channels import channels_create_v1
from src.message import message_send_v1
from src.message import message_edit_v1
from src.message import message_remove_v1
from src.message import message_senddm_v1
from src.message import message_share_v1
from src.message import message_sendlater_v1
from src.message import message_sendlaterdm_v1
from src.message import message_react_v1
from src.message import message_unreact_v1
from src.message import message_pin_v1
from src.message import message_unpin_v1
from src.error import InputError
from src.error import AccessError
from src.dm import dm_create_v1
from src.dm import dm_messages_v1
from src.admin import admin_userpermission_change_v1
from src.admin import admin_user_remove_v1
from src.data import data

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
def user3():
    user3 = auth_register_v1("jeremy@gmail.com", "1234567", "Jeremy", "Lee")
    return user3
@pytest.fixture
def channel(user):
    '''
    Creates a channel
    '''
    channel = channels_create_v1(user['token'], "Channel1", True)
    return channel
@pytest.fixture
def channel2(user):
    '''
    Creates another channel
    '''
    channel2 = channels_create_v1(user['token'], "Channel2", True)
    return channel2
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
    '''
    Creates a dm between two users
    '''
    dm_info = dm_create_v1(user['token'], [user2['auth_user_id']])
    return dm_info
@pytest.fixture
def remove(user, message):
    '''
    Removes a message from dm or channel
    '''
    message_remove_v1(user['token'], message['message_id'])
@pytest.fixture
def dm_message(user, dm_info):
    '''
    Sends a message to a dm
    '''
    dm_message = message_senddm_v1(user['token'], dm_info['dm_id'], 'Hello')
    return dm_message
@pytest.fixture
def dm_messages(user, dm_info):
    dm_messages = dm_messages_v1(user['token'], dm_info['dm_id'], 0)
    return dm_messages
@pytest.fixture
def join(user2, channel):
    '''
    Joins a channel
    '''
    channel_join_v1(user2['token'], channel['channel_id'])
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
@pytest.fixture
def sendlater(user, channel, timestamp):
    '''
    Sends a message to a channel at a given time
    '''
    message_sendlater_v1(user['token'], channel['channel_id'], 'Hello', timestamp)
@pytest.fixture
def sendlaterdm(user, dm_info, timestamp):
    '''
    Sends a message to a DM at a given time
    '''
    message_sendlaterdm_v1(user['token'], dm_info['dm_id'], 'Hello', timestamp)
@pytest.fixture
def sleep():
    '''
    Stops the thread for two seconds
    '''
    time.sleep(3)
@pytest.fixture
def react(user, message):
    '''
    Reacts to a message
    '''
    message_react_v1(user['token'], message['message_id'], 1)
@pytest.fixture
def pin(user, message):
    '''
    Pins a message
    '''
    message_pin_v1(user['token'], message['message_id'])
@pytest.fixture
def unpin(user, message):
    '''
    Unpins a message
    '''
    message_unpin_v1(user['token'], message['message_id'])
# Tests for message_send_v1
def test_message_send(clear, user, channel, message):
    '''
    Basic test for functionality of message_send_v1
    '''
    message_send_v1(user['token'], channel['channel_id'], '@Hello')
    messages = channel_messages_v1(user['token'], channel['channel_id'], 0)
    assert messages['messages'][1]['message'] == 'Hello'
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
def test_message_send_multiple(clear, user, channel, channel2, message, messages):
    '''
    Tests sending messages to multiple channels
    '''
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
def test_message_edit_input_error2(clear, user, channel, message, remove):
    '''
    Tests if an InputError is raised when message is already deleted
    '''
    with pytest.raises(InputError):
        assert message_edit_v1(user['token'], message['message_id'], 'Goodbye')
def test_message_edit_access_error(clear, user, user2, channel, message, join):
    '''
    Tests for when user has not created the message and is not an owner
    '''
    with pytest.raises(AccessError):
        assert message_edit_v1(user2['token'], message['message_id'], 'Goodbye')
def test_message_edit_invalid_token(clear, user, channel, message):
    '''
    Tests for invalid token
    '''
    with pytest.raises(InputError):
        assert message_edit_v1(5, message['message_id'], 'Goodbye')
def test_message_edit_dm(clear, user, user2, dm_info, dm_message):
    '''
    Tests message editing in a dm
    '''
    message_senddm_v1(user['token'], dm_info['dm_id'], 'Goodbye')
    message_edit_v1(user['token'], dm_message['message_id'], '123')
    messages = dm_messages_v1(user['token'], dm_info['dm_id'], 0)
    assert messages['messages'][0]['message'] == 'Goodbye'
    assert messages['messages'][1]['message'] == '123'
def test_message_edit_dm_input_error(clear, user, user2, dm_info, dm_message):
    '''
    Tests for when a message is already removed
    '''
    message_remove_v1(user['token'], dm_message['message_id'])
    with pytest.raises(InputError):
        assert message_edit_v1(user['token'], dm_message['message_id'], '123')
def test_message_edit_access_error2(clear, user, user2, channel, message, join):
    '''
    Tests for when a user is not an owner or the user who posted the message
    '''
    with pytest.raises(AccessError):
        assert message_edit_v1(user2['token'], message['message_id'], '123')
def test_message_edit_no_error(clear, user, user2, channel, join):
    message_info = message_send_v1(user2['token'], channel['channel_id'], 'Hello')
    message_edit_v1(user2['token'], message_info['message_id'], '123')
    messages = channel_messages_v1(user2['token'], channel['channel_id'], 0)
    assert messages['messages'][0]['message'] == '123'
# Tests for message_remove_v1
def test_message_remove(clear, user, channel, message, remove):
    '''
    Basic test for functionality of message_remove_v1
    '''
    messages = channel_messages_v1(user['token'], channel['channel_id'], 0)
    assert messages['messages'] == []
def test_message_remove_input_error(clear, user, channel, message, remove):
    '''
    Tests if an InputError is raised when message is already deleted
    '''
    with pytest.raises(InputError):
        assert message_remove_v1(user['token'], message['message_id'])
def test_message_remove_access_error(clear, user, user2, channel, message, join):
    '''
    Tests for when user has not created the message and is not an owner
    '''
    with pytest.raises(AccessError):
        assert message_remove_v1(user2['token'], message['message_id'])
def test_message_remove_multiple(clear, user, channel, message, remove):
    '''
    Tests for multiple removed messages
    '''
    message2 = message_send_v1(user['token'], channel['channel_id'], 'Hello123')
    message3 = message_send_v1(user['token'], channel['channel_id'], 'Goodbye')
    message4 = message_send_v1(user['token'], channel['channel_id'], 'Three')
    message_remove_v1(user['token'], message2['message_id'])
    message_remove_v1(user['token'], message3['message_id'])
    message_remove_v1(user['token'], message4['message_id'])
    messages = channel_messages_v1(user['token'], channel['channel_id'], 0)
    assert messages['messages'] == []
def test_message_remove_invalid_token(clear, user, channel, message):
    '''
    Tests for invalid token
    '''
    with pytest.raises(InputError):
        assert message_remove_v1(6, message['message_id'])
def test_message_remove_dm_input_error(clear, user, user2, dm_info, dm_message):
    '''
    Tests for when message has already been removed
    '''
    message_senddm_v1(user['token'], dm_info['dm_id'], 'Hello2')
    message_senddm_v1(user['token'], dm_info['dm_id'], 'Hello3')
    message_remove_v1(user['token'], dm_message['message_id'])
    with pytest.raises(InputError):
        assert message_remove_v1(user['token'], dm_message['message_id'])
# Tests for message_share_v1
def test_message_share_channel(clear, user, channel, channel2, message):
    '''
    Basic test for functionality of message_share_v1
    '''
    message_share_v1(user['token'], message['message_id'], '', channel2['channel_id'], -1)
    messages = channel_messages_v1(user['token'], channel2['channel_id'], 0)
    assert messages['messages'][0]['message'] == 'Hello'
def test_message_share_access_error(clear, user, user2, channel, channel2, message):
    '''
    Tests for when the user has not joined the channel they are trying to share to
    '''
    channel_id2 = channels_create_v1(user2['token'], "Channel2", True)
    with pytest.raises(AccessError):
        assert message_share_v1(user['token'], message['message_id'], '', channel_id2['channel_id'], -1)
def test_message_share_dm(clear, user, user2, user3, dm_info, dm_message):
    '''
    Tests for sharing message to a dm
    '''
    message_senddm_v1(user['token'], dm_info['dm_id'], 'Hello2')
    dm_info2 = dm_create_v1(user['token'], [user3['auth_user_id']])
    message_share_v1(user['token'], dm_message['message_id'], '', -1, dm_info2['dm_id'])
    messages = dm_messages_v1(user['token'], dm_info2['dm_id'], 0)
    assert messages['messages'][0]['message'] == 'Hello'
def test_message_share_dm_access_error(clear, user, user2, user3, dm_info, dm_message):
    '''
    Tests for when the user has not joined the dm they are trying to share to
    '''
    dms2 = dm_create_v1(user2['token'], [user3['auth_user_id']])
    with pytest.raises(AccessError):
        assert message_share_v1(user['token'], dm_message['message_id'], '', -1, dms2['dm_id'])

def test_message_share_multiple(clear, user, channel, channel2, message):
    '''
    Tests multiple shares to a channel
    '''
    message2 = message_send_v1(user['token'], channel['channel_id'], 'Hello2')
    message3 = message_send_v1(user['token'], channel['channel_id'], 'Hello3')
    message_share_v1(user['token'], message['message_id'], '', channel2['channel_id'], -1)
    message_share_v1(user['token'], message2['message_id'], '', channel2['channel_id'], -1)
    message_share_v1(user['token'], message3['message_id'], '', channel2['channel_id'], -1)
    messages = channel_messages_v1(user['token'], channel2['channel_id'], 0)
    assert messages['messages'][0]['message'] == 'Hello3'
    assert messages['messages'][1]['message'] == 'Hello2'
    assert messages['messages'][2]['message'] == 'Hello'
def test_message_share_message_addition(clear, user, channel, channel2):
    '''
    Tests if function works when only one condition of AccessError is not true
    '''
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
def test_message_senddm_v1(clear, user, user2, dm_info, dm_message):
    '''
    Basic test for functionality of message_senddm_v1
    '''
    message_senddm_v1(user['token'], dm_info['dm_id'], '@Hello')
    messages = dm_messages_v1(user['token'], dm_info['dm_id'], 0)
    assert messages['messages'][1]['message'] == 'Hello'
def test_message_senddm_input_error(clear, user, user2, dm_info):
    '''
    Tests if an InputError is raised when message is more than 1000 characters
    '''
    with pytest.raises(InputError):
        assert message_senddm_v1(user['token'], dm_info['dm_id'], 'Hello' * 1000)
def test_message_senddm_access_error(clear, user, user2, user3, dm_info):
    '''
    Tests for when the user has not joined the dm
    '''
    with pytest.raises(AccessError):
        assert message_senddm_v1(user3['token'], dm_info['dm_id'], 'Hello')
def test_message_senddm_multiple(clear, user, user2, dm_info, dm_message):
    '''
    Tests for multiple dms sent
    '''
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

def test_message_sendlater(clear, user, channel, timestamp, sendlater, sleep, messages):
    '''
    Basic test for functionality of message_sendlater_v1
    '''
    assert messages['messages'][0]['message'] == 'Hello'
def test_message_sendlater_invalid_channel(clear, user, channel, timestamp):
    '''
    Tests if an InputError is raised when channel id is invalid
    '''
    with pytest.raises(InputError):
        assert message_sendlater_v1(user['token'], 4, 'Hello', timestamp)
def test_message_sendlater_invalid_message(clear, user, channel, timestamp):
    '''
    Tests if an InputError is raised when a message is over 1000 characters
    '''
    with pytest.raises(InputError):
        assert message_sendlater_v1(user['token'], channel['channel_id'], 'Hello' * 1000, timestamp)
def test_message_sendlater_past_time(clear, user, channel, past_time):
    '''
    Tests if an InputError is raised when a time that has already past is entered 
    '''
    with pytest.raises(InputError):
        assert message_sendlater_v1(user['token'], channel['channel_id'], 'Hello', past_time)
def test_message_sendlater_access_error(clear, user, user2, channel, timestamp):
    '''
    Tests if an AccessError is raised when a user that is not in the channel tries to send a 
    message later
    '''
    with pytest.raises(AccessError):
        assert message_sendlater_v1(user2['token'], channel['channel_id'], 'Hello', timestamp)
def test_message_sendlater_invalid_token(clear, user, channel, timestamp):
    '''
    Tests if an InputError is raised when an invalid token is entered
    '''
    with pytest.raises(InputError):
        assert message_sendlater_v1(55, channel['channel_id'], 'Hello', timestamp)
def test_message_sendlater_notifications(clear, user):
    channel = channels_create_v1(user['token'], "Channel1", True)
    timestamp = int(time.time())
    user_login = auth_login_v1('gordonl@gmail.com', '1234567')
    message_sendlater_v1(user_login['token'], channel['channel_id'], '@Hello', timestamp)
    time.sleep(3)
    messages = channel_messages_v1(user['token'], channel['channel_id'], 0)
    assert messages['messages'][0]['message'] == '@Hello'
def test_message_sendlaterdm(clear, user, user2, timestamp, sendlaterdm, sleep, dm_messages):
    '''
    Basic test for functionality of message_sendlaterdm_v1
    '''
    assert dm_messages['messages'][0]['message'] == 'Hello'
def test_message_sendlaterdm_invalid_dm(clear, user, user2, dm_info, timestamp):
    '''
    Tests if an InputError is raised when an invalid dm is entered
    '''
    with pytest.raises(InputError):
        assert message_sendlaterdm_v1(user['token'], 6, 'Hello', timestamp)
def test_message_sendlaterdm_invalid_message(clear, user, user2, dm_info, timestamp):
    '''
    Tests if an InputError is raised when message is greater than 1000 characters
    '''
    with pytest.raises(InputError):
        assert message_sendlaterdm_v1(user['token'], dm_info['dm_id'], 'Hello' * 1000, timestamp)
def test_message_sendlaterdm_past_time(clear, user, user2, dm_info, past_time):
    '''
    Tests if an InputError is raised when a time that has already past is entered
    '''
    with pytest.raises(InputError):
        assert message_sendlaterdm_v1(user['token'], dm_info['dm_id'], 'Hello', past_time)
def test_message_sendlaterdm_access_error(clear, user, user2, user3, dm_info, timestamp):
    '''
    Tests if an AccessError is raised when a user that is not part of the dm tries to send a 
    message
    '''
    with pytest.raises(AccessError):
        assert message_sendlaterdm_v1(user3['token'], dm_info['dm_id'], 'Hello', timestamp)
def test_message_sendlaterdm_invalid_token(clear, user, user2, dm_info, timestamp):
    '''
    Tests if an InputError is raised when an invalid token is entered
    '''
    with pytest.raises(InputError):
        assert message_sendlaterdm_v1(7, dm_info['dm_id'], 'Hello', timestamp)
def test_message_sendlaterdm_notifications(clear, user, user2):
    dm_info = dm_create_v1(user['token'], [user2['auth_user_id']])
    timestamp = int(time.time())
    user_login = auth_login_v1('gordonl@gmail.com', '1234567')
    message_sendlaterdm_v1(user_login['token'], dm_info['dm_id'], '@Hello', timestamp)
    time.sleep(3)
    messages = dm_messages_v1(user['token'], dm_info['dm_id'], 0)
    assert messages['messages'][0]['message'] == '@Hello'



def test_message_react_channel(clear, user, channel, message):
    '''
    Basic test for functionality of message_react in a channel
    '''
    message_send_v1(user['token'], channel['channel_id'], 'Hello1')
    message_send_v1(user['token'], channel['channel_id'], 'Hello2')
    message_send_v1(user['token'], channel['channel_id'], 'ABC')
    message_react_v1(user['token'], message['message_id'], 1)
    messages = channel_messages_v1(user['token'], channel['channel_id'], 0)
    assert messages['messages'][3]['reacts'][0]['react_id'] == 1
    assert user['auth_user_id'] in messages['messages'][3]['reacts'][0]['u_ids']
    assert messages['messages'][3]['reacts'][0]['is_this_user_reacted'] == True
def test_message_react_dm(clear, user, user2, dm_info, dm_message):
    '''
    Basic test for functionality of message_react in a dm
    '''
    message_senddm_v1(user['token'], dm_info['dm_id'], 'Hello1')
    message_react_v1(user['token'], dm_message['message_id'], 1)
    messages = dm_messages_v1(user['token'], dm_info['dm_id'], 0)
    assert messages['messages'][1]['reacts'][0]['react_id'] == 1
    assert user['auth_user_id'] in messages['messages'][1]['reacts'][0]['u_ids']
    assert messages['messages'][1]['reacts'][0]['is_this_user_reacted'] == True
def test_message_react_invalid_message_id(clear, user, channel, message):
    '''
    Tests if an InputError is raised when the message id is invalid
    '''
    with pytest.raises(InputError):
        assert message_react_v1(user['token'], 2, 1)
def test_message_react_invalid_react_id(clear, user, channel, message):
    '''
    Tests if an InputError is raised when the react id is invalid
    '''
    with pytest.raises(InputError):
        assert message_react_v1(user['token'], message['message_id'], 100)
def test_message_react_already_reacted(clear, user, channel, message, react):
    '''
    Tests if an InputError is raised when a message has already been reacted by the user
    '''
    with pytest.raises(InputError):
        assert message_react_v1(user['token'], message['message_id'], 1)
def test_message_react_already_reacted_dm(clear, user, user2, dm_info, dm_message):
    '''
    Tests if an InputError is raised when a message has already been reacted by the user
    '''
    message_react_v1(user['token'], dm_message['message_id'], 1)
    with pytest.raises(InputError):
        assert message_react_v1(user['token'], dm_message['message_id'], 1)
def test_message_react_access_error(clear, user, user2, channel, message):
    '''
    Tests if an AccessError is raised when the user trying to react has not joined the channel
    '''
    with pytest.raises(AccessError):
        assert message_react_v1(user2['token'], message['message_id'], 1)
def test_message_react_invalid_token(clear, user, channel, message):
    '''
    Tests if an InputError is raised when an invalid token is entered
    '''
    with pytest.raises(InputError):
        assert message_react_v1(3, message['message_id'], 1)



def test_message_unreact_channel(clear, user, channel, message, react):
    '''
    Basic test for functionality of message_unreact_v1 in a channel
    '''
    message_send_v1(user['token'], channel['channel_id'], 'Hello1')
    message_unreact_v1(user['token'], message['message_id'], 1)
    messages = channel_messages_v1(user['token'], channel['channel_id'], 0)
    assert messages['messages'][1]['reacts'][0]['react_id'] == 1
    assert messages['messages'][1]['reacts'][0]['u_ids'] == []
    assert messages['messages'][1]['reacts'][0]['is_this_user_reacted'] == False
def test_message_unreact_dm(clear, user, user2, dm_info, dm_message):
    '''
    Basic test for functionality of message_unreact_v1 in a dm
    '''
    message_senddm_v1(user['token'], dm_info['dm_id'], 'Hello1')
    message_react_v1(user['token'], dm_message['message_id'], 1)
    message_unreact_v1(user['token'], dm_message['message_id'], 1)
    messages = dm_messages_v1(user['token'], dm_info['dm_id'], 0)
    assert messages['messages'][1]['reacts'][0]['react_id'] == 1
    assert messages['messages'][1]['reacts'][0]['u_ids'] == []
    assert messages['messages'][1]['reacts'][0]['is_this_user_reacted'] == False
def test_message_unreact_invalid_message_id(clear, user, channel, message, react):
    '''
    Tests if an InputError is raised when the message id is invalid
    '''
    with pytest.raises(InputError):
        assert message_unreact_v1(user['token'], 10, 1)
def test_message_unreact_invalid_react_id(clear, user, channel, message, react):
    '''
    Tests if an InputError is raised when the react id is invalid
    '''
    with pytest.raises(InputError):
        assert message_unreact_v1(user['token'], message['message_id'], 100)
def test_message_unreact_already_unreacted(clear, user, channel, message):
    '''
    Tests if an InputError is raised when a message has not been reacted by the user
    '''
    with pytest.raises(InputError):
        assert message_unreact_v1(user['token'], message['message_id'], 1)
def test_message_unreact_already_unreacted_dm(clear, user, user2, dm_info, dm_message):
    '''
    Tests if an InputError is raised when a message has not been reacted by the user
    '''
    with pytest.raises(InputError):
        assert message_unreact_v1(user['token'], dm_message['message_id'], 1)
def test_message_unreact_access_error(clear, user, user2, channel, message, react):
    '''
    Tests if an AccessError is raised when the user trying to unreact has not joined the channel
    '''
    with pytest.raises(AccessError):
        assert message_unreact_v1(user2['token'], message['message_id'], 1)
def test_message_unreact_invalid_token(clear, user, channel, message, react):
    '''
    Tests if an InputError is raised when an invalid token is entered
    '''
    with pytest.raises(InputError):
        assert message_unreact_v1(3, message['message_id'], 1)



def test_message_pin_channel(clear, user, channel, message, pin):
    '''
    Basic test for functionality of message_pin_v1 in a channel
    '''
    messages = channel_messages_v1(user['token'], channel['channel_id'], 0)
    assert messages['messages'][0]['is_pinned'] == True
def test_message_pin_dm(clear, user, user2, dm_info, dm_message):
    '''
    Basic test for functionality of message_pin_v1 in a dm
    '''
    message_pin_v1(user['token'], dm_message['message_id'])
    messages = dm_messages_v1(user['token'], dm_info['dm_id'], 0)
    assert messages['messages'][0]['is_pinned'] == True
def test_message_pin_invalid_message_id(clear, user, channel, message):
    '''
    Tests if an InputError is raised when an invalid message id is entered
    '''
    with pytest.raises(InputError):
        assert message_pin_v1(user['token'], 10)
def test_message_pin_invalid_message(clear, user, channel):
    '''
    Tests if an InputError is raised when an invalid message id is entered
    '''
    message = message_send_v1(user['token'], channel['channel_id'], 'Hello')
    message_send_v1(user['token'], channel['channel_id'], '2Hello')
    message_remove_v1(user['token'], message['message_id'])
    with pytest.raises(InputError):
        assert message_pin_v1(user['token'], message['message_id'])
def test_message_pin_invalid_message_dm(clear, user, user2, dm_info):
    '''
    Tests if an InputError is raised when an invalid message id is entered
    '''
    message = message_senddm_v1(user['token'], dm_info['dm_id'], 'Hello')
    message_senddm_v1(user['token'], dm_info['dm_id'], '2Hello')
    message_remove_v1(user['token'], message['message_id'])
    with pytest.raises(InputError):
        assert message_pin_v1(user['token'], message['message_id'])
def test_message_pin_already_pinned(clear, user, channel, message, pin):
    '''
    Tests if an InputError is raised when message pin is called when a message is already pinned
    '''
    with pytest.raises(InputError):
        assert message_pin_v1(user['token'], message['message_id'])
def test_message_pin_already_pinned_dm(clear, user, user2, dm_info, dm_message):
    '''
    Tests if an InputError is raised when message pin is called when a message is already pinned
    '''
    message_pin_v1(user['token'], dm_message['message_id'])
    with pytest.raises(InputError):
        assert message_pin_v1(user['token'], dm_message['message_id'])
def test_message_pin_access_error(clear, user, user2, channel, join, message):
    '''
    Tests if an AccessError is raised when a user that is not an owner tries to pin a message
    '''
    with pytest.raises(AccessError):
        assert message_pin_v1(user2['token'], message['message_id'])
def test_message_pin_access_error_dm(clear, user, user2, dm_info, dm_message):
    '''
    Tests if an AccessError is raised when a user that is not an owner tries to pin a message
    '''
    with pytest.raises(AccessError):
        assert message_pin_v1(user2['token'], dm_message['message_id'])
def test_message_pin_invalid_token(clear, user, channel, message):
    '''
    Tests if an InputError is raised when an invalid token is entered
    '''
    with pytest.raises(InputError):
        assert message_pin_v1(3, message['message_id'])


def test_message_unpin_channel(clear, user, channel, message, pin, unpin):
    '''
    Basic test for functionality of message_pin_v1 in a channel
    '''
    messages = channel_messages_v1(user['token'], channel['channel_id'], 0)
    assert messages['messages'][0]['is_pinned'] == False
def test_message_unpin_dm(clear, user, user2, dm_info, dm_message):
    '''
    Basic test for functionality of message_pin_v1 in a dm
    '''
    message_pin_v1(user['token'], dm_message['message_id'])
    message_unpin_v1(user['token'], dm_message['message_id'])
    messages = dm_messages_v1(user['token'], dm_info['dm_id'], 0)
    assert messages['messages'][0]['is_pinned'] == False
def test_message_unpin_invalid_message_id(clear, user, channel, message, pin):
    '''
    Tests if an InputError is raised when an invalid message id is entered
    '''
    with pytest.raises(InputError):
        assert message_unpin_v1(user['token'], 10)
def test_message_unpin_invalid_message(clear, user, channel):
    '''
    Tests if an InputError is raised when an invalid message id is entered
    '''
    message = message_send_v1(user['token'], channel['channel_id'], 'Hello')
    message_send_v1(user['token'], channel['channel_id'], '2Hello')
    message_pin_v1(user['token'], message['message_id'])
    message_remove_v1(user['token'], message['message_id'])
    with pytest.raises(InputError):
        assert message_unpin_v1(user['token'], message['message_id'])
def test_message_unpin_invalid_message_dm(clear, user, user2, dm_info):
    '''
    Tests if an InputError is raised when an invalid message id is entered
    '''
    message = message_senddm_v1(user['token'], dm_info['dm_id'], 'Hello')
    message_senddm_v1(user['token'], dm_info['dm_id'], '2Hello')
    message_pin_v1(user['token'], message['message_id'])
    message_remove_v1(user['token'], message['message_id'])
    with pytest.raises(InputError):
        assert message_unpin_v1(user['token'], message['message_id'])
def test_message_unpin_already_unpinned(clear, user, channel, message, pin, unpin):
    '''
    Tests if an InputError is raised when message pin is called when a message is already unpinned
    '''
    with pytest.raises(InputError):
        assert message_unpin_v1(user['token'], message['message_id'])
def test_message_pin_already_unpinned_dm(clear, user, user2, dm_info, dm_message):
    '''
    Tests if an InputError is raised when message pin is called when a message is already pinned
    '''
    with pytest.raises(InputError):
        assert message_unpin_v1(user['token'], dm_message['message_id'])
def test_message_unpin_access_error(clear, user, user2, channel, join, message, pin):
    '''
    Tests if an AccessError is raised when a user that is not an owner tries to unpin a message
    '''
    with pytest.raises(AccessError):
        assert message_unpin_v1(user2['token'], message['message_id'])
def test_message_unpin_access_error_dm(clear, user, user2, dm_info, dm_message):
    '''
    Tests if an AccessError is raised when a user that is not an owner tries to unpin a message
    '''
    message_pin_v1(user['token'], dm_message['message_id'])
    with pytest.raises(AccessError):
        assert message_unpin_v1(user2['token'], dm_message['message_id'])
def test_message_unpin_invalid_token(clear, user, channel, message, pin):
    '''
    Tests if an InputError is raised when an invalid token is entered
    '''
    with pytest.raises(InputError):
        assert message_unpin_v1(3, message['message_id'])

