from src.error import InputError
from src.error import AccessError
from src.data import data
''' 
This function lists all the channels that a user is in
Arguments:
    auth_user_id (int) - id of the user
Exceptions:
    
Return Value:
    Returns 'channels' 
'''
def channels_list_v1(auth_user_id):
    # Checks if auth_user_id exists
    valid = 0
    for users in data['users']:
        if users['id'] == auth_user_id:
            valid = 1
    if valid == 0:
        raise AccessError
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
    return {
        'channels': channel_list
    }
''' 
This function lists all the channels
Arguments:
    auth_user_id (int) - id of the user
Exceptions:
    
Return Value:
    Returns 'channels' 
'''
def channels_listall_v1(auth_user_id):
    # Checks if auth_user_id exists
    valid = 0
    for users in data['users']:
        if users['id'] == auth_user_id:
            valid = 1
    if valid == 0:
        raise AccessError
    channel_list = []
    # Loops through the data and adds every into the channel list
    for channel in data['channels']:
        channel_dict = {}
        channel_dict['channel_id'] = channel['channel_id']
        channel_dict['name'] = channel['name']
        channel_list.append(channel_dict)
    return {
        'channels': channel_list
    }
''' 
This function creates a channel and adds it to the data file
Arguments:
    auth_user_id (int) - id of the user
    name (string) - name of the channel
    is_public (bool) - determines if channel is public or private
Exceptions:
    InputError - Occurs when channel name is more than 20 characters long
    InputError - Occurs when no channel name is entered
Return Value:
    Returns 'channel_id' 
'''
def channels_create_v1(auth_user_id, name, is_public):
    # Checks if auth_user_id exists
    valid = 0
    for users in data['users']:
        if users['id'] == auth_user_id:
            valid = 1
    if valid == 0:
        raise AccessError
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
                'name_first': data['users'][auth_user_id]['firstname'],
                'name_last': data['users'][auth_user_id]['Lastname']
            }
        ],
        "all_members": [
            {
                'u_id': auth_user_id,
                'name_first': data['users'][auth_user_id]['firstname'],
                'name_last': data['users'][auth_user_id]['Lastname']
            }
        ],
        "messages": []
    }
    id = len(data['channels'])
    # Adds the new channel to the data list
    data['channels'].append(new_channel)
    return {
        'channel_id': id
    }
