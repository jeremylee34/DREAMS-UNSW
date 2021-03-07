from src.error import InputError
from src.error import AccessError

def check_valid_channel(data, channel_id):
    valid_channel = False
    for channels in data['channels']:
        if channels['channel_id'] == channel_id:
            valid_channel = True
    if valid_channel is False:
        return False

def check_public_channel(data, channel_id):
    if data['channels'][channel_id]['is_public'] is False:
        return False

def check_user_in_channel(data, channel_id, auth_user_id):
    user_in_channel = False
    for member in data['channels'][channel_id]['all_members']:
        ## if auth_user_id matches the member
        if member['u_id'] == auth_user_id:
            user_in_channel = True
    return user_in_channel