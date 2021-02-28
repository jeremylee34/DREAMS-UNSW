import tests.auth_info
import re
from src.error import InputError

def auth_login_v1(email, password):
    regex = '^[a-zA-Z0-9]+[\\._]?[a-zA-Z0-9]+[@]\\w+[.]\\w{2,3}$'
    #checks for valid email
    if re.search(regex, email):
        pass
    else:    
        raise InputError("Invalid email")
    #checks if email is correct
    if email is not users["user1"]["email"]:
        raise InputError("Incorrect email")
    #checks if password is correct
    if password is not users["user1"]["password"]:
        raise InputError("Incorrect password")
    return {
        'auth_user_id': 1,
    }

def auth_register_v1(email, password, name_first, name_last):
    regex = '^[a-zA-Z0-9]+[\\._]?[a-zA-Z0-9]+[@]\\w+[.]\\w{2,3}$'
    #checks for valid email
    if re.search(regex, email):
        pass
    else:    
        raise InputError("Invalid email")
    #checks for shared email
    i = 0
    for x in users:
        if email == users[x]["email"]:
            raise InputError("Email is already used")
            i = 1
    if i == 0:
        users["user1"]["email"] = email
    #checks for valid password
    if len(password) >= 6:
        users["user1"]["password"] = password
    else:
        raise InputError("Password too short")
    #checks for valid firstname
    if len(firstname) >= 1 and len(firstname) <= 50:
        users["user1"]["firstname"] = firstname
    else:
        raise InputError("Invalid firstname")
    #checks for valid lastname
    if len(Lastname) >= 1 and len(Lastname) <= 50:
        users["user1"]["Lastname"] = Lastname
    else:
        raise InputError("Invalid lastname")
    return {
        'auth_user_id' : 1,
    }

