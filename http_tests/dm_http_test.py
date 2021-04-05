import pytest
import requests
from src.config import port
from src.config import url
from src.other import clear_v1
from src.error import InputError
from src.error import AccessError

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
        'dm_id': 69,
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
        'u_id': 69
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
        'dm_id': 69
    }).status_code == 400
    
