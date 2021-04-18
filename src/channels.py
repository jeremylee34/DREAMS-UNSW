'''
Implementation of channels functions which includes channels_list_v1,
channels_listall_v1 and channels_create_v1.
Written by Gordon Liang
'''
import jwt
from src.error import InputError
from src.error import AccessError
from src.data import data

SECRET = 'HELLO'

def channels_list_v1(token):
    '''
    This function lists all the channels that a user is in
    Arguments:
        token (str) - contains a session_id which is used to get user_id
    Exceptions:
        AccessError - when auth_user_id does not exist
    Return Value:
        Returns 'channels'
    '''
    valid = 0
    # Checking if token is valid
    for tokens in data['token_list']:
        if tokens == token:
            valid = 1
    if valid != 1:
        raise InputError('User does not exist')
    # Getting auth_user_id from token
    payload = jwt.decode(token, SECRET, algorithms=['HS256'])
    session_id = payload['session_id']
    for user in data['users']:
        for s_id in user['session_ids']:
            if s_id == session_id:
                auth_user_id = user['u_id']
    # List of channels that user is in
    channel_list = []
    # Loops through channel list
    for channel in data['channels']:
        member_list = channel.get('all_members')
        # Loops through all members and checks if auth_user_id is included
        for member in member_list:
            # If the user is found, the channel is added to channel_list
            if member['u_id'] == auth_user_id:
                channel_dict = {}
                channel_dict['channel_id'] = channel['channel_id']
                channel_dict['name'] = channel['name']
                channel_list.append(channel_dict)
    return {'channels': channel_list}

def channels_listall_v1(token):
    '''
    This function lists all the channels
    Arguments:
        token (str) - contains a session_id which is used to get user_id
    Exceptions:
        AccessError - when auth_user_id does not exist
    Return Value:
        Returns 'channels'
    '''
    valid = 0
    # Checking if token is valid
    for tokens in data['token_list']:
        if tokens == token:
            valid = 1
    if valid != 1:
        raise InputError('User does not exist')
    channel_list = []
    # Loops through the data and adds every into the channel list
    for channel in data['channels']:
        channel_dict = {}
        channel_dict['channel_id'] = channel['channel_id']
        channel_dict['name'] = channel['name']
        channel_list.append(channel_dict)
    return {'channels': channel_list}

def channels_create_v1(token, name, is_public):
    '''
    This function creates a channel and adds it to the data file
    Arguments:
        token (str) - contains a session_id which is used to get user_id
        name (str) - name of the channel
        is_public (bool) - determines if channel is public or private
    Exceptions:
        InputError - Occurs when channel name is more than 20 characters long
        InputError - Occurs when no channel name is entered
        AccessError - when auth_user_id does not exist
    Return Value:
        Returns 'channel_id'
    '''
    valid = 0
    # Checking if token is valid
    for tokens in data['token_list']:
        if tokens == token:
            valid = 1
    if valid != 1:
        raise InputError('User does not exist')
    # Gets auth_user_id from token
    payload = jwt.decode(token, SECRET, algorithms=['HS256'])
    session_id = payload['session_id']
    for user in data['users']:
        for s_id in user['session_ids']:
            if s_id == session_id:
                auth_user_id = user['u_id']
    # Produces an error if channel name is greater than 20 characters
    if len(name) > 20:
        raise InputError('Name is more than 20 characters long')
    # Produces an error if no channel name is entered
    if len(name) == 0:
        raise InputError('Cannot have no channel name')
    # Creating a channel that includes all the keys
    new_channel = {
        "name": name,
        "is_public": is_public,
        "channel_id": len(data['channels']),
        "owner_members": [
            {
                'u_id': auth_user_id,
                'name_first': data['users'][auth_user_id]['name_first'],
                'name_last': data['users'][auth_user_id]['name_last'],
                'email': data['users'][auth_user_id]['email'],
                'handle_str': data['users'][auth_user_id]['handle_str']
            }
        ],
        "all_members": [
            {
                'u_id': auth_user_id,
                'name_first': data['users'][auth_user_id]['name_first'],
                'name_last': data['users'][auth_user_id]['name_last'],
                'email': data['users'][auth_user_id]['email'],
                'handle_str': data['users'][auth_user_id]['handle_str']
            }
        ],
        "messages": []
    }
    channel_id = len(data['channels'])
    # Adds the new channel to the data list
    data['channels'].append(new_channel)
    data['users'][auth_user_id]['num_channels'] += 1
    return {'channel_id': channel_id}


    ##############################
    ### ADD SRC AFTER FINISHED ###
    ##############################