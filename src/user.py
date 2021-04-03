from flask import request
import jwt
from src.data import data
from src.error import InputError
import re

def user_profile_v2(token, u_id):
    valid = 0
    #input_token = request.args.get('token')
    decoded_token = jwt.decode(token, 'HELLO', algorithms=['HS256'])
    #input_id = int(request.args.get('u_id'))
    profile = {}
    for x in data["users"]:
            if u_id == x['id']:
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
    return profile




def user_profile_setname_v2(token, name_first, name_last):
    decoded_token = jwt.decode(token, 'HELLO', algorithms=['HS256'])
    if len(name_first) < 1 or len(name_first) > 50:
        raise InputError("Invalid firstname")
    if len(name_last) < 1 or len(name_last) > 50:
        raise InputError("Invalid lastname")        
    for x in data["users"]:
        for y in x["session_ids"]:
            if decoded_token["session_ids"] == y:
                x['firstname'] = user['name_first']
                x['Lastname'] = user['name_last'] 
    return {}    



def user_profile_setemail_v2(token, email):
    decoded_token = jwt.decode(token, 'HELLO', algorithms=['HS256'])
    regex = '^[a-zA-Z0-9]+[\\._]?[a-zA-Z0-9]+[@]\\w+[.]\\w{2,3}$'
    unshared = 0
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
            for y in x["session_ids"]:
                if y == decoded_token["session_ids"]:
                    x['email'] = email
    return {}
        


def user_profile_sethandle_v1(token, handle_str):
    decoded_token = jwt.decode(token, 'HELLO', algorithms=['HS256'])
    if len(handle_str) < 3 or len(handle_str) > 20:
        raise InputError("Invalid handle")
    for x in data['users']:
        if x['handle_str'] == handle_str:
            raise InputError("Handle already used")
        else:
            for y in x["session_ids"]:
                if y == decoded_token["session_ids"]:
                    x['handle_str'] = handle_str
    return {}


def users_all_v1(token):
    return data["users"]