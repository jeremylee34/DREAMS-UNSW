import pytest
import requests
from src.config import port
from src.config import url
from src.other import clear_v1
from src.error import InputError
from src.error import AccessError

INVALID_ID = 1000

@pytest.fixture
def clear():
    requests.delete(f"{url}/clear/v1")


def test_dm_invite_v1_InputError1(clear):
    """
    InputError happnes when dm_id does not refer to a existing DM
    """
    reg_info1 = requests.post(f"{url}/auth/register/v2", json={
        'email': 'Godan@gmail.com',
        'password': 'password',
        'name_first': 'Godan',
        'name_last': 'Liang'
    })
    reg_info2 = requests.post(f"{url}/auth/register/v2", json={
        'email': 'Jeremy@gmail.com',
        'password': 'password',
        'name_first': 'Jeremy',
        'name_last': 'Lee'
    })
    assert requests.post(f"{url}/dm/invite/v1", json={
        'token': reg_info1['token'],
        'dm_id': INVALID_ID,
        'u_id': reg_info2['auth_user_id']
    }).status_code == 400
    
def test_dm_invite_v1_InputError2(clear):
    """
    InputError happens when u_id does not refer to a valid user
    """
    reg_info1 = requests.post(f"{url}/auth/register/v2", json={
        'email': 'Godan@gmail.com',
        'password': 'password',
        'name_first': 'Godan',
        'name_last': 'Liang'
    })
    reg_info2 = requests.post(f"{url}/auth/register/v2", json={
        'email': 'Jeremy@gmail.com',
        'password': 'password',
        'name_first': 'Jeremy',
        'name_last': 'Lee'
    })
    reg_info3 = requests.post(f"{url}/auth/register/v2", json={
        'email': 'Roland@gmail.com',
        'password': 'password',
        'name_first': 'Roland',
        'name_last': 'Lin'
    })
    dm_1 = requests.post(f"{url}/dm/create/v1", json={
        'token': reg_info1['token'],
        'u_ids': [reg_info2['auth_user_id'], reg_info3['auth_user_id']]
    })
    assert requests.post(f"{url}/dm/invite/v1", json={
        'token': reg_info1['token'],
        'dm_id': dm_1['dm_id'],
        'u_id': INVALID_ID
    }).status_code == 400
    
def test_dm_invite_v1_AccessError1(clear):
    """
    AccessError happens when authorised user is not already a member of the DM
    """
    reg_info1 = requests.post(f"{url}/auth/register/v2", json={
        'email': 'Godan@gmail.com',
        'password': 'password',
        'name_first': 'Godan',
        'name_last': 'Liang'
    })
    reg_info2 = requests.post(f"{url}/auth/register/v2", json={
        'email': 'Jeremy@gmail.com',
        'password': 'password',
        'name_first': 'Jeremy',
        'name_last': 'Lee'
    })
    reg_info3 = requests.post(f"{url}/auth/register/v2", json={
        'email': 'Roland@gmail.com',
        'password': 'password',
        'name_first': 'Roland',
        'name_last': 'Lin'
    })
    reg_info4 = requests.post(f"{url}/auth/register/v2", json={
        'email': 'Bolin@gmail.com',
        'password': 'password',
        'name_first': 'Bolin',
        'name_last': 'Ngo'
    })
    dm_2 = requests.post(f"{url}/dm/create/v1", json={
        'token': reg_info1['token'],
        'u_ids': [reg_info2['auth_user_id']]
    })
    assert requests.post(f"{url}/dm/invite/v1", json={
        'token': reg_info4['token'],
        'dm_id': dm_2['dm_id'],
        'u_id': reg_info3['auth_user_id']
    }).status_code == 403
    
def test_dm_invite_v1_Invite1(clear):
    """
    Test whether user will be invited and added to the specified DM
    """
    reg_info1 = requests.post(f"{url}/auth/register/v2", json={
        'email': 'Godan@gmail.com',
        'password': 'password',
        'name_first': 'Godan',
        'name_last': 'Liang'
    })
    reg_info2 = requests.post(f"{url}/auth/register/v2", json={
        'email': 'Jeremy@gmail.com',
        'password': 'password',
        'name_first': 'Jeremy',
        'name_last': 'Lee'
    })
    reg_info3 = requests.post(f"{url}/auth/register/v2", json={
        'email': 'Roland@gmail.com',
        'password': 'password',
        'name_first': 'Roland',
        'name_last': 'Lin'
    })
    dm_2 = requests.post(f"{url}/dm/create/v1", json={
        'token': reg_info1['token'],
        'u_ids': [reg_info2['auth_user_id']]
    })
    requests.post(f"{url}/dm/invite/v1", json={
        'token': reg_info1['token'],
        'dm_id': dm_2['dm_id'],
        'u_id': reg_info3['auth_user_id']
    })
    dm_details = requests.get(f"{url}/dm/details/v1", json={
        'token': reg_info1['token'],
        'dm_id': dm_2['dm_id']
    })
    dm_details = dm_details.json()
    assert dm_details['members'][-1]['u_id'] == reg_info3['auth_user_id'] 
    
def test_dm_invite_v1_Invite2(clear):
    """
    Test whether two users can be invited and added to the specified DM properly
    """
    reg_info1 = requests.post(f"{url}/auth/register/v2", json={
        'email': 'Godan@gmail.com',
        'password': 'password',
        'name_first': 'Godan',
        'name_last': 'Liang'
    })
    reg_info2 = requests.post(f"{url}/auth/register/v2", json={
        'email': 'Jeremy@gmail.com',
        'password': 'password',
        'name_first': 'Jeremy',
        'name_last': 'Lee'
    })
    reg_info3 = requests.post(f"{url}/auth/register/v2", json={
        'email': 'Roland@gmail.com',
        'password': 'password',
        'name_first': 'Roland',
        'name_last': 'Lin'
    })
    reg_info4 = requests.post(f"{url}/auth/register/v2", json={
        'email': 'Bolin@gmail.com',
        'password': 'password',
        'name_first': 'Bolin',
        'name_last': 'Ngo'
    })
    dm_2 = requests.post(f"{url}/dm/create/v1", json={
        'token': reg_info1['token'],
        'u_ids': [reg_info2['auth_user_id']]
    })
    requests.post(f"{url}/dm/invite/v1", json={
        'token': reg_info1['token'],
        'dm_id': dm_2['dm_id'],
        'u_id': reg_info3['auth_user_id']
    })
    requests.post(f"{url}/dm/invite/v1", json={
        'token': reg_info1['token'],
        'dm_id': dm_2['dm_id'],
        'u_id': reg_info4['auth_user_id']
    })
    dm_details = requests.get(f"{url}/dm/details/v1", json={
        'token': reg_info1['token'],
        'dm_id': dm_2['dm_id']
    })
    dm_details = dm_details.json()
    assert dm_details['members'][-2]['u_id'] == reg_info3['auth_user_id']
    assert dm_details['members'][-1]['u_id'] == reg_info4['auth_user_id']



def test_dm_leave_v1_InputError(clear):
    """
    InputError happens when dm_id does not refer to a existing DM
    """
    reg_info1 = requests.post(f"{url}/auth/register/v2", json={
        'email': 'Godan@gmail.com',
        'password': 'password',
        'name_first': 'Godan',
        'name_last': 'Liang'
    })
    assert requests.post(f"{url}/dm/leave/v1", json={
        'token': reg_info1['token'],
        'dm_id': INVALID_ID
    }).status_code == 400
    
def test_dm_leave_v1_AccessError(clear):
    """
    AccessError happens when authorised user is not a member of the DM
    """
    reg_info1 = requests.post(f"{url}/auth/register/v2", json={
        'email': 'Godan@gmail.com',
        'password': 'password',
        'name_first': 'Godan',
        'name_last': 'Liang'
    })
    reg_info2 = requests.post(f"{url}/auth/register/v2", json={
        'email': 'Jeremy@gmail.com',
        'password': 'password',
        'name_first': 'Jeremy',
        'name_last': 'Lee'
    })
    reg_info3 = requests.post(f"{url}/auth/register/v2", json={
        'email': 'Roland@gmail.com',
        'password': 'password',
        'name_first': 'Roland',
        'name_last': 'Lin'
    })
    dm_2 = requests.post(f"{url}/dm/create/v1", json={
        'token': reg_info1['token'],
        'u_ids': [reg_info2['auth_user_id']]
    })
    assert requests.post(f"{url}/dm/leave/v1", json={
        'token': reg_info3['token'],
        'dm_id': dm_2['dm_id']
    }).status_code == 403
    
def test_dm_leave_v1_Leave1(clear):
    """
    Test whether a user can leave the specified DM properly and changes are made
    If the most recent user has left properly, the -1 index of members will be of the previous user
    """
    reg_info1 = requests.post(f"{url}/auth/register/v2", json={
        'email': 'Godan@gmail.com',
        'password': 'password',
        'name_first': 'Godan',
        'name_last': 'Liang'
    })
    reg_info2 = requests.post(f"{url}/auth/register/v2", json={
        'email': 'Jeremy@gmail.com',
        'password': 'password',
        'name_first': 'Jeremy',
        'name_last': 'Lee'
    })
    reg_info3 = requests.post(f"{url}/auth/register/v2", json={
        'email': 'Roland@gmail.com',
        'password': 'password',
        'name_first': 'Roland',
        'name_last': 'Lin'
    })
    dm_2 = requests.post(f"{url}/dm/create/v1", json={
        'token': reg_info1['token'],
        'u_ids': [reg_info2['auth_user_id']]
    })
    requests.post(f"{url}/dm/invite/v1", json={
        'token': reg_info1['token'],
        'dm_id': dm_2['dm_id'],
        'u_id': reg_info3['auth_user_id']
    })
    requests.post(f"{url}/dm/leave/v1", json={
        'token': reg_info3['token'],
        'dm_id': dm_2['dm_id']
    })
    dm_details = requests.get(f"{url}/dm/details/v1", json={
        'token': reg_info1['token'],
        'dm_id': dm_2['dm_id']
    })
    dm_details = dm_details.json()
    assert dm_details['members'][-1]['u_id'] == reg_info2['auth_user_id']
    
def test_dm_leave_v1_LeaveALL(clear):
    """
    Test whether multiple users can leave the specified DM properly
    If all members of the DM leave, the members list for that DM should be empty
    Therefore, calling dm_details_v1 for anyone should raise an AccessError as the user is no longer part of the DM
    """
    reg_info1 = requests.post(f"{url}/auth/register/v2", json={
        'email': 'Godan@gmail.com',
        'password': 'password',
        'name_first': 'Godan',
        'name_last': 'Liang'
    })
    reg_info2 = requests.post(f"{url}/auth/register/v2", json={
        'email': 'Jeremy@gmail.com',
        'password': 'password',
        'name_first': 'Jeremy',
        'name_last': 'Lee'
    })
    reg_info3 = requests.post(f"{url}/auth/register/v2", json={
        'email': 'Roland@gmail.com',
        'password': 'password',
        'name_first': 'Roland',
        'name_last': 'Lin'
    })
    dm_2 = requests.post(f"{url}/dm/create/v1", json={
        'token': reg_info1['token'],
        'u_ids': [reg_info2['auth_user_id']]
    })
    requests.post(f"{url}/dm/invite/v1", json={
        'token': reg_info1['token'],
        'dm_id': dm_2['dm_id'],
        'u_id': reg_info3['auth_user_id']
    })
    requests.post(f"{url}/dm/leave/v1", json={
        'token': reg_info3['token'],
        'dm_id': dm_2['dm_id']
    })
    requests.post(f"{url}/dm/leave/v1", json={
        'token': reg_info2['token'],
        'dm_id': dm_2['dm_id']
    })
    requests.post(f"{url}/dm/leave/v1", json={
        'token': reg_info1['token'],
        'dm_id': dm_2['dm_id']
    })
    assert requests.get(f"{url}/dm/details/v1", json={
        'token': reg_info1['token'],
        'dm_id': dm_2['dm_id']
    }).status_code == 403
    assert requests.get(f"{url}/dm/details/v1", json={
        'token': reg_info2['token'],
        'dm_id': dm_2['dm_id']
    }).status_code == 403
    assert requests.get(f"{url}/dm/details/v1", json={
        'token': reg_info3['token'],
        'dm_id': dm_2['dm_id']
    }).status_code == 403
    
    
    
def test_dm_messages_v1_InputError1(clear):
    """
    InputError happens when dm_id does not refer to a existing DM
    """
    reg_info1 = requests.post(f"{url}/auth/register/v2", json={
        'email': 'Godan@gmail.com',
        'password': 'password',
        'name_first': 'Godan',
        'name_last': 'Liang'
    })
    assert requests.get(f"{url}/dm/messages/v1", json={
        'token': reg_info1['token'],
        'dm_id': INVALID_ID,
        'start': 0
    }).status_code == 400
    
def test_dm_messages_v1_InputError2(clear):
    """
    InputError happens when start is greater than total number of messages in 
    the channel
    """
    reg_info1 = requests.post(f"{url}/auth/register/v2", json={
        'email': 'Godan@gmail.com',
        'password': 'password',
        'name_first': 'Godan',
        'name_last': 'Liang'
    })
    reg_info2 = requests.post(f"{url}/auth/register/v2", json={
        'email': 'Jeremy@gmail.com',
        'password': 'password',
        'name_first': 'Jeremy',
        'name_last': 'Lee'
    })
    dm_2 = requests.post(f"{url}/dm/create/v1", json={
        'token': reg_info1['token'],
        'u_ids': [reg_info2['auth_user_id']]
    })
    message_id = requests.post(f"{url}/message/senddm/v1", json={
        'token': reg_info1['token'],
        'dm_id': dm_2['dm_id']
        'message': 'hi'
    })
    assert requests.get(f"{url}/dm/messages/v1", json={
        'token': reg_info1['token'],
        'dm_id': dm_2['dm_id'],
        'start': 1
    }).status_code == 400

def test_dm_messages_v1_AccessError(clear):
    """
    AccessError happens when authorised user is not a member of the DM
    """
    reg_info1 = requests.post(f"{url}/auth/register/v2", json={
        'email': 'Godan@gmail.com',
        'password': 'password',
        'name_first': 'Godan',
        'name_last': 'Liang'
    })
    reg_info2 = requests.post(f"{url}/auth/register/v2", json={
        'email': 'Jeremy@gmail.com',
        'password': 'password',
        'name_first': 'Jeremy',
        'name_last': 'Lee'
    })
    reg_info3 = requests.post(f"{url}/auth/register/v2", json={
        'email': 'Roland@gmail.com',
        'password': 'password',
        'name_first': 'Roland',
        'name_last': 'Lin'
    })
    dm_2 = requests.post(f"{url}/dm/create/v1", json={
        'token': reg_info1['token'],
        'u_ids': [reg_info2['auth_user_id']]
    })
    message_id = requests.post(f"{url}/message/senddm/v1", json={
        'token': reg_info1['token'],
        'dm_id': dm_2['dm_id']
        'message': 'hi'
    })
    assert requests.get(f"{url}/dm/messages/v1", json={
        'token': reg_info3['token'],
        'dm_id': dm_2['dm_id'],
        'start': 0
    }).status_code == 403
    
def test_dm_messages_v1_simple(clear):
    """
    Test if -1 is returned if start + 50 surpasses total messages
    """
    reg_info1 = requests.post(f"{url}/auth/register/v2", json={
        'email': 'Godan@gmail.com',
        'password': 'password',
        'name_first': 'Godan',
        'name_last': 'Liang'
    })
    reg_info2 = requests.post(f"{url}/auth/register/v2", json={
        'email': 'Jeremy@gmail.com',
        'password': 'password',
        'name_first': 'Jeremy',
        'name_last': 'Lee'
    })
    dm_2 = requests.post(f"{url}/dm/create/v1", json={
        'token': reg_info1['token'],
        'u_ids': [reg_info2['auth_user_id']]
    })
    message_id = requests.post(f"{url}/message/senddm/v1", json={
        'token': reg_info1['token'],
        'dm_id': dm_2['dm_id']
        'message': 'hi'
    })
    messages = requests.get(f"{url}/dm/messages/v1", json={
        'token': reg_info1['token'],
        'dm_id': dm_2['dm_id'],
        'start': 0
    })
    messages = messages.json()
    assert messages['end'] == -1

def test_dm_messages_v1_many_messages(clear):
    """
    Test that all messages are returned if start + 50 is within total
    messages in DM
    """
    reg_info1 = requests.post(f"{url}/auth/register/v2", json={
        'email': 'Godan@gmail.com',
        'password': 'password',
        'name_first': 'Godan',
        'name_last': 'Liang'
    })
    reg_info2 = requests.post(f"{url}/auth/register/v2", json={
        'email': 'Jeremy@gmail.com',
        'password': 'password',
        'name_first': 'Jeremy',
        'name_last': 'Lee'
    })
    dm_2 = requests.post(f"{url}/dm/create/v1", json={
        'token': reg_info1['token'],
        'u_ids': [reg_info2['auth_user_id']]
    })
    for i in range(0, 50):
        message_id = requests.post(f"{url}/message/senddm/v1", json={
        'token': reg_info1['token'],
        'dm_id': dm_2['dm_id']
        'message': 'hi'
        })
    messages = requests.get(f"{url}/dm/messages/v1", json={
        'token': reg_info1['token'],
        'dm_id': dm_2['dm_id'],
        'start': 0
    })
    messages = messages.json()
    assert messages['end'] == 50
        

