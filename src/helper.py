from src.error import InputError
from src.error import AccessError
from src.data import data

import jwt
import time
import threading

SECRET = "HELLO"
OWNER_PERMISSION = 1

def check_valid_channel(channel_id):
    """
    Checks if channel_id is a valid channel
    """
    valid_channel = False
    for channels in data['channels']:
        if channels['channel_id'] == channel_id:
            valid_channel = True
            break
    if valid_channel is False:
        return False

def check_public_channel(channel_id):
    """
    Checks if a channel is public
    """
    if data['channels'][channel_id]['is_public'] is False:
        return False
    else:
        return True

def check_user_in_channel(channel_id, u_id):
    """
    Checks whether a user is in a channel
    """
    user_in_channel = False
    for member in data['channels'][channel_id]['all_members']:
        ## if u_id matches the member
        if member['u_id'] == u_id:
            user_in_channel = True
            break
    return user_in_channel

def check_valid_user(u_id):
    """
    Checks whether a u_id refers to a valid user
    """
    valid_user = False
    for user in data['users']:
        if user['u_id'] == u_id:
            valid_user = True
            break
    return valid_user

def token_to_u_id(token):
    # find u_id related to token
    session_id = jwt.decode(token, SECRET, algorithms=['HS256'])
    for user in data['users']:
        for session in user['session_ids']:
            if session == session_id['session_id']:
                u_id = user['u_id']
    return u_id

def check_valid_dm(dm_id):
    valid_dm = False
    for dm in data['dms']:
        if dm['dm_id'] == dm_id:
            valid_dm = True
            break
    return valid_dm

def check_user_in_dm(u_id, dm_id):
    user_in_dm = False
    for member in data['dms'][dm_id]['members']:
        if member['u_id'] == u_id:
            user_in_dm = True
            break
    return user_in_dm

def check_valid_token(token):
    valid_token = False
    for token_hash in data['token_list']:
        if token_hash == token:
            valid_token = True
    return valid_token

def check_owner_perm(u_id):
    is_owner = False
    for user in data['users']:
        if user['u_id'] == u_id:
            if user['permission_id'] == OWNER_PERMISSION:
                is_owner = True
    return is_owner

def check_if_owner(u_id, channel_id):
    is_owner = False
    for user in data['channels'][channel_id]['owner_members']:
        if user['u_id'] == u_id:
            is_owner = True
            break
    return is_owner

def end_standup(channel_id, curr_time, owner_u_id):
    temp_channel = data['channels'][channel_id]
    data['channels'][channel_id]['standup'].clear
    data['channels'][channel_id]['active_standup'] = False
    data['channels'][channel_id]['standup_time_finish'] = 0
    # once timer ends, run this code 
    message_block = []
    for msg in temp_channel['standup']:
        new_msg = f"{msg['handle_str']}: {msg['message']}"
        message_block.append(new_msg)
    message_block_joined = '\n'.join(message_block)
    standup_msg = {
        'message_id': len(temp_channel['messages']),
        'u_id': owner_u_id,
        'time_created': curr_time,
        'message': message_block_joined
    }
    data['channels'][channel_id]['messages'].append(standup_msg)
    print('hi')
    
 

# def check_active_standup_in_channel(channel_id):
#     if not data['channels'][channel_id]['standup']:
#         active_standup = False
#     elif data['channels'][channel_id]['is_active'] is True:
#         active_standup = True
#     return active_standup

# def check_channel_owner(u_id, channel_id):
#     channel_owner = False
#     for owner in data['channels'][channel_id]['owner_members']:
#         if owner['u_id'] == u_id:
#             channel_owner = True
#     return channel_owner
