'''
Implementation of user functions which includes user_profile_v1, user_profile_setname_v1,
user_profile_setemail_v1, user_profile_sethandle_v1, users_all_v1
Written by Kanit Srihakorth and Tharushi Gunawardana
'''
from flask import request
import jwt
from data import data
from error import InputError, AccessError
import re
from auth import auth_register_v1
import os
from PIL import Image
import urllib.request
from config import port
from channels import channels_list_v1
import dm
from channels import channels_listall_v1
from datetime import datetime
from datetime import timezone

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
    Returns:
        Dictionary 'profile' containing u_id, email, name_first, name_last and handle
    """
    valid = 0
    valid_token = 0
    profile = {}
    for t in data["token_list"]:
        if token == t:
            valid_token = 1
    #If token is valid, then profile dict is updated otherwise access error is thrown
    if valid_token == 1:
        decoded_token = jwt.decode(token, SECRET, algorithms=['HS256'])
        #Getting information for user profile
        for x in data["users"]:
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
        InputError - if name_last is invalid (less than 1 character or greater than 50 character)
    Returns:
        Empty dictionary
    """
    valid_token = 0
    for t in data["token_list"]:
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
        for x in data["users"]:
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
        InputError - if email is already user by an existing user
    Returns:
        Empty dictionary
    """
    valid_token = 0
    for t in data["token_list"]:
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
        for x in data["users"]:
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
        InputError - if handle_str is invalid (less than 3 characters or greater than 20 characters)
    Returns:
        Empty dictionary
    """  
    valid_token = 0
    for t in data["token_list"]:
        if token == t:
            valid_token = 1
    #If token is valid, then profile dict is updated otherwise access error is thrown
    if valid_token == 1:
        decoded_token = jwt.decode(token, SECRET, algorithms=['HS256'])
        #Checks if handle_str is valid
        if len(handle_str) < 3 or len(handle_str) > 20:
            raise InputError("Invalid handle")
        for x in data['users']:
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
        None
    Returns:
        A list containig all of the users and their information
    """
    valid_token = 0
    for t in data["token_list"]:
        if token == t:
            valid_token = 1
    #If token is valid, then profile dict is updated otherwise access error is thrown
    if valid_token == 1:
        all_users = []
        info = {}
        #Gets the user information
        for x in data["users"]:
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
    valid = 0
    #Checking to see if token is valid
    for t in data['token_list']:
        if t == token:
            valid = 1
    #If token is valid then returns the user stats, otherwise raises input error
    if valid == 1:
        decoded_token = jwt.decode(token, SECRET, algorithms=['HS256'])
        #Finding the user
        for i in data["users"]:
            for j in i["session_ids"]:
                if decoded_token["session_id"] == j:
                    u_id = i['u_id']
        #Getting number of channels user is in
        num_user_channels = data['users'][u_id]['num_channels']
        #Getting total number of channels
        all_channels = channels_listall_v1(token)
        total_channels = len(all_channels['channels'])
        #Getting number of dms user is in
        dms = dm.dm_list_v1(token)
        num_user_dms = len(dms['dms'])
        #Getting total number of dms
        total_dms = len(data['dms'])
        #Getting number of messages user has sent
        num_user_messages = data['users'][u_id]['num_messages']
        #Getting total number of messages
        total_messages = len(data["message_ids"])
        #Calculating involvement rate
        numerator = num_user_messages + num_user_dms + num_user_channels
        denominator = total_channels + total_dms + total_messages
        involvement_rate = float(numerator / denominator)
        #Getting the timestamp
        current_time = datetime.now()
        timestamp = current_time.replace(tzinfo=timezone.utc).timestamp()
        #Applying correct timestamps and adding new user_stats to data
        new_stat = {}
        count = 0
        i = 0
        if len(data["user_stats"]) == 0:
            new_stat["channels_joined"] = [{'joined': num_user_channels, 'time': timestamp}]
            new_stat["dms_joined"] = [{'joined': num_user_dms, 'time': timestamp}]
            new_stat["messages_sent"] = [{'sent': num_user_messages, 'time': timestamp}]
            new_stat["u_id"] = u_id          
            data["user_stats"].append(new_stat)
        else:   
            for check in data['user_stats']:
                if check['u_id'] == u_id:
                    count = i
                    if check['channels_joined'][len(check['channels_joined'])-1]['joined'] == num_user_channels:
                        channel_time = check['channels_joined'][len(check['channels_joined'])-1]['time']
                        new_stat = {'joined': num_user_channels, 'time': channel_time}
                        data['user_stats'][count]['channels_joined'].append(new_stat)
                    else:
                        new_stat = {'joined': num_user_channels, 'time': timestamp}
                        data['user_stats'][count]['channels_joined'].append(new_stat)
                    if check['dms_joined'][len(check['dms_joined'])-1]['joined'] == num_user_dms:
                        dm_time = check['dms_joined'][len(check['dms_joined'])-1]['time']
                        new_stat = {'joined': num_user_dms, 'time': dm_time}
                        data['user_stats'][count]['dms_joined'].append(new_stat)
                    else:
                        new_stat = {'joined': num_user_dms, 'time': timestamp}
                        data['user_stats'][count]['dms_joined'].append(new_stat) 
                    if check['messages_sent'][len(check['messages_sent'])-1]['sent'] == num_user_messages:
                        message_time = check['messages_sent'][len(check['messages_sent'])-1]['time']
                        new_stat = {'sent': num_user_messages, 'time': message_time}
                        data['user_stats'][count]['messages_sent'].append(new_stat)
                    else:
                        new_stat = {'sent': num_user_messages, 'time': timestamp}
                        data['user_stats'][count]['messages_sent'].append(new_stat)  
                else:
                    new_stat["channels_joined"] = [{'joined': num_user_channels, 'time': timestamp}]
                    new_stat["dms_joined"] = [{'joined': num_user_dms, 'time': timestamp}]
                    new_stat["messages_sent"] = [{'sent': num_user_messages, 'time': timestamp}]
                    new_stat["u_id"] = u_id          
                    data["user_stats"].append(new_stat)                    
                i += 1
    else:
        raise InputError("Invalid token")
    return_stat = data['user_stats'][count].copy()
    remove_u_id = return_stat.pop('u_id')
    return_stat['involvement_rate'] = involvement_rate
    return return_stat

def users_stats_v1(token):
    valid = 0
    #Checking to see if token is valid
    for t in data['token_list']:
        if t == token:
            valid = 1
    #If token is valid then returns the users stats, otherwise raises input error
    if valid == 1:    
        #Getting number of channels that currently exist
        all_channels = channels_listall_v1(token)
        total_channels = len(all_channels['channels'])
        #Getting number of dms that currently exist
        existing_dms = 0
        for x in data["dms"]:
            if x["dm_id"] != '':
                existing_dms += 1
        #Getting number of existing messages
        existing_messages = 0
        for y in data["channels"]:
            for z in y["messages"]:
                if z["message"] != '':
                    existing_messages += 1
        for a in data["dms"]:
            for b in a["messages"]:
                if b["message"] != '':
                    existing_messages += 1
        #Finding the users joined in at least one channel or dm
        users_joined = []
        for i in data["channels"]:
            for j in i["all_members"]:
                if users_joined == []:
                    users_joined.append(j["u_id"])
                else:
                    joined = 0
                    for users in users_joined:
                        if users == j["u_id"]:
                            joined = 1
                    if joined == 0:
                        users_joined.append(j["u_id"])

        for i in data["dms"]:
            for j in i["members"]:
                if users_joined == []:
                    users_joined.append(j["u_id"])
                else:
                    joined = 0
                    for users in users_joined:
                        if users == j["u_id"]:
                            joined = 1
                    if joined == 0:
                        users_joined.append(j["u_id"])
        print(users_joined)
        #Calculating utilization_rate
        utilization_rate = float(len(users_joined) / len(data["users"]))
        #Getting the timestamp
        current_time = datetime.now()
        timestamp = current_time.replace(tzinfo=timezone.utc).timestamp()
        #Applying correct timestamps and adding new users_stats to data
        new_stat = {}
        count = 0
        i = 0
        if len(data["dreams_stats"]) == 0:
            new_stat["channels_exist"] = [{'exist': total_channels, 'time': timestamp}]
            new_stat["dms_exist"] = [{'exist': existing_dms, 'time': timestamp}]
            new_stat["messages_exist"] = [{'exist': existing_messages, 'time': timestamp}]        
            data["dreams_stats"] = new_stat
        else:
            check = data['dreams_stats']
            if check['channels_exist'][len(check['channels_exist'])-1]['exist'] == total_channels:
                channel_time = check['channels_exist'][len(check['channels_exist'])-1]['time']
                new_stat = {'exist': total_channels, 'time': channel_time}
                data['dreams_stats']['channels_exist'].append(new_stat)
            else:
                new_stat = {'exist': total_channels, 'time': timestamp}
                data['dreams_stats']['channels_exist'].append(new_stat)
            if check['dms_exist'][len(check['dms_exist'])-1]['exist'] == existing_dms:
                dm_time = check['dms_exist'][len(check['dms_exist'])-1]['time']
                new_stat = {'exist': existing_dms, 'time': dm_time}
                data['dreams_stats']['dms_exist'].append(new_stat)
            else:
                new_stat = {'exist': existing_dms, 'time': timestamp}
                data['dreams_stats']['dms_exist'].append(new_stat) 
            if check['messages_exist'][len(check['messages_exist'])-1]['exist'] == existing_messages:
                message_time = check['messages_exist'][len(check['messages_exist'])-1]['time']
                new_stat = {'exist': existing_messages, 'time': message_time}
                data['dreams_stats']['messages_exist'].append(new_stat)
            else:
                new_stat = {'exist': num_user_dms, 'time': timestamp}
                data['dreams_stats']['messages_exist'].append(new_stat)
    else:
        raise InputError("Invalid token")
    data['dreams_stats']['utilization_rate'] = utilization_rate
    return data['dreams_stats']

import re
def user_profile_uploadphoto_v1(token, img_url, x_start, y_start, x_end, y_end):
    valid = 0
    #Checking to see if token is valid
    for t in data['token_list']:
        if t == token:
            valid = 1
    #If token is valid then returns the users stats, otherwise raises input error
    if valid == 1:   
        decoded_token = jwt.decode(token, SECRET, algorithms=['HS256'])
        u_id = ''
        for x in data["users"]:
            for y in x["session_ids"]:
                if decoded_token["session_id"] == y:
                    u_id = x['u_id']  
        regex = '.*jpg$'
        if re.search(regex, img_url):
            pass
        else:
            raise InputError("Invalid image url")
        #Downloaded the photo
        fullfilename = os.path.join("static", f"user{u_id}_photo.jpg")
        urllib.request.urlretrieve(img_url, fullfilename)
        #Crop image
        image = Image.open(fullfilename)  
        width, height = image.size
        print(width, height)
        if x_start > width or x_end > width or x_start < 0 or x_end < 0:
            raise InputError("Invalid x dimensions")
        print(y_start, height, y_end, height)
        if x_start == x_end:
            raise InputError("Invalid x dimensions")
        if y_start > height or y_end > height or y_start < 0 or y_end < 0:
            raise InputError("Invalid y dimensions")
        if y_start == y_end:
            raise InputError("Invalid y dimensions")
        crop_image = image.crop((x_start,y_start,x_end,y_end))
        crop_image.save(fullfilename)
        #Adding link to data
        data["users"][u_id]["img_url"] = f'http://127.0.0.1:{port}/' + fullfilename
    else:
        raise InputError("Invalid token")
    return {}
    
from message import message_send_v1, message_share_v1, message_remove_v1
from channels import channels_create_v1
IMG_URL = "https://cdn.mos.cms.futurecdn.net/YB6aQqKZBVjtt3PuDSkJKe.jpg"
if __name__ == '__main__':
    r = auth_register_v1("tom@gmail.com", "hello1234", "tom", "brown")
    s = auth_register_v1("tim@gmail.com", "hello1234", "tom", "brown")
    k = auth_register_v1("toom@gmail.com", "hello1234", "tom", "brown")
    channel = channels_create_v1(r['token'], "Channel1", True)
    channels_create_v1(s['token'], "Channel2", True)
    channels_create_v1(r['token'], "Channel3", True)
    dms = dm.dm_create_v1(r['token'], [1])
    dms1 = dm.dm_create_v1(s['token'], [0])
    message_id = message_send_v1(r['token'], channel['channel_id'], 'Hello')
    message_send_v1(r['token'], channel['channel_id'], 'Hello')
    message_share_v1(s['token'], message_id['message_id'], '', -1, dms['dm_id'])
    message_share_v1(s['token'], message_id['message_id'], '', -1, dms1['dm_id'])
    message_share_v1(s['token'], message_id['message_id'], '', -1, dms['dm_id'])
    dm.dm_remove_v1(r['token'], 0)
    # message_remove_v1(r['token'], 4)
    # message_remove_v1(r['token'], 3)
    # message_remove_v1(r['token'], 2)
    # message_remove_v1(r['token'], 1)
    # message_remove_v1(r['token'], 0)
    # p = user_stats_v1(r['token'])
    # print(p)
    # t = user_stats_v1(s['token'])
    # print(t)
    # o = user_stats_v1(k['token'])
    # print(o)
    # e = users_stats_v1(r['token'])
    # print(e)
    user_profile_uploadphoto_v1(r['token'], IMG_URL, 0, 0, 1500, 1000)  
    # y = user_stats_v1(s['token'])
    # print(y)
    # j = users_stats_v1(s['token'])

    ##############################
    ### ADD SRC AFTER FINISHED ###
    ##############################