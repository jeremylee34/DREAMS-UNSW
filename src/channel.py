from src.error import InputError
from src.error import AccessError
from src.data import data

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


def channel_messages_v1(auth_user_id, channel_id, start):
    return {
        'messages': [
            {
                'message_id': 1,
                'u_id': 1,
                'message': 'Hello world',
                'time_created': 1582426789,
            }
        ],
        'start': 0,
        'end': 50,
    }

def channel_leave_v1(auth_user_id, channel_id):
    return {
    }

def channel_join_v1(auth_user_id, channel_id):
    return {
    }

def channel_addowner_v1(auth_user_id, channel_id, u_id):
    return {
    }

def channel_removeowner_v1(auth_user_id, channel_id, u_id):
    return {
    }
