'''
Implementation of auth functions which includes auth_login_v1,
auth_register_v1, auth_login_v1
Written by Kanit Srihakorth and Tharushi Gunawardana
'''
from src.database import data
from src.error import InputError, AccessError
import re
import jwt
import hashlib
from flask import request

SECRET = 'HELLO'

session_id = 0
def create_session_id():
    """
    Description of function:
        Creates a new session_id
    Parameters:
        None
    Exceptions:
        None
    Returns:
        Returns 'session_id'
    """    
    global session_id
    session_id += 1
    return session_id


def auth_login_v1(email, password):
    """
    Description of function:
        Accepts email and password to validate user login details.
    Parameters:
        email (str)
        password(str)
    Exceptions:
        InputError - when the email is not valid
        InputError - when the email is incorrect
        InputError - when the password is not correct
    Returns:
        Dictionary containing 'token' and 'auth_user_id'
    """
    
    regex = '^[a-zA-Z0-9]+[\\._]?[a-zA-Z0-9]+[@]\\w+[.]\\w{2,3}$'
    # Checks for valid email
    if re.search(regex, email):
        pass
    else:
        InputError("Invalid email")
        
    # Checks if email and password is correct
    correct_email = 0
    correct_password = 0
    input_password = hashlib.sha256(password.encode()).hexdigest()
    i = 0
    count = 0
    while i < len(data["users"]):
        if data["users"][i]["email"] == email:
            correct_email = 1
            count = i   
        if data["users"][i]["password"] == input_password:
            correct_password = 1
        i += 1
    if correct_email == 0:
        raise InputError("Incorrect email")
    if correct_password == 0:
        raise InputError("Incorrect password")
    #Generating a new session_id
    data["users"][count]["session_ids"].append(create_session_id())
    #Generating new token
    token = jwt.encode({'session_id': session_id}, SECRET, algorithm='HS256')
    data['token_list'].append(token)
    return {
        'token': token,
        'auth_user_id': count
    }



def auth_register_v1(email, password, name_first, name_last):
    """
    Description of function:
        Stores user registration information in the data file
    Parameters:
        email (str)
        password(str)
        name_first (str)
        name_last (str)
    Exceptions:
        InputError - when the email is not valid
        InputError - when the email is user by another existing user
        InputError - when the password is too short (less than 6 character)
        InputError - when the name_first is invalid (less than 1 character or greater than 50 characters)    
        InputError - when the name_last is invalid (less than 1 character or greater than 50 characters)
        
    Returns:
        Dictionary containing 'token' and 'auth_user_id'
    """    
    regex = '^[a-zA-Z0-9]+[\\._]?[a-zA-Z0-9]+[@]\\w+[.]\\w{2,3}$'
    # Getting auth_user_id
    count = len(data['users'])
    register = {}
    register['u_id'] = count
    # Checks for valid email
    if re.search(regex, email):
        pass
    else:    
        raise InputError("Invalid email")

    # Checks for shared email
    check_empty = bool(data["users"])
    if check_empty == False:
        register["email"] = email
    # If there are already thing in the dictionary
    else:
        for y in data["users"]:
            if y["email"] == email:
                raise InputError("Email is already used")
            else:
                register["email"] = email
    # Checks for valid password
    if len(password) >= 6:
        register["password"] = hashlib.sha256(password.encode()).hexdigest()
    else:
        raise InputError("Password too short")

    # Checks for valid firstname
    if len(name_first) >= 1 and len(name_first) <= 50:
        register["name_first"] = name_first
    else:
        raise InputError("Invalid firstname")

    # Checks for valid lastname
    if len(name_last) >= 1 and len(name_last) <= 50:
        register["name_last"] = name_last
    else:
        raise InputError("Invalid lastname")

    # making the handle
    # make lower case
    handle = (name_first + name_last).lower()

    # replace ' ' and '@' with ''
    handle = handle.replace("@", "")
    handle = handle.replace(" ", "")
    handle = handle.replace("\t", "")
    handle = handle.replace("\n", "")

    #check 20 chars; if exceed cut'em
    if len(handle) > 20:
        handle = handle[:20]
    
    # finding repetitions of names
    number = 0
    i = 0
    length = 0
    while i in range(len(data["users"])):
        if handle == data['users'][i]["handle_str"]:
            handle.replace(str(number), "")
            if len(handle) + len(str(number)) > 20:
                length = len(handle) + len(str(number)) - 20
                length = 20 - length
                handle = handle[:length]
            handle += str(number)
            number += 1
            i = 0
        else:
            i += 1 
      
    register["handle_str"] = handle 
    #setting DREAMS(admin) permission
    if (len(data['users']) < 1):
        register['permission_id'] = 1
    else:
        register['permission_id'] = 2
    #creating session_id list for user
    register['session_ids'] = []
    register['session_ids'].append(create_session_id())    
    #generating the token
    token = jwt.encode({'session_id': session_id}, SECRET, algorithm='HS256')
    data['token_list'].append(token)
    data['users'].append(register)
    return {
        'token': token,
        'auth_user_id': count
    }


def auth_logout_v1(token):
    """
    Description of function:
        Accepts a token and logs out a user of a particular session based on the token. If the logout is successful, then True is returned, otherwise False
    Parameters:
        token (str)
    Exceptions:
        None
    Returns:
        Dictionary containing 'is_success'
    """    
    logout = False
    valid_token = 0
    #Decodes the token
    decoded_token = jwt.decode(token, SECRET, algorithms=['HS256'])
    #Removes token from token_list if it exists
    for t in data["token_list"]:
        if token == t:
            valid_token = 1
            data['token_list'].remove(token) 
    #If the token is valid, then particular session_id is removed, otherwise AccessError is raised
    if valid_token == 1:
        for x in data["users"]:
            for y in x["session_ids"]:
                if decoded_token["session_id"] == y:
                    x["session_ids"].remove(y)
                    logout = True
    else:
        raise AccessError("Invalid token")
    return {
        'is_success': logout
    }


