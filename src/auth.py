from src.data import data
from src.error import InputError
import re
def auth_login_v1(email, password):
    regex = '^[a-zA-Z0-9]+[\\._]?[a-zA-Z0-9]+[@]\\w+[.]\\w{2,3}$'
    # Checks for valid email
    try:
        re.search(regex, email)
    except:
        InputError("Invalid email")
        
    # Checks if email and password is correct
    correct_email = 0
    correct_password = 0
    i = 0
    count = 0
    while i < len(data["users"]):
        if data["users"][i]["email"] == email:
            correct_email = 1
            count = i
        if data["users"][i]["password"] == password:
            correct_password = 1 
        i += 1
    if correct_email == 0:
        raise InputError("Incorrect email")
    if correct_password == 0:
        raise InputError("Incorrect password")
    print(count)
    return {
        'auth_user_id': count,
    }

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
        register["firstname"] = name_first
    else:
        raise InputError("Invalid firstname")

    # Checks for valid lastname
    if len(name_last) >= 1 and len(name_last) <= 50:
        register["Lastname"] = name_last
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
        if handle == data['users'][i]["handle"]:
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
      
    register["handle"] = handle 
    register['id'] = count
    data["users"].append(register)
    return {
        'auth_user_id' : count,
    }