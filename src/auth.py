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

    ############    
    #__HANDLE__#
    ############

    #make handle +, lower(), replace, len
    handle = (name_first + name_last).lower()

    handle = handle.replace("@", "")
    handle = handle.replace(" ", "")
    handle = handle.replace("\t", "")
    handle = handle.replace("\n", "")

    #check if current input will be unique or not
    #and count repeated time
    repeat_times = 0
    for curr in data["users"]:
        fname_in_data = (curr["firstname"].replace("@","").replace(" ","") \
                        .replace("\t","").replace("\n","")).lower()
        lname_in_data = (curr["Lastname"].replace("@","").replace(" ","") \
                        .replace("\t","").replace("\n","")).lower()
        fname_input   = (name_first.replace("@","").replace(" ","") \
                        .replace("\t","").replace("\n","")).lower()
        lname_input   = (name_last.replace("@","").replace(" ","") \
                        .replace("\t","").replace("\n","")).lower()           
        if fname_in_data == fname_input and lname_in_data == lname_input:
            #print(fname_in_data, fname_input, lname_in_data, lname_input) #for debug
            repeat_times += 1    
            #assign fname and lname
    
    #add when handle is unique
    if repeat_times == 0:
        if len(handle) > 20:
            handle = handle[:20]
        #print(handle) #########################FORDEBUG#######
        register["handle"] = handle 
    
    elif repeat_times > 0:
        if len(handle) > 20:
            handle = handle[:20]
        #start from 0
        #repeat_times - 1; since we start from 0
        handle += str(repeat_times - 1)  #asdf asdf0(repeat = 1, conca 0) 0,1,2,3
        #print(handle)################FORDEBUG####

        #count digit of repeated handle
        #count is (how many digit), count from repeated time
        if len(handle) > 20:
            #count how many time it repeat, find digit
            
            #for debugging number before next digit will
            #fall to digit-1 and give bade result
            #e.g. 10 will become 9 but still count as 2 digits
            count_repeated_time = repeat_times 
            
            #need minus one but prevent first
            #element to bug
            if (repeat_times > 1): 
                count_repeated_time = repeat_times - 1

            count_digit = 0
            while(count_repeated_time != 0): #ex: 2
                count_repeated_time //= 10
                count_digit += 1

            #print(repeat_times) #FDB
            #print(count_digit) #FDB
            #old length that not exceed 20    
                
            len_handle = len(handle) - ((count_digit) * 2)
                        #22          -  2
            #assert (len_handle <= 20)
            #slice end of string digit times
            ##handle += str(repeat_times + 1)
            handle = handle[:len_handle]

            handle += str(repeat_times - 1)
            register["handle"] = handle     
            print(handle)


    #print(handle)
    #register["handle"] = handle 
    data["users"].append(register)
     
    return {
        'auth_user_id' : count,
    }


#print(data)