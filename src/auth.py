from src.data import data
import re
from src.error import InputError

def auth_login_v1(email, password):
    regex = '^[a-zA-Z0-9]+[\\._]?[a-zA-Z0-9]+[@]\\w+[.]\\w{2,3}$'
    #checks for valid email
    try:
        re.search(regex, email)
    except:
        InputError("Invalid email")
        
    #checks if email and password is correct
    e = 0
    p = 0
    x = 0
    count = 0
    while x < len(data["users"]):
        if data["users"][x]["email"] == email:
            e = 1
            count = x + 1
        if data["users"][x]["password"] == password:
            p = 1 
        x += 1
    if e == 0:
        raise InputError("Incorrect email")
    if p == 0:
        raise InputError("Incorrect password")
    print(count)
    return {
        'auth_user_id': count,
    }

#HANDLES AND AUTH_USER_ID AND ASSUMPTION

def auth_register_v1(email, password, name_first, name_last):
    regex = '^[a-zA-Z0-9]+[\\._]?[a-zA-Z0-9]+[@]\\w+[.]\\w{2,3}$'
    #getting auth_user_id
    count = 1
    for i in data["users"]:
        count += 1
    register = {}

    #checks for valid email
    if re.search(regex, email):
        pass
    else:    
        raise InputError("Invalid email")

    #checks for shared email
    check_empty = bool(data["users"])
    if check_empty == False:
        register["email"] = email
    #if there are already thing in the dictionary
    else:
        for y in data["users"]:
            if y["email"] == email:
                raise InputError("Email is already used")
            else:
                register["email"] = email
    #checks for valid password
    if len(password) >= 6:
        register["password"] = password
    else:
        raise InputError("Password too short")

    #checks for valid firstname
    if len(name_first) >= 1 and len(name_first) <= 50:
        register["firstname"] = name_first
    else:
        raise InputError("Invalid firstname")

    #checks for valid lastname
    if len(name_last) >= 1 and len(name_last) <= 50:
        register["Lastname"] = name_last
    else:
        raise InputError("Invalid lastname")

    #making the handle
    #make lower case
    handle = (name_first + name_last).lower()

    #replace ' ' and '@' with ''
    handle = handle.replace("@", "")
    handle = handle.replace(" ", "")
    handle = handle.replace("\t", "")
    handle = handle.replace("\n", "")

    #check 20 chars; if exceed cut'em
    if len(handle) > 20:
        handle = handle[:20]
    
        #finding repetitions of names
        repeat = 0
        for r in data["users"]:
            last = r["Lastname"].replace("@", "")
            last = r["Lastname"].replace(" ", "")
            last = r["Lastname"].replace("\t", "")
            last = r["Lastname"].replace("\n", "")            
            first = r["firstname"].replace("@", "")
            first = r["firstname"].replace(" ", "")
            first = r["firstname"].replace("\t", "")
            first = r["firstname"].replace("\n", "")            
            name_last = name_last.replace("@", "")
            name_last = name_last.replace(" ", "")
            name_last = name_last.replace("\t", "")
            name_last = name_last.replace("\n", "")            
            name_first = name_first.replace("@", "")
            name_first = name_first.replace(" ", "")
            name_first = name_first.replace("\t", "")
            name_first = name_first.replace("\n", "")                                 
            if last == name_last and first == name_first:
                repeat += 1
        
        #find how many characters need to be replaced
        chars = list(str(repeat))
        num = 0
        for c in chars:
            num += 1

        #separate the characters of the handle
        if repeat >= 1:
            n = 0
            char_handle = list(handle) #[h, a, n, d, l, e]
            while n < num:
                pop_handle = char_handle.pop(-1)
                n += 1
            n = 0
            while n < num:
                char_handle.append(chars[n])
                n += 1
            char_handle = "".join(char_handle)
            #print(char_handle)
        #else:
            #print(handle)
    else:
        repeat = 0
        for r in data["users"]:
            last = r["Lastname"].replace("@", "")
            last = r["Lastname"].replace(" ", "")
            last = r["Lastname"].replace("\t", "")
            last = r["Lastname"].replace("\n", "")            
            first = r["firstname"].replace("@", "")
            first = r["firstname"].replace(" ", "")
            first = r["firstname"].replace("\t", "")
            first = r["firstname"].replace("\n", "")            
            name_last = name_last.replace("@", "")
            name_last = name_last.replace(" ", "")
            name_last = name_last.replace("\t", "")
            name_last = name_last.replace("\n", "")            
            name_first = name_first.replace("@", "")
            name_first = name_first.replace(" ", "")
            name_first = name_first.replace("\t", "")
            name_first = name_first.replace("\n", "")         
            if last == name_last and first == name_first:
                repeat += 1

        #separate the characters of the handle
        if repeat >= 1:
            n = 0
            char_handle = list(handle) #[h, a, n, d, l, e]
            char_handle.append(str(repeat))
            char_handle = "".join(char_handle)
            print(char_handle)
        else:
            print(handle)    
    register["handle"] = handle 
    data["users"].append(register)
    return {
        'auth_user_id' : count,
    }

"""auth_register_v1("honey@outlook.com", "hellooooo!!!", "honey", "smith")
auth_register_v1("asdfy@outlook.com", "hasdfooooo!!!", "ash", "blue")
auth_register_v1("tom@outlook.com", "hellooooo!!!", "Tom", "bite")
auth_register_v1("tom@gmail.com", "hellooooo!!!", "Tom", "bite")
auth_register_v1("tom@yahoo.com", "hellooooo!!!", "Tom", "bite")
auth_register_v1("tom@icloud.com", "hellooooo!!!", "Tom", "bite")
auth_register_v1("tom@google.com", "hellooooo!!!", "Tom", "bite")
auth_register_v1("tom1@gmail.com", "hellooooo!!!", "Tom", "bite")
auth_register_v1("tom2@gmail.com", "hellooooo!!!", "Tom", "bite")
auth_register_v1("tom3@gmail.com", "hellooooo!!!", "Tom", "bite")
auth_register_v1("tom4@gmail.com", "hellooooo!!!", "Tom", "bite")
auth_register_v1("tom5@gmail.com", "hellooooo!!!", "Tom", "bite")
auth_register_v1("tom6@gmail.com", "hellooooo!!!", "Tom", "bite")
auth_register_v1("tom7@gmail.com", "hellooooo!!!", "Tom", "bite")
auth_register_v1("tom8@gmail.com", "hellooooo!!!", "@Tom", "bite")
auth_register_v1("andy@gmail.com", "hellooooo!!!", "@Tom", "bite")

auth_login_v1("honey@outlook.com", "hellooooo!!!")
auth_login_v1("andy@gmail.com", "hellooooo!!!")"""

