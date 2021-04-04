from src.data import data
from src.error import InputError
from src.error import AccessError

from src.helper import check_valid_user
from src.helper import check_valid_dm
from src.helper import token_to_u_id
from src.helper import check_user_in_dm
from src.user import user_profile_v2

import jwt

SECRET = "HELLO"

def dm_details_v1(token, dm_id):
    """
    <Users that are a part of this dm can view basic information about it>

    Arguments:
        token (string)    - an encoded session_id used to identify a user's session
        dm_id (integer)    - a unique integer used to identify a dm

    Exceptions:
        InputError  - Occurs when dm_id is not a valid DM
        AccessError - Occurs when authorised user is not a member of this DM with dm_id

    Return Value:
        dms, a list of a dm dicts

    """
    # check valid dm_id
    if check_valid_dm(dm_id) == False:
        raise InputError("dm_id does not refer to a valid DM")
    # check whether user is a member of the dm with dm_id
    user_id = token_to_u_id(token)
    if check_user_in_dm(user_id, dm_id) == False:
        raise AccessError("Authorised user is not a member of this DM with dm_id")
    return {
        'name': data['dms'][dm_id]['name'],
        'members': data['dms'][dm_id]['members']
    }

def dm_list_v1(token):
    """
    <Returns the list of DMs that the user is a member of>

    Arguments:
        token (string)    - an encoded session_id used to identify a user's session

    Exceptions:
        None

    Return Value:
        dms, a list of a dm dicts

    """
    dms = []
    user_id = token_to_u_id(token)
    for dm in data['dms']:
        for member in dm['members']:
            if member['u_id'] == user_id:
                new_dm_dict = {
                    'dm_id': dm['dm_id'],
                    'name': dm['name']
                }
                dms.append(new_dm_dict)
                break
    return {
        'dms': dms
    }

def dm_create_v1(token, u_ids):
    """
    <Create a dm, noting the owner, members, and a concat.d string>

    Arguments:
        token (string)    - an encoded session_id used to identify a user's session
        u_ids (list)    - a list of u_id's to be added to dm

    Exceptions:
        InputError  - Occurs when u_id does not refer to a valid user

    Return Value:
        Returns a dict containing the new dm_id and dm_name

    """
    # Check valid u_ids
    for u_id in u_ids:
        if check_valid_user(u_id) == False:
            raise InputError("u_id does not refer to a valid user")

    owner_u_id = token_to_u_id(token)
    # create list of handles for name whilst updating member list
    handle_list = []
    member_list = []
    u_ids.append(owner_u_id)
    for u_id in u_ids:
        for user in data['users']:
            if user['u_id'] == u_id:
                handle_list.append(user['handle_str'])
                
                
                s_id = user['session_ids'][0]
                s_token = jwt.encode({'session_id': s_id}, SECRET, algorithm='HS256')
                profile = user_profile_v2(s_token, u_id)
                member_list.append(profile)

                break
    # sort and concatenate
    handle_list.sort()
    handle_list_str = ', '.join(map(str, handle_list))
    dm_id = len(data['dms'])
    new_dm = {
        'name': handle_list_str,
        'dm_id': dm_id,
        'owner': owner_u_id,
        'members': member_list,
        "messages" : []
    }
    data['dms'].append(new_dm)
    return {
        'dm_id': dm_id,
        'dm_name': handle_list_str
    }

def dm_remove_v1(token, dm_id):
    """
    <Remove dm with dm_id>

    Arguments:
        token (string)    - an encoded session_id used to identify a user's session
        dm_id (integer)    - a unique integer used to identify a dm

    Exceptions:
        InputError  - Occurs when dm_id does not refer to a valid DM
        AccessError - Occurs when the user is not the original DM creator

    Return Value:
        Returns nothing

    """
    # check valid dm_id
    if check_valid_dm(dm_id) == False:
        raise InputError("dm_id does not refer to a valid DM")
    # check if user is authorised to remove dm
    user_id = token_to_u_id(token)

    if data['dms'][dm_id]['owner'] == user_id:
        empty_dict = {}
        for key in data['dms'][dm_id]:
            empty_dict[key] = ''
        data['dms'][dm_id] = empty_dict
    else:
        raise AccessError("The user is not the original DM creator")

    return {
    }

