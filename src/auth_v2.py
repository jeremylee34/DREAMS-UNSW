from json import dumps
from flask import Flask, request
import config
from data import data
from error import InputError, AccessError
import re

app = Flask(__name__)

@app.route('/auth/login/v2', methods=['POST'])
def login():
    login_info = request.get_json()
    regex = '^[a-zA-Z0-9]+[\\._]?[a-zA-Z0-9]+[@]\\w+[.]\\w{2,3}$'
    # Checks for valid email
    if re.search(regex, login_info['email']):
        pass
    else:
        InputError("Invalid email")
        
    # Checks if email and password is correct
    correct_email = 0
    correct_password = 0
    i = 0
    count = 0
    while i < len(data["users"]):
        if data["users"][i]["email"] == login_info['email']:
            correct_email = 1
            count = i
        if data["users"][i]["password"] == login_info['password']:
            correct_password = 1 
        i += 1
    if correct_email == 0:
        raise InputError("Incorrect email")
    if correct_password == 0:
        raise InputError("Incorrect password")    
    return dumps({
        'token': '',
        'auth_user_id': count,
    })


@app.route('/auth/register/v2', methods=['POST'])
def register():
    info = request.get_json()
    regex = '^[a-zA-Z0-9]+[\\._]?[a-zA-Z0-9]+[@]\\w+[.]\\w{2,3}$'
    # Getting auth_user_id
    count = len(data['users'])
    register = {}

    # Checks for valid email
    if re.search(regex, info['email']):
        pass
    else:    
        raise InputError("Invalid email")

    # Checks for shared email
    check_empty = bool(data["users"])
    if check_empty == False:
        register["email"] = info['email']
    # If there are already thing in the dictionary
    else:
        for y in data["users"]:
            if y["email"] == info['email']:
                raise InputError("Email is already used")
            else:
                register["email"] = info['email']
    # Checks for valid password
    if len(info['password']) >= 6:
        register["password"] = info['password']
    else:
        raise InputError("Password too short")

    # Checks for valid firstname
    if len(info['name_first']) >= 1 and len(info['name_first']) <= 50:
        register["firstname"] = info['name_first']
    else:
        raise InputError("Invalid firstname")

    # Checks for valid lastname
    if len(info['name_last']) >= 1 and len(info['name_last']) <= 50:
        register["Lastname"] = info['name_last']
    else:
        raise InputError("Invalid lastname")

    # making the handle
    # make lower case
    handle = (info['name_first'] + info['name_last']).lower()

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
    register['id'] = count
    data["users"].append(register)    
    return dumps({
        'token': '',
        'auth_user_id': count,
        'data.email': data['users']
    })

"""@app.route('/auth/logout/v1', methods=['POST'])
def logout(token):

    return dumps({
        'is_success': '',
    })
"""
"""@app.route('/auth/logout/v1', methods=['POST'])
def logout(token):

    return dumps({
        'is_success': '',
    })
"""

"""@app.route('/user/profile/v2', methods=['GET'])
def user_profile():

@app.route('/user/profile/setname/v2', methods=['PUT'])


@app.route('/user/profile/setemail/v2', methods=['PUT'])


@app.route('/user/profile/sethandle/v1', methods=['PUT'])


@app.route('/users/all/v1', methods=['GET'])

"""
@app.route('/clear/v1', methods=['DELETE'])
def clear():
    data['users'].clear()
    data['channels'].clear()
    data['messages'].clear()  
    return dumps({})  


if __name__ == '__main__':
    app.run(port=config.port)