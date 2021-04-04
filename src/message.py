import jwt
from src.error import InputError
from src.error import AccessError
from src.data import data
from datetime import datetime
from datetime import timezone

SECRET = 'HELLO'

def message_send_v1(token, channel_id, message):
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
    for channel in data['channels']:
        for message in channel['messages']:
            if message['message_id'] == message_id:
                if message['message'] == '':
                    raise InputError('Message does not exist')
                u_id = message['u_id']
                current_channel = channel
                channel_id = channel['channel_id']
                for member in current_channel['owner_members']:
                    if member['u_id'] == auth_user_id and auth_user_id == u_id:
                        validuser = 1
    if validuser != 1:
        raise AccessError('Message was not sent by user and user is not an owner of the channel')
    for message2 in data['channels'][channel_id]['messages']:
        if message2['message_id'] == message_id:
            message2['message'] = ''
    # messages = [i for i in current_channel['messages'] if not (i['message_id'] == auth_user)]
    # data['channels'][channel_id]['messages'] = messages
    return {
    }

def message_edit_v1(token, message_id, message):
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
    return {
    }
def message_share_v1(token, og_message_id, message, channel_id, dm_id):
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