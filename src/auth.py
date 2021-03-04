from src.auth_info import users
import re
from src.error import InputError

def auth_login_v1(email, password):
    regex = '^[a-zA-Z0-9]+[\\._]?[a-zA-Z0-9]+[@]\\w+[.]\\w{2,3}$'
    #checks for valid email
    """if re.search(regex, email):
        pass
    else:    
        raise InputError("Invalid email")"""

    try:
        re.search(regex, email)
    except:
        InputError("Invalid email")
        
    #checks if email and password is correct
    e = 0
    p = 0
    count = 1
    num = 0
    for x in users:
        if users[x]["email"] == email:
            e = 1
            num = count
        if users[x]["password"] == password:
            p = 1
        count += 1
    if e == 0:
        raise InputError("Incorrect email")
    if p == 0:
        raise InputError("Incorrect password")
    return {
        'auth_user_id': num,
    }

#HANDLES AND AUTH_USER_ID AND ASSUMPTION

def auth_register_v1(email, password, name_first, name_last):
    regex = '^[a-zA-Z0-9]+[\\._]?[a-zA-Z0-9]+[@]\\w+[.]\\w{2,3}$'
    #getting auth_user_id
    count = 1
    for i in users:
        count += 1
    users[f"user{count}"] = {}
    #checks for valid email
    if re.search(regex, email):
        pass
    else:    
        raise InputError("Invalid email")
    #checks for shared email
    if count == 1:
        users[f"user{count}"]["email"] = email
    else:
        x = 1
        while x < count:
            if email == users[f"user{x}"]["email"]:
                raise InputError("Email is already used")
            x += 1
        users[f"user{count}"]["email"] = email
    #checks for valid password
    if len(password) >= 6:
        users[f"user{count}"]["password"] = password
    else:
        raise InputError("Password too short")
    #checks for valid firstname
    if len(name_first) >= 1 and len(name_first) <= 50:
        users[f"user{count}"]["firstname"] = name_first
    else:
        raise InputError("Invalid firstname")
    #checks for valid lastname
    if len(name_last) >= 1 and len(name_last) <= 50:
        users[f"user{count}"]["Lastname"] = name_last
    else:
        raise InputError("Invalid lastname")
    print(count)
    #handle	
    handle = ''
    #error will occur before getting here?
    conca = users[f"user{count}"]["firstname"]+users[f"user{count}"]["lastname"]
    r = re.compiler(r"[@]")
    cut_ad = r.sub("",s)
    handle += conca.replace(" ","")
    if len(handle)>20
	raise InputError("too long conca")    

    return {
        'auth_user_id' : count,
    }

#auth_register_v1("honey@outlook.com", "hellooooo!!!", "Tim", "Oreo")
#auth_register_v1("tom@outlook.com", "hellooooo!!!", "Tom", "bite")
#auth_register_v1("andy@gmail.com", "hellooooo!!!", "Andy", "cook")
#auth_login_v1("andy@gmail.com", "hellooooo!!!")
#auth_login_v1("tom@outlook.com", "hellooooo!!!")
