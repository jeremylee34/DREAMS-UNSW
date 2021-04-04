'''
Implementation of auth functions which includes auth_login_v1 and
auth_register_v1.
Written by Kanit Srihakorth and Tharushi Gunawardana
'''
from src.data import data
from src.error import InputError
import re


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
        if data["users"][i]["email"] == email and data["users"][i]["password"] == input_password:
            correct_email = 1
            count = i
            data["users"][count]["session_ids"].append(create_session_id())
            correct_password = 1 
            token = jwt.encode({'session_id': session_id}, SECRET, algorithm='HS256')
            data['token_list'].append(token)
        i += 1
    if correct_email == 0:
        raise InputError("Incorrect email")
    if correct_password == 0:
        raise InputError("Incorrect password")

    return {
        'token': token,
        'auth_user_id': count,
    }

'''
Description of function:
    Stores user registration information in the data file. It returns the auth_user_id of that user.

Parameters:
    email (str)
    password (str)
    name_first (str) 
    name_last (str)

Exceptions:
    InputError - when the email is not valid
    InputError - when the email is used by another user
    InputError - when the password is too short (smaller than 6 character)
    InputError - when the name_first is invalid (smaller than 1 character or larger than 50 characters)    
    InputError - when the name_last is invalid (smaller than 1 character or larger than 50 characters)

Returns:
    'auth_user_id'
'''
def auth_register_v1(email, password, name_first, name_last):
    regex = '^[a-zA-Z0-9]+[\\._]?[a-zA-Z0-9]+[@]\\w+[.]\\w{2,3}$'
    # Getting auth_user_id
    count = len(data['users'])
    register = {}

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
        register["password"] = password
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
    # repeat = 0
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
            
    #setting DREAMS(admin) permission
    if (len(data['user']) < 1):
        register['permission_id'] = '1'
    else:
        register['permission_id'] = '2'

    register["handle_str"] = handle 
    register['session_ids'] = []
    register['session_ids'].append(create_session_id())    
    token = jwt.encode({'session_id': session_id}, SECRET, algorithm='HS256')
    data['token_list'].append(token)
    data["users"].append(register)
    return {
        'token': token,
        'auth_user_id': count,
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
    decoded_token = jwt.decode(token, SECRET, algorithms=['HS256'])
    for t in data["token_list"]:
        if token == t:
            valid_token = 1
            data['token_list'].remove(token) 
    if valid_token == 1:
        for x in data["users"]:
            for y in x["session_ids"]:
                if decoded_token["session_id"] == y:
                    x["session_ids"].remove(y)
                    logout = True
    else:
        raise AccessError("Invalid token")
    return {
        'is_success': logout,
    }


