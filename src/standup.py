from src.error import InputError, AccessError
from src.data import data
from src.user import user_profile_v1
from src.message import message_send_v1
from src.helper import token_to_u_id
from src.helper import check_valid_channel
from src.helper import check_valid_token
from src.helper import check_user_in_channel
# from src.helper import end_standup

from datetime import datetime
from datetime import timedelta
from datetime import timezone

import time
import threading

def standup_start_v1(token, channel_id, length):

    # record the finishing time, create standup in channels and sleep
    time_finish = datetime.now() + timedelta(seconds=length)
    curr_time = time_finish.replace(tzinfo=timezone.utc).timestamp()

    if check_valid_token(token) == False:
        raise InputError("token does not refer to a valid token")
    owner_u_id = token_to_u_id(token)
    #Loop through channels list to check if channel_id is valid
    #raises InputError if not
    if check_valid_channel(channel_id) is False:
        raise InputError('channel_id does not refer to a valid channel')
    #Checks if an active standup is already running in the channel
    if data['channels'][channel_id]['active_standup'] is True:
        raise InputError('an active standup is currently running in this channel')
    #Checks if auth is a member of channel
    #Raises AccessError if not
    if check_user_in_channel(channel_id, owner_u_id) is False:
        raise AccessError('the authorised user is not already a member of the channel')
    
    data['channels'][channel_id]['active_standup'] = True
    data['channels'][channel_id]['standup_time_finish'] = curr_time
    
    t = threading.Timer(length, end_standup, args=[channel_id, curr_time, owner_u_id, token])
    if t.is_alive():
        t.cancel()
    t.start()

    return {
        'time_finish': curr_time
    }

def end_standup(channel_id, curr_time, owner_u_id, token):
    if check_valid_channel is False:
        raise InputError('channel_id does not refer to a valid channel')
    temp_channel = data['channels'][channel_id]
    data['channels'][channel_id]['standup'].clear
    data['channels'][channel_id]['active_standup'] = False
    data['channels'][channel_id]['standup_time_finish'] = 0
    # once timer ends, run this code 
    if data['channels'][channel_id]['standup']:

        message_block = []
        for msg in temp_channel['standup']:
            new_msg = f"{msg['handle_str']}: {msg['message']}"
            message_block.append(new_msg)
        message_block_joined = '\n'.join(message_block)
        message_send_v1(token, channel_id, message_block_joined)
    return{}

def standup_active_v1(token, channel_id):
    if check_valid_token(token) == False:
        raise InputError("token does not refer to a valid token")
    #Loop through channels list to check if channel_id is valid
    #raises InputError if not
    if check_valid_channel(channel_id) is False:
        raise InputError('channel_id does not refer to a valid channel')
    active_status = data['channels'][channel_id]['active_standup']
    if active_status is False:
        time_finish = None
    else:
        time_finish = data['channels'][channel_id]['standup_time_finish']
    
    return {
        'is_active': active_status,
        'time_finish': time_finish
    }

def standup_send_v1(token, channel_id, message):
    if check_valid_token(token) == False:
        raise InputError("token does not refer to a valid token")
    u_id = token_to_u_id(token)
    #Loop through channels list to check if channel_id is valid
    #raises InputError if not
    if check_valid_channel(channel_id) is False:
        raise InputError('channel_id does not refer to a valid channel')
    #Checks if an active standup is already running in the channel
    if data['channels'][channel_id]['active_standup'] is False:
        raise InputError('an active standup is not currently running in this channel')
    #check is msg is longer than 1000 characters
    if len(message) > 1000:
        raise InputError('Message is more than 1000 characters')
    #Checks if auth is a member of channel
    #Raises AccessError if not
    if check_user_in_channel(channel_id, u_id) is False:
        raise AccessError('the authorised user is not already a member of the channel')
    
    profile = user_profile_v1(token, u_id)
    new_msg = {
        'handle_str': profile['user']['handle_str'],
        'message': message
    }
    data['channels'][channel_id]['standup'].append(new_msg)
    return {}
