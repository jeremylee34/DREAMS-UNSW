
'''
Implementation of other functions which includes clear_v1,
search_v1, notifications_get_v1
Written by Kanit Srihakorth and Tharushi Gunawardana
'''
import requests
import jwt
from src.database import data
from src.channel import channel_messages_v1
from src.channels import channels_list_v1

from src.error import InputError, AccessError

def clear_v1():
    """
    Description of function:
        Removes all existing users and their information
    Parameters:
        None
    Exceptions:
        None
    Returns:
        Empty dictionary
    """           
    for x in data["users"]:
        x["session_ids"].clear()
    data['users'].clear()
    data['channels'].clear()
    data['dms'].clear() 
    data['message_ids'].clear() 
    data['token_list'].clear()
    data['notifications'].clear()
    return {}

def search_v1(token, query_str):
    """
    Description of function:
        Given query string, return collection of messages
        in all channel/DMs that user joined that matched query
    Parameters:
        token (str)
        query_str (str)
    Exceptions:
        InputError - if query_str is above 1000 characters
    Returns:
        dictionary of message_id, u_id, message, time_created 
    """
    valid = 0
    for tokens in data['token_list']:
        if tokens == token:
            valid = 1
    if valid != 1:
        raise AccessError('User does not exist')

    msg_list = []
    token = jwt.decode(token, 'HELLO', algorithms=['HS256'])

    if len(query_str) > 1000:
        raise InputError("query_str is above 1000 characters")

    for user in data['users']:
        for session in user['session_ids']:
            if session == token["session_id"]:
                for channel in data['channels']:
                    for message in channel['messages']:
                        if query_str == message['message']:
                            msg_list.append(message)
                for dm in data['dms']:
                    for dm_message in dm['messages']:
                        if query_str == dm_message['message']:
                            msg_list.append(dm_message)

    return {
       'messages': msg_list
    } 

def notifications_get_v1(token):
    """
    Description of function:
        Remove the user(u_id) from the Dreams. 
        Must have authority to do so, being admin.
    Parameters:
        token (str)
        u_id (int)
    Exceptions:
        InputError - if the u_id is not a valid user
        AccessError - Authorised user isn't an owner
    Returns:
        Blank dictionary
    """
    valid = 0
    for tokens in data['token_list']:
        if tokens == token:
            valid = 1
    if valid != 1:
        raise AccessError('User does not exist')

    decoded_token = jwt.decode(token, 'HELLO', algorithms=['HS256'])
    msg_list = []
    notification_num = 0
    #check if valid
    for user in data['users']:
        for session in user['session_ids']:
            if session == decoded_token["session_id"]:
                handle = user['handle_str']
                for notification in data['notifications']:
                    if notification_num == 20:
                        break
                    handle_from = data['users'][notification['u_id']]['handle_str']
                    if f'@{handle}' in notification['message']:
                        if notification['channel_id'] == -1:
                            dm_name = data['dms'][notification['channel_id']]['name']
                            new_dict = {
                                'channel_id': notification['channel_id'],
                                'dm_id': notification['dm_id'],
                                'notification_message': f"{handle_from} tagged you in {dm_name}: {notification['message'][:20]}",
                            }
                        else:
                            channel_name = data['channels'][notification['channel_id']]['name']
                            new_dict = {
                                'channel_id': notification['channel_id'],
                                'dm_id': notification['dm_id'],
                                'notification_message': f"{handle_from} tagged you in {channel_name}: {notification['message'][:20]}",
                            }
                        msg_list.append(new_dict)
                    #notification['message'] == '' and not @:
                    else:
                        if notification['channel_id'] == -1:
                            dm_name = data['dms'][notification['channel_id']]['name']
                            new_dict = {
                                'channel_id': notification['channel_id'],
                                'dm_id': notification['dm_id'],
                                'notification_message': f"{handle_from} added you to {dm_name}"
                            }
                        else:
                            channel_name = data['channels'][notification['channel_id']]['name']
                            new_dict = {
                                'channel_id': notification['channel_id'],
                                'dm_id': notification['dm_id'],
                                'notification_message': f"{handle_from} added you to {channel_name}"
                            }
                        msg_list.append(new_dict)
                    notification_num += 1
    return {
        'notifications': msg_list
    }
