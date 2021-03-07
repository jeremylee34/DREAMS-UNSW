"""
First implementation of channel.py
channel_join_v1 and channel_messages_v1 authored by Jeremy Lee
"""
from src.data import data
from src.error import InputError
from src.error import AccessError

def channel_invite_v1(auth_user_id, channel_id, u_id):
    return {
    }

def channel_details_v1(auth_user_id, channel_id):
    """
    returns channel details
    """
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
    """
    returns channel messages
    """
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
    """
    joins a user to a channel
    """
    if data['channels'][channel_id['channel_id']]['is_public'] is False:
        raise AccessError
    user_in_channel = False
    ## search thru all members
    for i in range(len(data['channels'][channel_id['channel_id']]['all_members'])):
        ## if auth_user_id matches the member
        if data['channels'][channel_id['channel_id']]['all_members'][i]['u_id'] == auth_user_id:
            user_in_channel = True
    if user_in_channel is False:
        ## if user not added
        user_to_append = {
            'u_id' : auth_user_id,
            'name_first' : data['users'][auth_user_id][firstname],
            'name_last' : data['users'][auth_user_id][Lastname],
        }
        data['channels'][channel_id['channel_id']]['all_members'].append(user)
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
