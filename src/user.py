'''
Implementation of user functions which includes user_profile_v1, user_profile_setname_v1,
user_profile_setemail_v1, user_profile_sethandle_v1, users_all_v1
Written by Kanit Srihakorth and Tharushi Gunawardana
'''

from flask import request
import jwt
import src.data as data
from src.error import InputError, AccessError
import re
import os
from PIL import Image
import urllib.request
from src.config import port
from datetime import datetime
from datetime import timezone
import requests
import time

SECRET = 'HELLO'

def user_profile_v1(token, u_id):
    """
    Description of function:
        Provides basic information of a user
    Parameters:
        token (str)
        u_id (int)
    Exceptions:
        InputError - if the u_id is not a valid user
        InputError - if token is invalid
    Returns:
        Dictionary 'profile' containing u_id, email, name_first, name_last and handle
    """
    valid = 0
    valid_token = 0
    profile = {}
    for t in data.data["token_list"]:
        if token == t:
            valid_token = 1
    #If token is valid, then profile dict is updated otherwise access error is thrown
    if valid_token == 1:
        decoded_token = jwt.decode(token, SECRET, algorithms=['HS256'])
        #Getting information for user profile
        for x in data.data["users"]:
                if u_id == x['u_id']:
                    valid = 1
                    for y in x["session_ids"]:
                        if decoded_token["session_id"] == y:
                            profile = {
                                'u_id': x['u_id'],
                                'email': x['email'],
                                'name_first': x['name_first'],
                                'name_last': x['name_last'],
                                'handle_str': x['handle_str']  
                            }
        #If u_id is not valid
        if valid == 0:
            raise InputError("Invalid user")
    else:
        raise InputError("Invalid token")
    return {'user': profile}

def user_profile_setname_v1(token, name_first, name_last):
    """
    Description of function:
        Changes firstname and lastname of a user
    Parameters:
        token (str)
        name_first (str)
        name_last (str)
    Exceptions:
        InputError - if name_first is invalid (less than 1 character or greater than 50 character)
        InputError - if token is invalid
        InputError - if name_last is invalid (less than 1 character or greater than 50 character)
    Returns:
        Empty dictionary
    """
    valid_token = 0
    for t in data.data["token_list"]:
        if token == t:
            valid_token = 1    
    #If token is valid, then profile dict is updated otherwise access error is thrown
    if valid_token == 1:
        decoded_token = jwt.decode(token, SECRET, algorithms=['HS256'])
        #Checks if name_first is valid
        if len(name_first) < 1 or len(name_first) > 50:
            raise InputError("Invalid firstname")
        #Checks if name_last is valid
        if len(name_last) < 1 or len(name_last) > 50:
            raise InputError("Invalid lastname")        
        #Updating user firstname and lastname
        for x in data.data["users"]:
            for y in x["session_ids"]:
                if decoded_token["session_id"] == y:
                    x['name_first'] = name_first
                    x['name_last'] = name_last 
    else:
        raise InputError("Invalid token")
    return {}    

def user_profile_setemail_v1(token, email):
    """
    Description of function:
        Changes email of a user
    Parameters:
        token (str)
        email (str)
    Exceptions:
        InputError - if email is invalid
        InputError - if token is invalid
        InputError - if email is already user by an existing user
    Returns:
        Empty dictionary
    """
    valid_token = 0
    for t in data.data["token_list"]:
        if token == t:
            valid_token = 1
    #If token is valid, then profile dict is updated otherwise access error is thrown
    if valid_token == 1:
        decoded_token = jwt.decode(token, SECRET, algorithms=['HS256'])
        regex = '^[a-zA-Z0-9]+[\\._]?[a-zA-Z0-9]+[@]\\w+[.]\\w{2,3}$'
        # Checks for valid email
        if re.search(regex, email):
            pass
        else:    
            raise InputError("Invalid email")
        #checking for if email is already used
        for x in data.data["users"]:
            if x["email"] == email:
                raise InputError("Email is already used")
            else:
                #Updating user email
                for y in x["session_ids"]:
                    if y == decoded_token["session_id"]:
                        x['email'] = email
    else:
        raise InputError("Invalid token")
    return {}
        


def user_profile_sethandle_v1(token, handle_str):
    """
    Description of function:
        Changes handle of a user
    Parameters:
        token (str)
        handle_str (str)
    Exceptions:
        InputError - if token is invalid
        InputError - if handle_str is invalid (less than 3 characters or greater than 20 characters)
    Returns:
        Empty dictionary
    """  
    valid_token = 0
    for t in data.data["token_list"]:
        if token == t:
            valid_token = 1
    #If token is valid, then profile dict is updated otherwise access error is thrown
    if valid_token == 1:
        decoded_token = jwt.decode(token, SECRET, algorithms=['HS256'])
        #Checks if handle_str is valid
        if len(handle_str) < 3 or len(handle_str) > 20:
            raise InputError("Invalid handle")
        for x in data.data['users']:
            #Checks if handle is already used
            if x['handle_str'] == handle_str:
                raise InputError("Handle already used")
            else:
                #Updates user handle
                for y in x["session_ids"]:
                    if y == decoded_token["session_id"]:
                        x['handle_str'] = handle_str
    else:
        raise InputError("Invalid token")
    return {}


def users_all_v1(token):
    """
    Description of function:
        Provides a list of all users information
    Parameters:
        token (str)
    Exceptions:
        InputError - if token is invalid
    Returns:
        A list containig all of the users and their information
    """
    valid_token = 0
    for t in data.data["token_list"]:
        if token == t:
            valid_token = 1
    #If token is valid, then profile dict is updated otherwise access error is thrown
    if valid_token == 1:
        all_users = []
        info = {}
        #Gets the user information
        for x in data.data["users"]:
            info['u_id'] = x['u_id']
            info['email'] = x['email']
            info['name_first'] = x['name_first']
            info['name_last'] = x['name_last']
            info['handle_str'] = x['handle_str']
            info['permission_id'] = x['permission_id']
            all_users.append(info)
    else:
        raise InputError("Invalid token")  
    return {'users': all_users}


def user_stats_v1(token):
    """
    Description of function:
        Provides a information on the involvement of the user in dreams (channels and dms joined and messages sent)
    Parameters:
        token (str)
    Exceptions:
        InputError - if token is invalid
    Returns:
        A dictionary containing channels_joined, dms_joined, messages_sent and involvement_rate
    """    
    valid = 0
    #Checking to see if token is valid
    for t in data.data['token_list']:
        if t == token:
            valid = 1
    if valid != 1:
        raise InputError("Invalid token")
    decoded_token = jwt.decode(token, SECRET, algorithms=['HS256'])
    #Finding the user
    for i in data.data["users"]:
        for j in i["session_ids"]:
            if decoded_token["session_id"] == j:
                u_id = i['u_id']
    # Getting number of channels user is in
    num_user_channels = data.data['users'][u_id]['num_channels']
    # Getting total number of channels
    total_channels = len(data.data['channels'])
    #Getting number of dms user is in
    num_user_dms = data.data['users'][u_id]['num_dms']
    #Getting total number of dms
    total_dms = 0
    for dm in data.data['dms']:
        if dm['dm_id'] != '':
            total_dms += 1
    #Getting number of messages user has sent
    num_user_messages = data.data['users'][u_id]['num_messages']
    #Getting total number of messages
    total_messages = len(data.data["message_ids"])
    #Calculating involvement rate
    numerator = num_user_messages + num_user_dms + num_user_channels
    denominator = total_channels + total_dms + total_messages
    involvement_rate = 0
    if denominator != 0:
        involvement_rate = float(numerator / denominator)
    #Getting the timestamp
    timestamp = int(time.time())
    new_stat = data.data['users'][u_id]['user_stats']
    if num_user_channels != data.data['users'][u_id]['user_stats']['channels_joined'][0]:
        new_stat['channels_joined'][0]['num_channels_joined'] = num_user_channels
        new_stat['channels_joined'][0]['timestamp'] = timestamp
    if num_user_dms != data.data['users'][u_id]['user_stats']['dms_joined'][0]:
        new_stat['dms_joined'][0]['num_dms_joined'] = num_user_dms
        new_stat['dms_joined'][0]['timestamp'] = timestamp
    if num_user_messages != data.data['users'][u_id]['user_stats']['messages_sent'][0]:
        new_stat['messages_sent'][0]['num_messages_sent'] = num_user_messages
        new_stat['messages_sent'][0]['timestamp'] = timestamp
    new_stat['involvement_rate'] = involvement_rate
    #Applying correct timestamps and adding new user_stats to data
    data.data['users'][u_id]['user_stats'] = new_stat
    return {'user_stats': new_stat}

def users_stats_v1(token):
    """
    Description of function:
        Provides a information on the utilization of dreams (channels, dms, messages currently existing)
    Parameters:
        token (str)
    Exceptions:
        InputError - if token is invalid
    Returns:
        A dictionary containing channels_exist dms_exist, messages_exist and utilization_rate
    """        
    valid = 0
    #Checking to see if token is valid
    for t in data.data['token_list']:
        if t == token:
            valid = 1
    if valid != 1:
        raise InputError("Invalid token")
    #Getting number of channels that currently exist
    total_channels = len(data.data['channels'])
    #Getting number of dms that currently exist
    existing_dms = 0
    for dm in data.data["dms"]:
        if dm["dm_id"] != '':
            existing_dms += 1
    #Getting number of existing messages
    existing_messages = 0
    for channel in data.data["channels"]:
        for message in channel["messages"]:
            if message["message"] != '':
                existing_messages += 1
    for dm2 in data.data["dms"]:
        for dm_message in dm2["messages"]:
            if dm_message["message"] != '':
                existing_messages += 1
    #Finding the users joined in at least one channel or dm
    num_users_in_channel_or_dm = 0
    for user in data.data['users']:
        if user['num_channels'] >= 1:
            num_users_in_channel_or_dm += 1
        elif user['num_dms'] >= 1:
            num_users_in_channel_or_dm += 1
    total_num_users = len(data.data['users'])
    utilization_rate = float(num_users_in_channel_or_dm / total_num_users)
    timestamp = int(time.time())
    if data.data['dreams_stats'] == {}:
        dreams_stats = {
            'channels_exist': [{
                'num_channels_exist': total_channels,
                'timestamp': timestamp
            }],
            'dms_exist': [{
                'num_dms_exist': existing_dms,
                'timestamp': timestamp
            }],
            'messages_exist': [{
                'num_messages_exist': existing_messages,
                'timestamp': timestamp
            }],
            'utilization_rate': utilization_rate
        }
        data.data['dreams_stats'] = dreams_stats
    else:
        if total_channels != data.data['dreams_stats']['channels_exist'][0]['num_channels_exist']:
            data.data['dreams_stats']['channels_exist'][0]['num_channels_exist'] = total_channels
            data.data['dreams_stats']['channels_exist'][0]['timestamp'] = timestamp
        if existing_dms != data.data['dreams_stats']['dms_exist'][0]['num_dms_exist']:
            data.data['dreams_stats']['dms_exist'][0]['num_dms_exist'] = existing_dms
            data.data['dreams_stats']['dms_exist'][0]['timestamp'] = timestamp
        if existing_messages != data.data['dreams_stats']['messages_exist'][0]['num_messages_exist']:
            data.data['dreams_stats']['messages_exist'][0]['num_messages_exist'] = existing_messages
            data.data['dreams_stats']['messages_exist'][0]['timestamp'] = timestamp
        data.data['dreams_stats']['utilization_rate'] = utilization_rate
    new_stats = data.data['dreams_stats']
    return {'dreams_stats': new_stats}

def user_profile_uploadphoto_v1(token, img_url, x_start, y_start, x_end, y_end):
    """
    Description of function:
        Uploads and crops a user's profile photo
    Parameters:
        token (str)
        img_url (str)
        x_start (int)
        y_start (int)
        x_end (int)
        y_end (int)
    Exceptions:
        InputError - if token is invalid
        InputError - if x dimensions are not within the photo size
        InputError - if y dimensions are not within the photo size
        InputError - if x_start and x_end are the same
        InputError - if y_start and y_end are the same
        InputError - if image is not JPG
        InputError - if image url is not valid
    Returns:
        An empty dictionary
    """       
    valid = 0
    #Checking to see if token is valid
    for t in data.data['token_list']:
        if t == token:
            valid = 1
    if valid != 1:
        raise InputError("Invalid token")
    #If token is valid then returns the users stats, otherwise raises input error
    decoded_token = jwt.decode(token, SECRET, algorithms=['HS256'])
    u_id = ''
    for x in data.data["users"]:
        for y in x["session_ids"]:
            if decoded_token["session_id"] == y:
                u_id = x['u_id']  
    #Checking if img_url ends with jpg
    regex = '.*jpg$'
    if re.search(regex, img_url):
        pass
    else:
        raise InputError("Invalid image url")
    #Checking if img_url return a 200 http_status
    try: 
        requests.get(img_url)
    except requests.exceptions.ConnectionError as invalid_url:    
        raise InputError("Image_url doesn't have a HTTP status of 200") from invalid_url
    #Downloaded the photo
    fullfilename = os.path.join("static", f"user{u_id}_photo.jpg")
    urllib.request.urlretrieve(img_url, fullfilename)
    image = Image.open(fullfilename)  
    width, height = image.size
    #Accounting for invalid x inputs
    if x_start > width or x_end > width or x_start < 0 or x_end < 0:
        raise InputError("Invalid x dimensions")
    if x_start == x_end:
        raise InputError("Invalid x dimensions")
    #Accounting for invalid y inputs
    if y_start > height or y_end > height or y_start < 0 or y_end < 0:
        raise InputError("Invalid y dimensions")
    if y_start == y_end:
        raise InputError("Invalid y dimensions")
    #Cropping image
    crop_image = image.crop((x_start,y_start,x_end,y_end))
    crop_image.save(fullfilename)
    #Adding link to data
    data.data["users"][u_id]["img_url"] = f'http://127.0.0.1:{port}/' + fullfilename
    return {}
