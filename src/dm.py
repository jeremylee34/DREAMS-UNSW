from src.data import data
from src.error import InputError
from src.error import AccessError

from src.helper import check_valid_user
from src.helper import check_valid_dm
from src.helper import token_to_u_id
from src.helper import check_user_in_dm

from src.user import user_profile_v1

import jwt

SECRET = "HELLO"


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
    #Check if dm_id refers to a valid dm, raise InputError if not
    if check_valid_dm(dm_id) == False:
        raise InputError("dm_id does not refer to an existing dm")
    #Check if u_id refers to a valid user, raise InputError if not 
    if check_valid_user(u_id) == False:
        raise InputError("u_id does not refer to a valid user")
    user = token_to_u_id(token)
    #Check if token user is a member of the specified dm, raise AccessError if not
    if check_user_in_dm(user, dm_id) == False:
        raise AccessError("the authorised user is not a member of this DM")
    #Look for corresponding dm through dm_id then append invited user to members list
    #Also update the name of the dm by adding new handle and re-sorting 
    for dm in data['dms']:
        if dm['dm_id'] == dm_id:
            for users in data['users']:
                if users['u_id'] ==  u_id:
                    s_id = users['session_ids'][0]
                    s_token = jwt.encode({'session_id': s_id}, SECRET, algorithm='HS256')
                    profile = user_profile_v1(s_token, u_id)
                    dm['members'].append(profile)
                    handlelist = dm['name'].split(", ")
                    handlelist.append(users['handle_str'])
                    break 
            handlelist.sort()
            handlelist_string = ', '.join(map(str, handlelist))
            dm['name'] = handlelist_string                
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
    #Check if dm_id refers to a valid dm, raise InputError if not
    if check_valid_dm(dm_id) == False:
        raise InputError("dm_id does not refer to an existing dm")
    user = token_to_u_id(token)
    #Check if token user is a member of the specified dm, raise AccessError if not
    if check_user_in_dm(user, dm_id) == False:
        raise AccessError("the authorised user is not a member of this DM")
    #Look for corresponding dm through dm_id then remove token user from members list
    #Also remove the token users handle from name 
    for dm in data['dms']:
        if dm['dm_id'] == dm_id:
            for users in data['users']:
                if users['u_id'] == user:
                    s_id = users['session_ids'][0]
                    s_token = jwt.encode({'session_id': s_id}, SECRET, algorithm='HS256')
                    profile = user_profile_v1(s_token, user)
                    dm['members'].remove(profile)
                    stringU = users['handle_str']                   
                    handlelist = dm['name'].split(", ")
                    handlelist.remove(stringU)
                    break
            handlelist.sort()
            handlelist_string = ', '.join(map(str, handlelist))
            dm['name'] = handlelist_string        
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
    #Check if dm_id refers to a valid dm, raise InputError if not
    if check_valid_dm(dm_id) == False:
        raise InputError("dm_id does not refer to an existing dm")
    #Check if start is greater tham total messages in the DM
    #Raise InputError if it is 
    for dm in data['dms']:
        if dm['dm_id'] == dm_id:
            if start > len(dm['messages']):
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
    for dm in data['dms']:
        if dm['dm_id'] == dm_id:
            for msgs in dm['messages']:
                tempmsg = {
                    'message_id': msgs['message_id'],
                    'u_id': message['u_id'],
                    'message': message['message'],
                    'time_created': message['time_created']
                }
                messages.append(tempmsg)
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
    



