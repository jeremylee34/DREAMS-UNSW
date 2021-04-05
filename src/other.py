'''
Implementation of other functions which includes clear_v1,
search_v1, notifications_get_v1
Written by Kanit Srihakorth and Tharushi Gunawardana
'''
from src.data import data
def clear_v1():
    """
    Description of function:
        Removes all existing users and their information
    Parameters:
        None
    Exceptions:
        None
    Returns:
        Empty dictionary
    """           
    for x in data["users"]:
        x["session_ids"].clear()
    data['users'].clear()
    data['channels'].clear()
    data['dms'].clear() 
    data['message_ids'].clear() 
    data['token_list'].clear()
    data['notifications'].clear()
    return {}

def search_v1(auth_user_id, query_str):
    return {
        'messages': [
            {
                'message_id': 1,
                'u_id': 1,
                'message': 'Hello world',
                'time_created': 1582426789,
            }
        ],
    }
