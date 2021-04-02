from json import dumps
from flask import Flask, request
from src.config import port
from src.data import data
from src.error import InputError, AccessError
import re
import hashlib
import jwt


app = Flask(__name__)

session_id = 0
def create_session_id():
    global session_id
    session_id += 1
    return session_id

def create_token():
    return jwt.encode({})

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
    input_password = hashlib.sha256(login_info["password"].encode()).hexdigest()
    i = 0
    count = 0
    while i < len(data["users"]):
        if data["users"][i]["email"] == login_info['email'] and data["users"][i]["password"] == input_password:
            correct_email = 1
            count = i
            data["users"][count]["session_ids"].append(create_session_id())
            correct_password = 1 
            token = jwt.encode({'session_ids': session_id}, 'HELLO', algorithm='HS256')
        i += 1
    if correct_email == 0:
        raise InputError("Incorrect email")
    if correct_password == 0:
        raise InputError("Incorrect password")

    return dumps({
        'token': token,
        'auth_user_id': count,
        'data': data["users"]
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
        register["password"] = hashlib.sha256(info['password'].encode()).hexdigest()
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
    #creating session_id
    register['session_ids'] = []
    register['session_ids'].append(create_session_id())    
    #generating the token
    token = jwt.encode({'session_ids': session_id}, 'HELLO', algorithm='HS256')
    data["users"].append(register)    
    return dumps({
        'token': token,
        'auth_user_id': count,
        'data.email': data['users']
    })

@app.route('/auth/logout/v1', methods=['POST'])
def logout():
    logout = False
    user = request.get_json()
    token = jwt.decode(user['token'], 'HELLO', algorithms=['HS256'])
    for x in data["users"]:
        for y in x["session_ids"]:
            if token["session_ids"] == y:
                x["session_ids"].remove(y)
                logout = True
    return dumps({
        'is_success': logout,
    })

@app.route('/user/profile/v2', methods=['GET'])
def user_profile():
    valid = 0
    input_token = request.args.get('token')
    decoded_token = jwt.decode(input_token, 'HELLO', algorithms=['HS256'])
    input_id = int(request.args.get('u_id'))
    profile = {}
    for x in data["users"]:
            if input_id == x['id']:
                valid = 1
                for y in x["session_ids"]:
                    if decoded_token["session_ids"] == y:
                        profile['u_id'] = x['id']
                        profile['email'] = x['email']
                        profile['name_first'] = x['firstname']
                        profile['name_last'] = x['Lastname']
                        profile['handle'] = x['handle_str']  
    if valid == 0:
        raise InputError("Invalid user")
    return dumps(profile)



@app.route('/user/profile/setname/v2', methods=['PUT'])
def profile_setname():
    user = request.get_json()
    decoded_token = jwt.decode(user['token'], 'HELLO', algorithms=['HS256'])
    if len(user['name_first']) < 1 or len(user['name_first']) > 50:
        raise InputError("Invalid firstname")
    if len(user['name_last']) < 1 or len(user['name_last']) > 50:
        raise InputError("Invalid lastname")        
    for x in data["users"]:
        for y in x["session_ids"]:
            if decoded_token["session_ids"] == y:
                x['firstname'] = user['name_first']
                x['Lastname'] = user['name_last'] 
    return dumps({})    


@app.route('/user/profile/setemail/v2', methods=['PUT'])
def profile_setemail():
    user = request.get_json()
    decoded_token = jwt.decode(user['token'], 'HELLO', algorithms=['HS256'])
    regex = '^[a-zA-Z0-9]+[\\._]?[a-zA-Z0-9]+[@]\\w+[.]\\w{2,3}$'
    unshared = 0
    # Checks for valid email
    if re.search(regex, user['email']):
        pass
    else:    
        raise InputError("Invalid email")
    #checking for if email is already used
    for x in data["users"]:
        if x["email"] == user['email']:
            raise InputError("Email is already used")
        else:
            for y in x["session_ids"]:
                if y == decoded_token["session_ids"]:
                    x['email'] = user['email']
    return dumps({})
        

@app.route('/user/profile/sethandle/v1', methods=['PUT'])
def profile_sethandle():
    user = request.get_json()
    decoded_token = jwt.decode(user['token'], 'HELLO', algorithms=['HS256'])
    if len(user['handle_str']) < 3 or len(user['handle_str']) > 20:
        raise InputError("Invalid handle")
    for x in data['users']:
        if x['handle_str'] == user['handle_str']:
            raise InputError("Handle already used")
        else:
            for y in x["session_ids"]:
                if y == decoded_token["session_ids"]:
                    x['handle_str'] = user['handle_str']
    return dumps({})

@app.route('/users/all/v1', methods=['GET'])
def users_all():
    input_token = request.args.get('token')
    return dumps(data["users"])

"""
@app.route('/search/v2', methods=['GET'])


@app.route('/admin/user/remove/v1', methods=['DELETE'])


@app.route('/admin/userpermission/change/v1', methods=['POST'])


@app.route('/notifications/get/v1', methods=['GET'])
"""
@app.route('/clear/v1', methods=['DELETE'])
def clear():
    for x in data["users"]:
        x["session_ids"].clear()
    data['users'].clear()
    data['channels'].clear()
    data['messages'].clear()  
    return dumps({})


if __name__ == '__main__':
    app.run(port=port)
    
