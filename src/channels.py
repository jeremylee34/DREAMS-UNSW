from src.error import InputError
from src.data import data

def channels_list_v1(auth_user_id):
    channel_list = []
    for channel in data['channels']:
        member_list = channel.get('all_members')
        for member in member_list:
            if member == auth_user_id:
                channel_list.append(channel)
    return {
        'channels': channel_list
    }

def channels_listall_v1(auth_user_id):
    channel_list = []
    for channel in data['channels']:
        channel_list.append(channel)
    return {
        'channels': channel_list
    }

def channels_create_v1(auth_user_id, name, is_public):
    if len(name) > 20:
        raise InputError('Name is more than 20 characters long')
    if len(name) == 0:
        raise InputError('Cannot have no channel name')
    new_channel = {
        "name": name,
        "is_public": is_public,
        "id": len(data['channels']),
        "owner_members": [auth_user_id,],
        "all_members": [],
    }
    id = len(data['channels'])
    data['channels'].append(new_channel)
    return {
        'channel_id': id,
    }
