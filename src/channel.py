from src.error import InputError
from src.error import AccessError
from src.data import data

def channel_invite_v1(auth_user_id, channel_id, u_id):
    errorcount = 0
    #Checks if auth is a member of channel
    #Raises AccessError if not
    for channel in data['channels']
        membersall = channel.get('all_members']
        for member in membersall:
            if member == auth_user_id:
                errorcount = errorcount + 1
            if errorcount = 0:
                raise AccessError('the authorised user is not already a member of the channel')
    #Loop through users list to check if u_id is valid
    errorcount = 0
    for users in data['users']:
        if users['id'] == u_id:
            errorcount = errorcount + 1
    if errorcount == 0:
        raise InputError('u_id does not refer to a valid user')                            
    #Loop through channels list to check if channel_id is valid 
    #If found, append the u_id to all_members in the channel 
    errorcount = 0
    for channel in data['channels']:
        if channels['channel_id'] == channel_id:
            channels['all_members'].append(u_id)
            errorcount = errorcount + 1   
    if errorcount == 0:
        raise InputError('channel_id does not refer to a valid channel')                                       
    return {}

def channel_details_v1(auth_user_id, channel_id):
    return {
        'name': 'Hayden',
        'owner_members': [
            {
                'u_id': 1,
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
            }
        ],
        'all_members': [
            {
                'u_id': 1,
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
            }
        ],
    }

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
