import src.data as data
from src.error import InputError
from src.error import AccessError

from src.helper import check_valid_user
from src.helper import check_valid_dm
from src.helper import token_to_u_id
from src.helper import check_user_in_dm
from src.helper import check_valid_token
from src.user import user_profile_v1

import jwt

SECRET = "HELLO"
DREAMS_OWWNER = 0

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
    if check_valid_token(token) == False:
        raise InputError("token does not refer to a valid token")
    # check valid dm_id
    if check_valid_dm(dm_id) == False:
        raise InputError("dm_id does not refer to a valid DM")
    # check whether user is a member of the dm with dm_id
    user_id = token_to_u_id(token)
    if check_user_in_dm(user_id, dm_id) == False:
        raise AccessError("Authorised user is not a member of this DM with dm_id")
    return {
        'name': data.data['dms'][dm_id]['name'],
        'members': data.data['dms'][dm_id]['members']
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
    if check_valid_token(token) == False:
        raise InputError("token does not refer to a valid token")
    dms = []
    user_id = token_to_u_id(token)
    for dm in data.data['dms']:
        for member in dm['members']:
            if member['u_id'] == user_id:
                new_dm_dict = {
                    'dm_id': dm['dm_id'],
                    'name': dm['name']
                }
                dms.append(new_dm_dict)
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
    if check_valid_token(token) is False:
        raise InputError("token does not refer to a valid token")
    # Check valid u_ids
    for u_id in u_ids:
        if check_valid_user(u_id) is False:
            raise InputError("u_id does not refer to a valid user")

    owner_u_id = token_to_u_id(token)
    # create list of handles for name whilst updating member list
    handle_list = []
    member_list = []
    # u_ids.append(owner_u_id)
    u_ids.insert(0, owner_u_id,)
    for u_id in u_ids:
        handle_list.append(data.data['users'][u_id]['handle_str'])
        s_id = data.data['users'][u_id]['session_ids'][0]
        s_token = jwt.encode({'session_id': s_id}, SECRET, algorithm='HS256')
        profile = user_profile_v1(s_token, u_id)
        member_list.append(profile['user'])

    # sort and concatenate
    handle_list.sort()
    handle_list_str = ', '.join(map(str, handle_list))
    dm_id = len(data.data['dms'])
    new_dm = {
        'name': handle_list_str,
        'dm_id': dm_id,
        'owner': owner_u_id,
        'members': member_list,
        "messages" : []
    }
    data.data['dms'].append(new_dm)
    new_notification = {
        "u_id": owner_u_id,
        "message": "",
        "channel_id": -1,
        "dm_id": dm_id,
        'reacts': []
    }
    data.data['notifications'].append(new_notification)
    data.data['users'][owner_u_id]['num_dms'] += 1
    for user in u_ids:
        data.data['users'][user]['num_dms'] += 1
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
    if check_valid_token(token) == False:
        raise InputError("token does not refer to a valid token")
    # check valid dm_id
    if check_valid_dm(dm_id) == False:
        raise InputError("dm_id does not refer to a valid DM")
    # check if user is authorised to remove dm
    user_id = token_to_u_id(token)

    if data.data['dms'][dm_id]['owner'] == user_id:
        empty_dict = {}
        for key in data.data['dms'][dm_id]:
            empty_dict[key] = ''
        data.data['dms'][dm_id] = empty_dict
    else:
        raise AccessError("The user is not the original DM creator")
    return {
    }

def dm_invite_v1(token, dm_id, u_id):
    """
    <Function is called by user refered by token to add u_id to DM>
    
    Arguments:
        <token> (<string>)  - encoded id that identifies user session
        <dm_id> (<integer>) - Identifier for particular DM 
        <u_id> (<integer>)  - Identifier for particular user 
        
    Exceptions:
        InputError  - Occurs when dm_id does not refer to an exising dm and u_id
                      does not refer to a valid user   
        AccessError  - Occurs when authorised user is not a member of the DM       
        
    Return Value: {} 
    """
    if check_valid_token(token) == False:
        raise InputError("token does not refer to a valid token")
    #Check if dm_id refers to a valid dm, raise InputError if not
    if check_valid_dm(dm_id) == False:
        raise InputError("dm_id does not refer to an existing dm")
    #Check if u_id refers to a valid user, raise InputError if not 
    if check_valid_user(u_id) == False:
        raise InputError("u_id does not refer to a valid user")
    # Check if u_id is already in the dm
    if check_user_in_dm(u_id, dm_id) == True:
        raise InputError("User with u_id is already in the dm")
    user = token_to_u_id(token)
    #Check if token user is a member of the specified dm, raise AccessError if not
    if check_user_in_dm(user, dm_id) == False:
        raise AccessError("the authorised user is not a member of this DM")
    #Look for corresponding dm through dm_id then append invited user to members list
    #Also update the name of the dm by adding new handle and re-sorting 
    s_id = data.data['users'][u_id]['session_ids'][0]
    s_token = jwt.encode({'session_id': s_id}, SECRET, algorithm='HS256')
    profile = user_profile_v1(s_token, u_id)
    data.data['dms'][dm_id]['members'].append(profile['user'])
    handlelist = data.data['dms'][dm_id]['name'].split(", ")
    handlelist.append(data.data['users'][u_id]['handle_str'])

    handlelist.sort()
    handlelist_string = ', '.join(map(str, handlelist))
    data.data['dms'][dm_id]['name'] = handlelist_string        

    new_notification = {
        "u_id": user,
        "message": "",
        "channel_id": -1,
        "dm_id": dm_id,
        'reacts': []
    }
    data.data['notifications'].append(new_notification)
    data.data['users'][u_id]['num_dms'] += 1
    return {}
       
       
def dm_leave_v1(token, dm_id):
    """
    <Function is called by user refered by token to leave DM>
    
    Arguments:
        <token> (<string>)  - encoded id that identifies user session
        <dm_id> (<integer>) - Identifier for particular DM 
        
    Exceptions:
        InputError  - Occurs when dm_id does not refer to an exising dm   
        AccessError  - Occurs when authorised user is not a member of the DM       
        
    Return Value: {} 
    """
    if check_valid_token(token) == False:
        raise InputError("token does not refer to a valid token")
    #Check if dm_id refers to a valid dm, raise InputError if not
    if check_valid_dm(dm_id) == False:
        raise InputError("dm_id does not refer to an existing dm")
    user = token_to_u_id(token)
    #Check if token user is a member of the specified dm, raise AccessError if not
    if check_user_in_dm(user, dm_id) == False:
        raise AccessError("the authorised user is not a member of this DM")
    #Look for corresponding dm through dm_id then remove token user from members list
    #Also remove the token users handle from name 
    for users in data.data['users']:
        if users['u_id'] == user:
            s_id = users['session_ids'][0]
            s_token = jwt.encode({'session_id': s_id}, SECRET, algorithm='HS256')
            profile = user_profile_v1(s_token, user)
            data.data['dms'][dm_id]['members'].remove(profile['user'])
            stringU = users['handle_str']                   
            handlelist = data.data['dms'][dm_id]['name'].split(", ")
            handlelist.remove(stringU)

    handlelist.sort()
    handlelist_string = ', '.join(map(str, handlelist))
    data.data['dms'][dm_id]['name'] = handlelist_string
    data.data['users'][user]['num_dms'] -= 1        
    return{}
    
    
def dm_messages_v1(token, dm_id, start):
    """
    <Function is called by user to return up to 50 messages from DM>
    
    Arguments:
        <token> (<string>)  - encoded id that identifies user session
        <dm_id> (<integer>) - Identifier for particular DM 
        <start> (<integer>)  - First index of messages to be returned
        
    Exceptions:
        InputError  - Occurs when dm_id does not refer to an exising dm and start
                      is greater than the total number of messages in DM  
        AccessError  - Occurs when authorised user is not a member of the DM       
        
    Return Value: 
        messages  - List of dictionaries descibing each message 
        start  - First index of messages returned
        end  - Final index of messages returned, usually start + 50 but will be 
               set to -1 if start + 50 surpasses the bound of messages in DM 
    """
    if check_valid_token(token) == False:
        raise InputError("token does not refer to a valid token")
    #Check if dm_id refers to a valid dm, raise InputError if not
    if check_valid_dm(dm_id) == False:
        raise InputError("dm_id does not refer to an existing dm")
    #Check if start is greater tham total messages in the DM
    #Raise InputError if it is 
    length_messages = len(data.data['dms'][dm_id]['messages'])
    if start == 0 and length_messages == 0:
        return {
            'messages': [],
            'start': start,
            'end': 0
        }
    if start >= length_messages:
        raise InputError("Start is greater tham total messages in the DM")

    user = token_to_u_id(token)
    #Check if token user is a member of the specified dm, raise AccessError if not
    if check_user_in_dm(user, dm_id) == False:
        raise AccessError("the authorised user is not a member of this DM")
    #Create empty list to append to and return 
    #Index names used to iterate through and act as a boundry 
    messages = []
    message_start = start
    message_end = start + 50
    #Find particular dm that dm_id refers to 
    #Record components of each message while appending to messages list
    #End loop once start index matches end index or last message is reached
    for msgs in data.data['dms'][dm_id]['messages']:
        tempmsg = {
            'message_id': msgs['message_id'],
            'u_id': msgs['u_id'],
            'message': msgs['message'],
            'time_created': msgs['time_created'],
            'reacts': msgs['reacts'],
            'is_pinned': msgs['is_pinned']
        }
        messages.append(tempmsg)
        if user in messages[-1]['reacts'][0]['u_ids']:
            messages[-1]['reacts'][0]['is_this_user_reacted'] = True
        message_start = message_start + 1
        if message_start == message_end:
            break
    #Check to see if end index is within the total number of messages
    #If not, set to -1 to indicate no more can be returned
    if message_start < message_end:
        message_end = -1
    return{
        'messages': messages,
        'start': start,
        'end': message_end        
    }
