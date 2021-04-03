from src.error import InputError
from src.error import AccessError

import jwt

SECRET = "HELLO"

def check_valid_channel(data, channel_id):
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

def check_public_channel(data, channel_id):
    """
    Checks if a channel is public
    """
    if data['channels'][channel_id]['is_public'] is False:
        return False

def check_user_in_channel(data, channel_id, auth_user_id):
    """
    Checks whether a user is in a channel
    """
    user_in_channel = False
    for member in data['channels'][channel_id]['all_members']:
        ## if auth_user_id matches the member
        if member['id'] == auth_user_id:
            user_in_channel = True
            break
    return user_in_channel

def check_valid_user(data, u_id):
    """
    Checks whether a u_id refers to a valid user
    """
    valid_user = False
    for user in data['users']:
        if user['id'] == u_id:
            valid_user = True
            break
    return valid_user

def token_to_u_id(data, token):
    # find u_id related to token
    session_id = jwt.decode(token, SECRET, algorithms=['HS256'])
    for user in data['users']:
        for session in user['session_ids']:
            if session == session_id['session_ids']:
                return user['id']

def check_valid_dm(data, dm_id):
    valid_dm = False
    for dm in data['dms']:
        if dm['dm_id'] == dm_id:
            valid_dm = True
            break
    return valid_dm

def check_user_in_dm(data, u_id, dm_id):
    user_in_dm = False
    for member in data['dms'][dm_id]['members']:
        if member['id'] == u_id:
            user_in_dm = True
            break
    return user_in_dm