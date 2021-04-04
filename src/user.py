def user_profile_v1(auth_user_id, u_id):
    return {
        'user': {
            'u_id': 1,
            'email': 'cs1531@cse.unsw.edu.au',
            'name_first': 'Hayden',
            'name_last': 'Jacobs',
            'handle_str': 'haydenjacobs',
        },
    }

def user_profile_setname_v1(auth_user_id, name_first, name_last):
    return {
    }

def user_profile_setemail_v1(auth_user_id, email):
    return {
    }

def user_profile_sethandle_v1(auth_user_id, handle_str):
    return {
    }

def users_all(token):
    input_token = request.args.get('token') #what's the use of token?
    data = {}
    return {
        'users' : data
    }

def admin_user_remove(token, u_id):
#check if admin have permission 
    for x in data['users']:    
        if (x['session_ids'] == decoded_token['session_ids']):
            if (x['permission_id'] == '1'):
                access = 1
                #approved access, start delete process
                for y in data['users']:
                    if (input_id == y['id']):
                        valid = 1
                        y.pop('email', 'password', 'firstname', 'Lastname', 
                              'handle_str', 'session_ids')

    #left with 'id' to identicate, to tell that left only 'id' return "Removed user"
    #check in search func, to modify it to relate with this approach
    if valid == 0:
        raise InputError("Invalid user")
    if access == 0:
        raise AccessError("The authorised user is not an owner")

    return {}

def admin_userpermission_change_v1(token, u_id, permission_id):
    for x in data['users']:    
        if (x['session_ids'] == decoded_token['session_ids']):
            if (x['permission_id'] == '1'):
                access = 1
                #approved access, start delete process
                for y in data['users']:
                    if (input_id == y['id']):
                        valid = 1
                        y['permission_id'] = input_permission
    
    return{}

