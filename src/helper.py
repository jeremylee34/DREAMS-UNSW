from src.error import InputError
from src.error import AccessError

def check_valid_channel(channel_id, data):
    valid_channel = False
    for channels in data['channels']:
        if channels['channel_id'] == channel_id:
            valid_channel = True
    if valid_channel is False:
        return False

def check_public_channel(channel_id, data):
    if data['channels'][channel_id]['is_public'] is False:
        return False