'''
Implementation of message functions that includes message_send_v1,
message_edit_v1, message_remove_v1, message_share_v1, message_senddm_v1.
Written by Gordon Liang
'''
import jwt
from src.error import InputError
from src.error import AccessError
from src.data import data
from datetime import datetime
from datetime import timezone

SECRET = 'HELLO'

def message_send_v1(token, channel_id, message):
    '''
    This function sends a given message to a given channel
    Arguments:
        token (str) - contains the session_id
        channel_id (int) - refers to an existing channel in the channels list
        message (str) - message given that is sent to the messages list in the channel
    Exceptions:
        InputError - when the message is more than 1000 characters and no message is given
        AccessError - If the token is invalid or the user has not joined the channel
    Return Value:
        {message_id}
    '''
    if len(message) > 1000:
        raise InputError('Message is more than 1000 characters')
    if len(message) == 0:
        raise InputError('No message given')
    valid = 0
    joined = 0
    payload = jwt.decode(token, SECRET, algorithms=['HS256'])
    session_id = payload['session_id']
    for user in data['users']:
        for s_id in user['session_ids']:
            if s_id == session_id:
                auth_user_id = user['u_id']
                valid = 1
    if valid != 1:
        raise AccessError('User does not exist')
    for user in data['channels'][channel_id]['all_members']:
        if user['u_id'] == auth_user_id:
            joined = 1
    if joined != 1:
        raise AccessError('User has not joined the channel')
    message_id = len(data['message_ids'])
    data['message_ids'].append(message_id)
    current_time = datetime.now()
    timestamp = round(current_time.replace(tzinfo=timezone.utc).timestamp(), 1)
    new_message = {
        'message_id': message_id,
        'u_id': auth_user_id,
        'message': message,
        'time_created': timestamp
    }
    data['channels'][channel_id]['messages'].insert(0, new_message)
    return {
        'message_id': message_id,
    }

def message_remove_v1(token, message_id):
    '''
    This function removes a message from a channel or dm
    Arguments:
        token (int) - contains session_id
        message_id (int) - message_id for message that needs to be removed
    Exceptions:
        InputError - when message is already removed
        AccessError - when token is invalid or message was not sent by user
                      and user is not owner of channel
    Return Value:
        {}
    '''
    valid = 0
    validuser = 0
    payload = jwt.decode(token, SECRET, algorithms=['HS256'])
    session_id = payload['session_id']
    for user in data['users']:
        for s_id in user['session_ids']:
            if s_id == session_id:
                auth_user_id = user['u_id']
                valid = 1
    if valid != 1:
        raise AccessError('User does not exist')
    for dm in data['dms']:
        for dm_message in dm['messages']:
            if dm_message['message_id'] == message_id:
                if dm_message['message'] == '':
                    raise InputError('Message does not exist')
    for channel in data['channels']:
        for message in channel['messages']:
            if message['message_id'] == message_id:
                if message['message'] == '':
                    raise InputError('Message does not exist')
                u_id = message['u_id']
                current_channel = channel
                for member in current_channel['owner_members']:
                    if member['u_id'] == auth_user_id and auth_user_id == u_id:
                        validuser = 1
    if validuser != 1:
        raise AccessError('Message was not sent by user and user is not an owner of the channel')
    for channel2 in data['channels']:
        for message2 in channel2['messages']:
            if message2['message_id'] == message_id:
                message2['message'] = ''
    for dm2 in data['dms']:
        for dm_message2 in dm2['messages']:
            if dm_message2['message_id'] == message_id:
                dm_message2['message'] = ''
    return {
    }

def message_edit_v1(token, message_id, message):
    '''
    This function edits a message in a channel or dm
    Arguments:
        token (str) - contains session_id
        message_id (int) - message_id for message that needs to be edited
        message (str) - message that replaces the current message
    Exceptions:
        InputError - when message is over 1000 characters or when message is
                     is already deleted
        AccessError - when the token is invalid or when the user is not an owner
                      and the message was not sent by the user
    Return Value:
        {}
    '''
    validuser = 0
    if len(message) > 1000:
        raise InputError('Message is more than 1000 characters')
    payload = jwt.decode(token, SECRET, algorithms=['HS256'])
    session_id = payload['session_id']
    for user in data['users']:
        for s_id in user['session_ids']:
            if s_id == session_id:
                auth_user_id = user['u_id']
                valid = 1
    if valid != 1:
        raise AccessError('User does not exist')
    
    for dm in data['dms']:
        for dm_message in dm['messages']:
            if dm_message['message_id'] == message_id:
                if dm_message['message'] == '':
                    raise InputError('Message has been deleted')
    for channel in data['channels']:
        for message2 in channel['messages']:
            if message2['message_id'] == message_id:
                u_id = message2['u_id']
                current_channel = channel
                if message2['message'] == '':
                    raise InputError('Message has been deleted')
            for member in current_channel['owner_members']:
                if member['u_id'] == auth_user_id and auth_user_id == u_id:
                    validuser = 1
            if validuser != 1:
                raise AccessError('Message was not sent by user and user is not an owner of the channel')
    for channel2 in data['channels']:
        for message3 in channel2['messages']:
            if message3['message_id'] == message_id:
                message3['message'] = message
    for dms in data['dms']:
        for dmmessage in dms['messages']:
            if dmmessage['message_id'] == message_id:
                dmmessage['message'] = message
    return {
    }
def message_share_v1(token, og_message_id, message, channel_id, dm_id):
    '''
    This function shares a message to a channel or dm
    Arguments:
        token (str) - contains session_id
        og_message_id (int) - message_id of the message that is being shared
        message (str) - optional message that can be included with message
                        being shared
        channel_id (int) - id of the channel that will have shared message. -1 
                           if being sent to dm
        dm_id (int) - id of the dm that the message is being shared to. -1 if
                      message is sent to channel
    Exceptions:
        InputError - when message is over 1000 characters
        AccessError - when token is invalid and user has not joined the channel
    Return Value:
        {shared_message_id} - returns id of the shared message
    '''
    if len(message) > 1000:
        raise InputError('Message is over 1000 characters')
    joined = 0
    payload = jwt.decode(token, SECRET, algorithms=['HS256'])
    session_id = payload['session_id']
    for user in data['users']:
        for s_id in user['session_ids']:
            if s_id == session_id:
                auth_user_id = user['u_id']
                valid = 1
    if valid != 1:
        raise AccessError('User does not exist')
    if channel_id != -1:
        for member in data['channels'][channel_id]['all_members']:
            if member['u_id'] == auth_user_id:
                joined = 1
        if joined != 1:
            raise AccessError('User has not joined channel')
    else:
        for member in data['dms'][dm_id]['members']:
            if member['u_id'] == auth_user_id:
                joined = 1
        if joined != 1:
            raise AccessError('User has not joined channel')
    for channel in data['channels']:
        for message2 in channel['messages']:
            if message2['message_id'] == og_message_id:
                shared_message = message2['message']
    shared_message += message
    message_id = len(data['message_ids'])
    data['message_ids'].append(message_id)
    current_time = datetime.now()
    timestamp = round(current_time.replace(tzinfo=timezone.utc).timestamp(), 1)
    new_message = {
        'message_id': len(data['message_ids']),
        'u_id': auth_user_id,
        'message': shared_message,
        'time_created': timestamp
    }
    data['channels'][channel_id]['messages'].insert(0, new_message)
    return {
        'shared_message_id': message_id
    }
def message_senddm_v1(token, dm_id, message):
    '''
    This function sends messages to dm
    Arguments:
        token (str) - contains session_id
        dm_id (int) - id of the dm that the message is being sent to
        message (str) - message that is being sent to dm
    Exceptions:
        InputError - when the message is over 1000 characters
        AccessError - when there is an invalid token or user is not part of dm
    Return Value:
        {message_id} - returns the id of the message
    '''
    exists = 0
    if len(message) > 1000:
        raise InputError('Message is more than 1000 characters')
    payload = jwt.decode(token, SECRET, algorithms=['HS256'])
    session_id = payload['session_id']
    for user in data['users']:
        for s_id in user['session_ids']:
            if s_id == session_id:
                auth_user_id = user['u_id']
                valid = 1
    if valid != 1:
        raise AccessError('User does not exist')
    for member in data['dms'][dm_id]['members']:
        if auth_user_id == member['u_id']:
            exists = 1
    if exists != 1:
        raise AccessError('User is not part of DM')
    message_id = len(data['message_ids'])
    data['message_ids'].append(message_id)
    current_time = datetime.now()
    timestamp = round(current_time.replace(tzinfo=timezone.utc).timestamp(), 1)
    new_message = {
        'message_id': message_id,
        'u_id': auth_user_id,
        'message': message,
        'time_created': timestamp
    }
    data['dms'][dm_id]['messages'].insert(0, new_message)
    return {
        'message_id': message_id
    }