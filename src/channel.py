"""
First implementation of channel.py
channel_join_v1 and channel_messages_v1 authored by Jeremy Lee
"""
from src.data import data
from src.error import InputError
from src.error import AccessError
from src.helper import check_valid_channel
from src.helper import check_public_channel
from src.helper import check_user_in_channel

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
    # Check valid channel
    if check_valid_channel(data, channel_id) is False:
        raise InputError("Channel ID is not a valid channel")

    # Check if start is greater than number of messages in channel
    if start > len(data['channels'][channel_id]['messages']):
        raise InputError("Start is greater than the total number of messages in the channel")

    # Check if user is in channel
    if check_user_in_channel(data, channel_id, auth_user_id) is False:
        raise AccessError("Authorised user is not a member of channel with channel_id")

    messages = {}
    message_index = start
    for message in data['channels'][channel_id]['messages']:
        pass
    
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
