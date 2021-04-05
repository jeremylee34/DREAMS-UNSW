import pytest
import requests
from src.config import url
from src.other import clear_v1
from src.error import InputError
from src.error import AccessError

INPUT_ERROR = 400
ACCESS_ERROR = 403
INVALID_ID = 9999

@pytest.fixture
def clear():
    requests.delete(f"{url}/clear/v1")

@pytest.fixture
def user_token1():
    info1 = requests.post(f"{url}/auth/register/v2", json={
        'email': 'Godan@gmail.com',
        'password': 'password',
        'name_first': 'Godan',
        'name_last': 'Liang'
    }).json()
    return info1

@pytest.fixture
def user_token2(user_token1):
    info2 = requests.post(f"{url}/auth/register/v2", json={
        'email': 'Jeremy@gmail.com',
        'password': 'password',
        'name_first': 'Jeremy',
        'name_last': 'Lee'
    }).json()
    return info2

@pytest.fixture
def user_token3(user_token1, user_token2):
    info3 = requests.post(f"{url}/auth/register/v2", json={
        'email': 'Roland@gmail.com',
        'password': 'password',
        'name_first': 'Roland',
        'name_last': 'Lin'
    }).json()
    return info3

@pytest.fixture
def unadded_user_token(user_token1, user_token2, user_token3):
    user_toke = requests.post(f"{url}/auth/register/v2", json={
        'email': 'Bolin@gmail.com',
        'password': 'password',
        'name_first': 'Bolin',
        'name_last': 'Ngo'
    }).json()
    return user_toke

@pytest.fixture
def dm_1(user_token1, user_token2, user_token3):
    u_ids = [user_token2['auth_user_id'], user_token3['auth_user_id']]
    dm = requests.post(f"{url}/dm/create/v1", json={
        'token': user_token1['token'],
        'u_ids': u_ids
    }).json()
    return dm

@pytest.fixture
def dm_2(user_token1, user_token2):
    u_ids = [user_token2['auth_user_id']]
    dm = requests.post(f"{url}/dm/create/v1", json={
        'token': user_token1['token'],
        'u_ids': u_ids
    }).json()
    return dm

################################################################################
################################################################################
################################################################################


def test_dm_details_v1_input_error(clear, user_token1):
    """
    InputError to be thrown when DM ID is not a valid DM
    """
    assert requests.get(f"{url}/dm/details/v1", json={
        'token': user_token1['token'],
        'dm_id': INVALID_ID
    }).status_code == INPUT_ERROR

def test_dm_details_v1_access_error(clear, unadded_user_token, dm_1):
    """
    AccessError to be thrown when authorised user is not a member of this DM with dm_id
    """
    assert requests.get(f"{url}/dm/details/v1", json={
        'token': unadded_user_token['token'],
        'dm_id': dm_1['dm_id']
    }).status_code == ACCESS_ERROR

def test_dm_details_v1_simple(clear_data, user_token1, user_token2, user_token3, dm_1):
    """
    Testing whether dm_details_v1 returns the correct name and members
    """
    dm_details = requests.get(f"{url}/dm/details/v1", json={
        'token': user_token1['token'],
        'dm_id': dm_1['dm_id']
    }).json()
    user_profile_dict1 = requests.get(f"{url}/user/profile/v2", json={
        'token': user_token1['token'],
        'u_id': user_token1['auth_user_id']
    }).json()
    handle1 = user_profile_dict1['handle_str']
    user_profile_dict2 = requests.get(f"{url}/user/profile/v2", json={
        'token': user_token2['token'],
        'u_id': user_token2['auth_user_id']
    }).json()
    handle2 = user_profile_dict2['handle_str']
    user_profile_dict3 = requests.get(f"{url}/user/profile/v2", json={
        'token': user_token3['token'],
        'u_id': user_token3['auth_user_id']
    }).json()
    handle3 = user_profile_dict3['handle_str']
    assert dm_details['name'] == f"{handle1}, {handle2}, {handle3}"
    assert user_profile_dict1 in dm_details['members']
    assert user_profile_dict2 in dm_details['members']
    assert user_profile_dict3 in dm_details['members']

def test_dm_list_v1_simple(clear_data, user_token1, dm_1, dm_2):
    """
    Testing whether dm_list_v1 returns the list of DMs correctly
    """
    dms = requests.get(f"{url}/dm/list/v1", json={
        'token': user_token1['token']
    }).json()
    expected_dm = {
        'dms': [
            {
                'dm_id': 0,
                'name': 'godanliang, jeremylee, rolandlin'
            },
            {
                'dm_id': 1,
                'name': 'godanliang, jeremylee'
            }
        ]
    }
    assert dms == expected_dm

def test_dm_create_v1_input_error(clear_data, user_token1):
    """
    InputError to be thrown when u_id does not refer to valid user
    """
    assert requests.post(f"{url}/dm/create/v1", json={
        'token': user_token1['token'],
        'u_ids': [INVALID_ID]
    }).status_code == INPUT_ERROR

def test_dm_create_v1_simple(clear_data, user_token1, user_token2, user_token3):
    """
    Testing whether dm_create_v1 returns the correct dm_id and dm_name
    """
    u_ids = [user_token2['auth_user_id'], user_token3['auth_user_id']]  
    dm_1 = requests.post(f"{url}/dm/create/v1", json={
        'token': user_token1['token'],
        'u_ids': u_ids
    }).json()
    assert dm_1['dm_id'] == 0
    user_profile_dict1 = requests.get(f"{url}/user/profile/v2", json={
        'token': user_token1['token'],
        'u_id': user_token1['auth_user_id']
    }).json()
    handle1 = user_profile_dict1['handle_str']
    user_profile_dict2 = requests.get(f"{url}/user/profile/v2", json={
        'token': user_token2['token'],
        'u_id': user_token2['auth_user_id']
    }).json()
    handle2 = user_profile_dict2['handle_str']
    user_profile_dict3 = requests.get(f"{url}/user/profile/v2", json={
        'token': user_token3['token'],
        'u_id': user_token3['auth_user_id']
    }).json()
    handle3 = user_profile_dict3['handle_str']
    assert dm_1['dm_name'] == f"{handle1}, {handle2}, {handle3}"

def test_dm_remove_v1_input_error(clear_data, user_token1):
    """
    InputError to be thrown when dm_id does not refer to a valid DM
    """
    assert requests.delete(f"{url}/dm/remove/v1", json={
        'token': user_token1['token'],
        'dm_id': INVALID_ID
    }).status_code == INPUT_ERROR
    
def test_dm_remove_v1_access_error(clear_data, unadded_user_token, dm_1):
    """
    AccessError to be thrown when the user is not the original DM creator
    """
    assert requests.delete(f"{url}/dm/remove/v1", json={
        'token': unadded_user_token['token'],
        'dm_id': dm_1['dm_id']
    }).status_code == ACCESS_ERROR

def test_dm_remove_v1(clear_data, user_token1, dm_1):
    """
    Testing whether dm is removed. If dm is removed, dm_details_v1 should raise
    InputError since dm is removed.
    """
    requests.delete(f"{url}/dm/remove/v1", json={
        'token': user_token1['token'],
        'dm_id': dm_1['dm_id']
    })
    assert requests.get(f"{url}/dm/details/v1", json={
        'token': user_token1['token'],
        'dm_id': dm_1['dm_id']
    }).status_code == INPUT_ERROR

################################################################################
################################################################################
################################################################################


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
    reg_info1 = reg_info1.json()
    reg_info2 = requests.post(f"{url}/auth/register/v2", json={
        'email': 'Jeremy@gmail.com',
        'password': 'password',
        'name_first': 'Jeremy',
        'name_last': 'Lee'
    })
    reg_info2 = reg_info2.json()
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
    reg_info1 = reg_info1.json()
    reg_info2 = requests.post(f"{url}/auth/register/v2", json={
        'email': 'Jeremy@gmail.com',
        'password': 'password',
        'name_first': 'Jeremy',
        'name_last': 'Lee'
    })
    reg_info2 = reg_info2.json()
    reg_info3 = requests.post(f"{url}/auth/register/v2", json={
        'email': 'Roland@gmail.com',
        'password': 'password',
        'name_first': 'Roland',
        'name_last': 'Lin'
    })
    reg_info3 = reg_info3.json()
    dm_1 = requests.post(f"{url}/dm/create/v1", json={
        'token': reg_info1['token'],
        'u_ids': [reg_info2['auth_user_id'], reg_info3['auth_user_id']]
    })
    dm_1 = dm_1.json()
    assert requests.post(f"{url}/dm/invite/v1", json={
        'token': reg_info1['token'],
        'dm_id': dm_1['dm_id'],
        'u_id': INVALID_ID
    }).status_code == 400
    
def test_dm_invite_v1_InputError3(clear):
    """
    Test whether InputError will be raised if user already in DM is invited
    """
    reg_info1 = requests.post(f"{url}/auth/register/v2", json={
        'email': 'Godan@gmail.com',
        'password': 'password',
        'name_first': 'Godan',
        'name_last': 'Liang'
    })
    reg_info1 = reg_info1.json()
    reg_info2 = requests.post(f"{url}/auth/register/v2", json={
        'email': 'Jeremy@gmail.com',
        'password': 'password',
        'name_first': 'Jeremy',
        'name_last': 'Lee'
    })
    reg_info2 = reg_info2.json()
    reg_info3 = requests.post(f"{url}/auth/register/v2", json={
        'email': 'Roland@gmail.com',
        'password': 'password',
        'name_first': 'Roland',
        'name_last': 'Lin'
    })
    reg_info3 = reg_info3.json()
    dm_2 = requests.post(f"{url}/dm/create/v1", json={
        'token': reg_info1['token'],
        'u_ids': [reg_info2['auth_user_id']]
    })
    dm_2 = dm_2.json()
    requests.post(f"{url}/dm/invite/v1", json={
        'token': reg_info1['token'],
        'dm_id': dm_2['dm_id'],
        'u_id': reg_info3['auth_user_id']
    })
    assert requests.post(f"{url}/dm/invite/v1", json={
        'token': reg_info1['token'],
        'dm_id': dm_2['dm_id'],
        'u_id': reg_info3['auth_user_id']
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
    reg_info1 = reg_info1.json()
    reg_info2 = requests.post(f"{url}/auth/register/v2", json={
        'email': 'Jeremy@gmail.com',
        'password': 'password',
        'name_first': 'Jeremy',
        'name_last': 'Lee'
    })
    reg_info2 = reg_info2.json()
    reg_info3 = requests.post(f"{url}/auth/register/v2", json={
        'email': 'Roland@gmail.com',
        'password': 'password',
        'name_first': 'Roland',
        'name_last': 'Lin'
    })
    reg_info3 = reg_info3.json()
    reg_info4 = requests.post(f"{url}/auth/register/v2", json={
        'email': 'Bolin@gmail.com',
        'password': 'password',
        'name_first': 'Bolin',
        'name_last': 'Ngo'
    })
    reg_info4 = reg_info4.json()
    dm_2 = requests.post(f"{url}/dm/create/v1", json={
        'token': reg_info1['token'],
        'u_ids': [reg_info2['auth_user_id']]
    })
    dm_2 = dm_2.json()
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
    reg_info1 = reg_info1.json()
    reg_info2 = requests.post(f"{url}/auth/register/v2", json={
        'email': 'Jeremy@gmail.com',
        'password': 'password',
        'name_first': 'Jeremy',
        'name_last': 'Lee'
    })
    reg_info2 = reg_info2.json()
    reg_info3 = requests.post(f"{url}/auth/register/v2", json={
        'email': 'Roland@gmail.com',
        'password': 'password',
        'name_first': 'Roland',
        'name_last': 'Lin'
    })
    reg_info3 = reg_info3.json()
    dm_2 = requests.post(f"{url}/dm/create/v1", json={
        'token': reg_info1['token'],
        'u_ids': [reg_info2['auth_user_id']]
    })
    dm_2 = dm_2.json()
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
    reg_info1 = reg_info1.json()
    reg_info2 = requests.post(f"{url}/auth/register/v2", json={
        'email': 'Jeremy@gmail.com',
        'password': 'password',
        'name_first': 'Jeremy',
        'name_last': 'Lee'
    })
    reg_info2 = reg_info2.json()
    reg_info3 = requests.post(f"{url}/auth/register/v2", json={
        'email': 'Roland@gmail.com',
        'password': 'password',
        'name_first': 'Roland',
        'name_last': 'Lin'
    })
    reg_info3 = reg_info3.json()
    reg_info4 = requests.post(f"{url}/auth/register/v2", json={
        'email': 'Bolin@gmail.com',
        'password': 'password',
        'name_first': 'Bolin',
        'name_last': 'Ngo'
    })
    reg_info4 = reg_info4.json()
    dm_2 = requests.post(f"{url}/dm/create/v1", json={
        'token': reg_info1['token'],
        'u_ids': [reg_info2['auth_user_id']]
    })
    dm_2 = dm_2.json()
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
    reg_info1 = reg_info1.json()
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
    reg_info1 = reg_info1.json()
    reg_info2 = requests.post(f"{url}/auth/register/v2", json={
        'email': 'Jeremy@gmail.com',
        'password': 'password',
        'name_first': 'Jeremy',
        'name_last': 'Lee'
    })
    reg_info2 = reg_info2.json()
    reg_info3 = requests.post(f"{url}/auth/register/v2", json={
        'email': 'Roland@gmail.com',
        'password': 'password',
        'name_first': 'Roland',
        'name_last': 'Lin'
    })
    reg_info3 = reg_info3.json()
    dm_2 = requests.post(f"{url}/dm/create/v1", json={
        'token': reg_info1['token'],
        'u_ids': [reg_info2['auth_user_id']]
    })
    dm_2 = dm_2.json()
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
    reg_info1 = reg_info1.json()
    reg_info2 = requests.post(f"{url}/auth/register/v2", json={
        'email': 'Jeremy@gmail.com',
        'password': 'password',
        'name_first': 'Jeremy',
        'name_last': 'Lee'
    })
    reg_info2 = reg_info2.json()
    reg_info3 = requests.post(f"{url}/auth/register/v2", json={
        'email': 'Roland@gmail.com',
        'password': 'password',
        'name_first': 'Roland',
        'name_last': 'Lin'
    })
    reg_info3 = reg_info3.json()
    dm_2 = requests.post(f"{url}/dm/create/v1", json={
        'token': reg_info1['token'],
        'u_ids': [reg_info2['auth_user_id']]
    })
    dm_2 = dm_2.json()
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
    reg_info1 = reg_info1.json()
    reg_info2 = requests.post(f"{url}/auth/register/v2", json={
        'email': 'Jeremy@gmail.com',
        'password': 'password',
        'name_first': 'Jeremy',
        'name_last': 'Lee'
    })
    reg_info2 = reg_info2.json()
    reg_info3 = requests.post(f"{url}/auth/register/v2", json={
        'email': 'Roland@gmail.com',
        'password': 'password',
        'name_first': 'Roland',
        'name_last': 'Lin'
    })
    reg_info3 = reg_info3.json()
    dm_2 = requests.post(f"{url}/dm/create/v1", json={
        'token': reg_info1['token'],
        'u_ids': [reg_info2['auth_user_id']]
    })
    dm_2 = dm_2.json()
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
    reg_info1 = reg_info1.json()
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
    reg_info1 = reg_info1.json()
    reg_info2 = requests.post(f"{url}/auth/register/v2", json={
        'email': 'Jeremy@gmail.com',
        'password': 'password',
        'name_first': 'Jeremy',
        'name_last': 'Lee'
    })
    reg_info2 = reg_info2.json()
    dm_2 = requests.post(f"{url}/dm/create/v1", json={
        'token': reg_info1['token'],
        'u_ids': [reg_info2['auth_user_id']]
    })
    dm_2 = dm_2.json()
    message_id = requests.post(f"{url}/message/senddm/v1", json={
        'token': reg_info1['token'],
        'dm_id': dm_2['dm_id']
        'message': 'hi'
    })
    message_id = message_id.json()
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
    reg_info1 = reg_info1.json()
    reg_info2 = requests.post(f"{url}/auth/register/v2", json={
        'email': 'Jeremy@gmail.com',
        'password': 'password',
        'name_first': 'Jeremy',
        'name_last': 'Lee'
    })
    reg_info2 = reg_info2.json()
    reg_info3 = requests.post(f"{url}/auth/register/v2", json={
        'email': 'Roland@gmail.com',
        'password': 'password',
        'name_first': 'Roland',
        'name_last': 'Lin'
    })
    reg_info3 = reg_info3.json()
    dm_2 = requests.post(f"{url}/dm/create/v1", json={
        'token': reg_info1['token'],
        'u_ids': [reg_info2['auth_user_id']]
    })
    dm_2 = dm_2.json()
    message_id = requests.post(f"{url}/message/senddm/v1", json={
        'token': reg_info1['token'],
        'dm_id': dm_2['dm_id']
        'message': 'hi'
    })
    message_id = message_id.json()
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
    reg_info1 = reg_info1.json()
    reg_info2 = requests.post(f"{url}/auth/register/v2", json={
        'email': 'Jeremy@gmail.com',
        'password': 'password',
        'name_first': 'Jeremy',
        'name_last': 'Lee'
    })
    reg_info2 = reg_info2.json()
    dm_2 = requests.post(f"{url}/dm/create/v1", json={
        'token': reg_info1['token'],
        'u_ids': [reg_info2['auth_user_id']]
    })
    dm_2 = dm_2.json()
    message_id = requests.post(f"{url}/message/senddm/v1", json={
        'token': reg_info1['token'],
        'dm_id': dm_2['dm_id']
        'message': 'hi'
    })
    message_id = message_id.json()
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
    reg_info1 = reg_info1.json()
    reg_info2 = requests.post(f"{url}/auth/register/v2", json={
        'email': 'Jeremy@gmail.com',
        'password': 'password',
        'name_first': 'Jeremy',
        'name_last': 'Lee'
    })
    reg_info2 = reg_info2.json()
    dm_2 = requests.post(f"{url}/dm/create/v1", json={
        'token': reg_info1['token'],
        'u_ids': [reg_info2['auth_user_id']]
    })
    dm_2 = dm_2.json()
    for i in range(0, 50):
        message_id = requests.post(f"{url}/message/senddm/v1", json={
        'token': reg_info1['token'],
        'dm_id': dm_2['dm_id']
        'message': 'hi'
        })
        message_id = message_id.json()
    messages = requests.get(f"{url}/dm/messages/v1", json={
        'token': reg_info1['token'],
        'dm_id': dm_2['dm_id'],
        'start': 0
    })
    messages = messages.json()
    assert messages['end'] == 50
        
