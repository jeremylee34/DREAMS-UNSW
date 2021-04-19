from src.error import InputError
from src.error import AccessError
from src.data import data

import jwt
import random
import string
from re import search
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
    global data
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

def generate_secret_code(email):
    '''
    return generated secret code, 6 characters,
    mixture of uppercase letters and digits
    ''' 
    #loop through and see if email match any in database 
    valid_mail = 0
    for user in data['users']:
        if email == user['email']:
            valid_mail = 1
    
    if valid_mail == 0:
        raise InputError('Invalid email')
    else:
        random_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

        #attach random_str to user data
        for user in data['users']:
            if email == user['email']:
                user['secret_code'] = random_str

        return random_str

def check_secret_code(secret):
    '''
    check if secret code is valid, 
    return 1 if valid,
    return 0 if invalid
    '''
    if len(secret) == 6:
        for letter in secret:
            if letter in (string.ascii_uppercase + string.digits): 
                return 1
    return 0

def get_secret_code(u_id):
    '''
    Return user's secret code if any
    '''
    secret_code_exist = 0
    for user in data['users']:
        if user['u_id'] == u_id:
            secret_code = user['secret_code']
            secret_code_exist = 1
    if secret_code_exist == 0:
        raise InputError('No secret code in this u_id')

    return secret_code
