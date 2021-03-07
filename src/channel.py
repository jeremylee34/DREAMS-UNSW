"""
First iteration of channel.py
channel_join_v1 and channel_messages_v1 authored by Jeremy Lee
chanel_invite_v1 and channel_details authored by Roland Lin
"""
from src.data import data
from src.error import InputError
from src.error import AccessError
from src.helper import check_valid_channel
from src.helper import check_public_channel
from src.helper import check_user_in_channel

def channel_invite_v1(auth_user_id, channel_id, u_id): 
    #Loop through channels list to check if channel_id is valid 
    #raises InputError if not
    errorcount = 0
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            errorcount = errorcount + 1
    if errorcount == 0:
        raise InputError('channel_id does not refer to a valid channel')    
    #Loop through users list to check if u_id is valid
    #raises InputError if not
    errorcount = 0
    for users in data['users']:
        if users['id'] == u_id:
            errorcount = errorcount + 1
    if errorcount == 0:
        raise InputError('u_id does not refer to a valid user')    
    errorcount = 0
    #Checks if auth is a member of channel
    #Raises AccessError if not
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:            
            for idcheck in channel['all_members']:
                if idcheck['u_id'] == auth_user_id:
                    errorcount = errorcount + 1
    if errorcount == 0:
        raise AccessError('the authorised user is not already a member of the channel')                        
                                          
    #Append new_member dictionary to 'all_members' in channel    
    new_member = {
        "u_id": u_id,
        "name_first": data['users'][u_id]['firstname'],
        "name_last": data['users'][u_id]['Lastname']
    }
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            channel['all_members'].append(new_member)    
    return {}
            
               
   

def channel_details_v1(auth_user_id, channel_id):
    #Loop through channels list to check if channel_id is valid
    #raises InputError if not
    errorcount = 0
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            errorcount = errorcount + 1
    if errorcount == 0:
        raise InputError('Channel ID is not a valid channel')
    errorcount = 0
    #Check if auth is part of channel     
    #Raises AccessError if not
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            for member in channel['all_members']:
                if member['u_id'] == auth_user_id:
                    errorcount = errorcount + 1
    if errorcount == 0:
        raise AccessError('Authorised user is not a member of channel with channel_id')      
    #Make dictionary with required keys that is to be returned 
    channel_info = {
        "name": "",
        "owner_members": [],
        "all_members": []
    }
    #Searches for channel_id and copys info into channel_info
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            channel_info['name'] = channel['name']
            for owners in channel['owner_members']:
                channel_info['owner_members'].append(owners)
            for members in channel['all_members']:
                channel_info['all_members'].append(members)        
    return channel_info

"""
Given a channel_id that an authorised user is in, return up to 50 messages after
and including the "start" index. R

Arguments:
    auth_user_id (dict)    - unique id attributed to a particular member
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
def channel_messages_v1(auth_user_id, channel_id, start):
    # Check valid channel
    if check_valid_channel(data, channel_id) is False:
        raise InputError("Channel ID is not a valid channel")

    # Check if start is greater than number of messages in channel
    if start > len(data['channels'][channel_id]['messages']):
        raise InputError("Start is greater than the total number of messages in the channel")
    
    # Check if user is in channel
    if check_user_in_channel(data, channel_id, auth_user_id) is False:
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

def channel_leave_v1(auth_user_id, channel_id):
    return {
    }

"""
Given a channel_id of a channel that the authorised user can join, adds them to that channel

Arguments:
    auth_user_id (dict)    - unique id attributed to a particular member
    channel_id (dict)    - unique id attributeed to a particular channel

Exceptions:
    InputError  - Occurs when channel_id is not a valid channel
    AccessError - Occurs when channel_id refers to a channel that is private

Return Value:
    Returns nothing on all cases

"""
def channel_join_v1(auth_user_id, channel_id):
    # Check valid channel
    if check_valid_channel(data, channel_id) is False:
        raise InputError("Channel ID is not a valid channel")

    # Check whether channel accesible
    if check_public_channel(data, channel_id) is False:
        raise AccessError("channel_id refers to a channel that is private")

    ## search thru all members
    user_in_channel = check_user_in_channel(data, channel_id, auth_user_id)
    if user_in_channel is False:
        ## if user not added
        user_to_append = {
            'u_id' : auth_user_id,
            'name_first' : data['users'][auth_user_id]['firstname'],
            'name_last' : data['users'][auth_user_id]['Lastname'],
        }
        data['channels'][channel_id]['all_members'].append(user_to_append)
    else:
        pass
    return {
    }

def channel_addowner_v1(auth_user_id, channel_id, u_id):
    return {
    }

def channel_removeowner_v1(auth_user_id, channel_id, u_id):
    return {
    }
