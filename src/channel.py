"""
First iteration of channel.py
channel_join_v1 and channel_messages_v1 authored by Jeremy Lee
chanel_invite_v1 and channel_details authored by Roland Lin
"""
from src.data import data
from src.error import InputError
from src.error import AccessError
from src.user import user_profile_v1
from src.helper import check_valid_channel
from src.helper import check_public_channel
from src.helper import check_user_in_channel
from src.helper import token_to_u_id
from src.helper import check_owner_perm
from src.helper import check_if_owner
from src.helper import check_valid_user
from src.helper import check_valid_token

import jwt

GLOBAL_OWNER = 0
DREAMS_OWNER = 0
OWNER_PERMISSION = 1
SECRET = "HELLO"

def channel_invite_v1(token, channel_id, u_id):
    """
    <This function adds the user with u_id to the channel with channel_id owned by u_id>

    Arguments:
        token (string)    - an encoded session_id used to identify a user's session
        channel_id (integer)    - <unique id used to identify the particular
        channel the u_id is being added to>
        u_id (integer)    - <unique id used to identify the user who is being
        added to the channel>

    Exceptions:
        InputError - Occurs when channel_id does not refer to a valid channel or
        when u_id does not refer to a valid user
        AccessError - Occurs when the user with input u_id is not in the
        channel with input channel_id

    Return Value:
        Returns <{}> on u_id being succesfully added to channel with channel_id
    """
    if check_valid_token(token) == False:
        raise InputError("token does not refer to a valid token")
    owner_u_id = token_to_u_id(token)
    #Loop through channels list to check if channel_id is valid
    #raises InputError if not
    if check_valid_channel(channel_id) is False:
        raise InputError('channel_id does not refer to a valid channel')
    #Loop through users list to check if u_id is valid
    #raises InputError if not
    if check_valid_user(u_id) is False:
        raise InputError('u_id does not refer to a valid user')
    #Checks if auth is a member of channel
    #Raises AccessError if not
    if check_user_in_channel(channel_id, owner_u_id) is False:
        raise AccessError('the authorised user is not already a member of the channel')

    #Append new_member dictionary to 'all_members' in channel
    new_member = {
        "u_id": u_id,
        "name_first": data['users'][u_id]['name_first'],
        "name_last": data['users'][u_id]['name_last']
    }
    new_notification = {
        "u_id": owner_u_id,
        "message": "",
        "channel_id": channel_id,
        "dm_id": -1
    }
    data['notifications'].append(new_notification)
    data['channels'][channel_id]['all_members'].append(new_member)

    return {}


def channel_details_v1(token, channel_id):
    """
    <This function returns details of the channel with channel_id that the user
    with token is part of>

    Arguments:
        token (string)    - an encoded session_id used to identify a user's session
        channel_id (integer)    - <unique id used to identify the particular
        channel that the u_id is retrieving details on>

    Exceptions:
        InputError - Occurs when channel_id does not refer to a valid channel
        AccessError - Occurs when the user with input u_id is not a
        member of the channel with input channel_id

    Return Value:
        Returns <name> on u_id being part of channel with channel_id
        and channel_id being valid
        Returns <owner_members> on u_id being part of channel with
        channel_id and channel_id being valid
        Returns <all_members> on u_id being part of channel with
        channel_id and channel_id being valid
    """
    if check_valid_token(token) == False:
        raise InputError("token does not refer to a valid token")
    u_id = token_to_u_id(token)
    #Loop through channels list to check if channel_id is valid
    #raises InputError if not
    if check_valid_channel(channel_id) is False:
        raise InputError("Channel ID is not a valid channel")
    #Checks if auth is a member of channel
    #Raises AccessError if not
    if check_user_in_channel(channel_id, u_id) is False:
        raise AccessError('the authorised user is not already a member of the channel')

    #Make dictionary with required keys that is to be returned
    channel_info = {
        "name": "",
        "is_public": data['channels'][channel_id]['is_public'],
        "owner_members": [],
        "all_members": []
    }
    #Searches for channel_id and copys info into channel_info
    channel = data['channels'][channel_id]
    channel_info['name'] = channel['name']
    for owners in channel['owner_members']:
        channel_info['owner_members'].append(owners)
    for members in channel['all_members']:
        channel_info['all_members'].append(members)
    return channel_info


def channel_messages_v1(token, channel_id, start):
    """
    Given a channel_id that an authorised user is in, return up to 50 messages after
    and including the "start" index.

    Arguments:
        token (string)    - an encoded session_id used to identify a user's session
        channel_id (dict)    - unique id attributeed to a particular channel
        start (int) - what index the message capture should start at

    Exceptions:
        InputError  - Occurs when channel_id is not a valid channel
        InputError - Occurs when start is greater than total number of messages in channel
        AccessError - Occurs when authorised user is not a member of channel with channel_id

    Return Value:
        Returns a list of message dictionaries, a start index and an end index (start + 50)
        if not yet at end of all messages in channel
        Returns a list of message dictionaries, a start index and an end index (-1)
        if reached end of all messages in channel
    """
    if check_valid_token(token) == False:
        raise InputError("token does not refer to a valid token")
    # Check valid channel
    if check_valid_channel(channel_id) is False:
        raise InputError("Channel ID is not a valid channel")
    # Check if start is greater than number of messages in channel
    length_messages = len(data['channels'][channel_id]['messages'])
    if start == 0 and length_messages == 0:
        return {
            'messages': [],
            'start': start,
            'end': 0
        }
    if start >= length_messages:
        raise InputError("Start is greater than the total number of messages in the channel")
    u_id = token_to_u_id(token)
    # Check if user is in channel
    if check_user_in_channel(channel_id, u_id) is False:
        raise AccessError("Authorised user is not a member of channel with channel_id")

    messages = []
    message_index = start
    message_index_end = start + 50
    for message in data['channels'][channel_id]['messages']:
        temp_message = {
            'message_id': message['message_id'],
            'u_id': message['u_id'],
            'message': message['message'],
            'time_created': message['time_created']
        }
        messages.append(temp_message)
        # iterate to next index, if past 50 msgs, end loop
        message_index += 1
        if message_index == message_index_end:
            break

    # if reached end of messages before capturing 50 messages, set to -1
    if message_index != message_index_end:
        message_index_end = -1

    return {
        'messages': messages,
        'start': start,
        'end': message_index_end
    }

def channel_leave_v1(token, channel_id):
    """
    Given a channel ID, user is removed as a member of this channel. 

    Arguments:
        token (string)    - an encoded session_id used to identify a user's session
        channel_id (dict)    - unique id attributeed to a particular channel

    Exceptions:
        InputError  - Occurs when channel_id is not a valid channel
        AccessError - Occurs when authorised user is not a member of channel with channel_id

    Return Value:
        Returns nothing on all cases
    """
    
    if check_valid_token(token) == False:
        raise InputError("token does not refer to a valid token")
    u_id = token_to_u_id(token)
    # Check valid channel
    if check_valid_channel(channel_id) is False:
        raise InputError("Channel ID is not a valid channel")
    # Check if user is in channel
    if check_user_in_channel(channel_id, u_id) is False:
        raise AccessError("Authorised user is not a member of channel with channel_id")

    for user in data['channels'][channel_id]['owner_members']:
        if user['u_id'] == u_id:
            if len(data['channels'][channel_id]['owner_members']) > 1:
                data['channels'][channel_id]['owner_members'].remove(user)  

    for user in data['channels'][channel_id]['all_members']:
        if user['u_id'] == u_id:
            if len(data['channels'][channel_id]['all_members']) > 1:
                data['channels'][channel_id]['all_members'].remove(user)
    return {
    }


def channel_join_v1(token, channel_id):
    """
    Given a channel_id of a channel that the authorised user can join, adds them to that channel

    Arguments:
        token (string)    - an encoded session_id used to identify a user's session
        channel_id (dict)    - unique id attributeed to a particular channel

    Exceptions:
        InputError  - Occurs when channel_id is not a valid channel
        AccessError - Occurs when channel_id refers to a channel that is private

    Return Value:
        Returns nothing on all cases
    """
    
    if check_valid_token(token) == False:
        raise InputError("token does not refer to a valid token")
    u_id = token_to_u_id(token)
    # Check valid channel
    if check_valid_channel(channel_id) is False:
        raise InputError("Channel ID is not a valid channel")
    
    # Check whether channel accesible
    if check_owner_perm(u_id) == True:
        pass
    elif check_public_channel(channel_id) is False:
        raise AccessError("channel_id refers to a channel that is private")

    ## search thru all members
    user_in_channel = check_user_in_channel(channel_id, u_id)
    if user_in_channel is False:
        ## if user not added
        user_to_append = {
            'u_id' : u_id,
            'name_first' : data['users'][u_id]['name_first'],
            'name_last' : data['users'][u_id]['name_last'],
        }
        data['channels'][channel_id]['all_members'].append(user_to_append)
    else:
        pass
    return {
    }

def channel_addowner_v1(token, channel_id, u_id):
    """
    Make user with user id u_id an owner of this channel

    Arguments:
        token (string)    - an encoded session_id used to identify a user's session
        channel_id (dict)    - unique id attributeed to a particular channel
        u_id (integer)    - <unique id used to identify the user who is being added as owner

    Exceptions:
        InputError  - Occurs when channel_id is not a valid channel
        InputError  - Occurs when user with user id u_id is already an owner of the channel
        AccessError - Occurs when when the authorised user is not an owner of 
        the **Dreams**, or an owner of this channel
      
    Return Value:
        Returns nothing on all cases
    """
    
    if check_valid_token(token) == False:
        raise InputError("token does not refer to a valid token")
    author_id = token_to_u_id(token)
    # Check valid channel
    if check_valid_channel(channel_id) is False:
        raise InputError("Channel ID is not a valid channel")
    # Check if u_id is already owner
    if check_if_owner(u_id, channel_id) is True:
        raise InputError("user with user id u_id is already an owner of the channel")
    
    # Check if person with token is dreams owner or owner of channel
    if author_id == DREAMS_OWNER:
        pass
    elif check_if_owner(author_id, channel_id) is False:
        raise AccessError("The authorised user is not an owner of the **Dreams**, or an owner of this channel")
    s_id = data['users'][u_id]['session_ids'][0]
    s_token = jwt.encode({'session_id': s_id}, SECRET, algorithm='HS256')
    profile = user_profile_v1(s_token, u_id)
    data['channels'][channel_id]['owner_members'].append(profile)

    if check_user_in_channel(channel_id, u_id) is False:
        data['channels'][channel_id]['all_members'].append(profile)
        
    return {
    }

def channel_removeowner_v1(token, channel_id, u_id):
    """
    Remove user with user id u_id an owner of this channel

    Arguments:
        token (string)    - an encoded session_id used to identify a user's session
        channel_id (dict)    - unique id attributeed to a particular channel
        u_id (integer)    - <unique id used to identify the user who is being removed as owner

    Exceptions:
        InputError  - Occurs when channel_id is not a valid channel
        InputError  - Occurs when user with user id u_id is not already an owner of the channel
        InputError  - Occurs when the user is currently the only owner
        AccessError - Occurs when when the authorised user is not an owner of 
        the **Dreams**, or an owner of this channel
      
    Return Value:
        Returns nothing on all cases
    """
    
    if check_valid_token(token) == False:
        raise InputError("token does not refer to a valid token")
    author_id = token_to_u_id(token)
    # Check valid channel
    if check_valid_channel(channel_id) is False:
        raise InputError("Channel ID is not a valid channel")
    # Check if user with u_id is an owner in the first place
    if check_if_owner(u_id, channel_id) is False:
        raise InputError("user with user id u_id is not an owner of the channel.")
    
    # Check if user is the only owner
    if len(data['channels'][channel_id]['owner_members']) == 1:
        raise InputError("User is currently the only owner")\
    # Check if person with token is dreams owner or owner of channel
    if author_id == DREAMS_OWNER:
        pass
    elif check_if_owner(author_id, channel_id) is False:
        raise AccessError("The authorised user is not an owner of the **Dreams**, or an owner of this channel")

    for owner_member in data['channels'][channel_id]['owner_members']:
        if owner_member['u_id'] == u_id:
            data['channels'][channel_id]['owner_members'].remove(owner_member)

    return {
    }
