'''
Implementation of user functions which includes user_profile_v1, user_profile_setname_v1,
user_profile_setemail_v1, user_profile_sethandle_v1, users_all_v1
Written by Kanit Srihakorth and Tharushi Gunawardana
'''
from flask import request
import jwt
from src.data import data
from src.error import InputError, AccessError
import re

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
    for t in data["token_list"]:
        if token == t:
            valid_token = 1
    #If token is valid, then profile dict is updated otherwise access error is thrown
    if valid_token == 1:
        decoded_token = jwt.decode(token, SECRET, algorithms=['HS256'])
        profile = {}
        #Getting information for user profile
        for x in data["users"]:
                if u_id == x['u_id']:
                    valid = 1
                    for y in x["session_ids"]:
                        if decoded_token["session_id"] == y:
                            profile['u_id'] = x['u_id']
                            profile['email'] = x['email']
                            profile['name_first'] = x['name_first']
                            profile['name_last'] = x['name_last']
                            profile['handle_str'] = x['handle_str']  
        #If u_id is not valid
        if valid == 0:
            raise InputError("Invalid user")
    else:
        raise AccessError("Invalid token")
    return profile

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
        raise AccessError("Invalid token")
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
        raise AccessError("Invalid token")
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
        raise AccessError("Invalid token")
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
        raise AccessError("Invalid token")
    return all_users