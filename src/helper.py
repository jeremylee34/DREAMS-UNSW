from src.error import InputError
from src.error import AccessError
from src.data import data

import jwt

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

def check_user_in_channel(channel_id, auth_user_id):
    """
    Checks whether a user is in a channel
    """
    user_in_channel = False
    for member in data['channels'][channel_id]['all_members']:
        ## if auth_user_id matches the member
        if member['u_id'] == auth_user_id:
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
                return user['u_id']

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
            break
    return valid_token

def check_dreams_owner(u_id):
    dreams_owner = False
    for user in data['users']:
        if user['u_id'] == u_id:
            if user['permission_id'] == OWNER_PERMISSION:
                dreams_owner = True
                break
    return dreams_owner

