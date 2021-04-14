import jwt
from src.data import data
from src.error import InputError
from src.error import AccessError
# from src.server import returns
# from src.server import save

SECRET = 'HELLO'

def admin_user_remove_v1(token, u_id):
    """
    Description of function:
        Remove the user(u_id) from the Dreams. 
        Must have authority to do so, being admin.
    Parameters:
        token (str)
        u_id (int)
    Exceptions:
        InputError - if the u_id is not a valid user
        AccessError - Authorised user isn't an owner
    Returns:
        Blank dictionary
    """
    # global data
    # returns()
    valid_token = 0
    valid = 0
    for tokens in data['token_list']:
        if tokens == token:
            valid_token = 1
    if valid_token == 0:
        raise AccessError('Invalid token')
    decoded_token = jwt.decode(token, SECRET, algorithms=['HS256'])
    for user in data['users']:
        if user['u_id'] == u_id:
            valid = 1
        for s_id in user['session_ids']:
            if s_id == decoded_token['session_id']:
                auth_user_id = user['u_id']
    if valid == 0:
        raise InputError("Invalid user")
    num_owners = 0
    for user2 in data['users']:
        if user2['permission_id'] == 1:
            num_owners += 1
    if num_owners == 1 and data['users'][auth_user_id]['permission_id'] == 1:
        raise InputError("User is the only owner")
    if data['users'][auth_user_id]['permission_id'] == 2:
        raise AccessError("Authorised user is not an owner")

    for x in data['users']: 
        if x['u_id'] == u_id:
            data['users'].remove(x)
    
    for channel_id in data['channels']:
        for messages in channel_id['messages']:
            if messages['u_id'] == u_id:
                messages['message'] = 'Removed user'

    for dm_id in data['dms']:
        for message2 in dm_id['messages']:
            if message2['u_id'] == u_id:
                message2['message'] = 'Removed user'
    # save()
    return {}

def admin_userpermission_change_v1(token, u_id, permission_id):
    """
    Description of function:
        Given the user(u_id) new permission described by permission_id. 
        Must have authority to do so, being admin.
    Parameters:
        token (str)
        u_id (int)
        permission_id (str)
    Exceptions:
        InputError - if the u_id is not a valid user
        AccessError - Authorised user isn't an owner
    Returns:
        Blank dictionary
    """ 
    # global data
    # returns()
    valid_permission = 0
    if permission_id == 1 or permission_id == 2:
        valid_permission = 1
    if valid_permission == 0:
        raise AccessError('Permission_id is not valid') 
    valid = 0
    valid_token = 0
    for tokens in data['token_list']:
        if tokens == token:
            valid_token = 1
    if valid_token == 0:
        raise AccessError('Invalid token')
    decoded_token = jwt.decode(token, SECRET, algorithms=['HS256'])
    for user in data['users']:
        if user['u_id'] == u_id:
            valid = 1
        for s_id in user['session_ids']:
            if s_id == decoded_token['session_id']:
                auth_user_id = user['u_id']
    if valid == 0:
        raise InputError("Invalid user")
    if data['users'][auth_user_id]['permission_id'] == 2:
        raise AccessError("Authorised user is not an owner")
        
    data['users'][u_id]['permission_id'] = permission_id
    # save()
    return {}
