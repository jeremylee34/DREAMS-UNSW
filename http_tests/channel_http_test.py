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

def test_channel_invite_v1_InputErr1(clear):
    """
    InputError happens when user and channel ID are invalid
    """
    reg_info1 = requests.post(f"{url}/auth/register/v2", json={
        'email': 'Godan@gmail.com',
        'password': 'password',
        'name_first': 'Godan',
        'name_last': 'Liang'
    })
    reg_info1 = reg_info1.json()
    assert requests.post(f"{url}/channel/invite/v2", json={
        'token': reg_info1['token'],
        'channel_id': INVALID_ID,
        'u_id': INVALID_ID
    }).status_code == 400
    
def test_channel_invite_v1_InputErr2(clear):
    """
    InputError happens when user ID is invalid
    """
    reg_info1 = requests.post(f"{url}/auth/register/v2", json={
        'email': 'Godan@gmail.com',
        'password': 'password',
        'name_first': 'Godan',
        'name_last': 'Liang'
    })
    reg_info1 = reg_info1.json()
    channel_id1 = requests.post(f"{url}/channels/create/v2", json={
        'token': reg_info1['token'],
        'name': 'Channel1',
        'is_public': True
    })
    channel_id1 = channel_id1.json()
    assert requests.post(f"{url}/channel/invite/v2", json={
        'token': reg_info1['token'],
        'channel_id': channel_id1['channel_id'],
        'u_id': INVALID_ID
    }).status_code == 400
    
def test_channel_invite_v1_InputErr3(clear):
    """
    InputError happens when channel ID is invalid
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
    assert requests.post(f"{url}/channel/invite/v2", json={
        'token': reg_info1['token'],
        'channel_id': INVALID_ID,
        'u_id': reg_info2['auth_user_id']
    }).status_code == 400
    
def test_channel_invite_v1_AccessErr(clear):
    """
    AccessError happens when auth is not in channel for invite
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
    channel_id1 = requests.post(f"{url}/channels/create/v2", json={
        'token': reg_info1['token'],
        'name': 'Channel1',
        'is_public': True
    })
    channel_id1 = channel_id1.json()
    assert requests.post(f"{url}/channel/invite/v2", json={
        'token': reg_info2['token'],
        'channel_id': channel_id1['channel_id'],
        'u_id': reg_info1['auth_user_id']
    }).status_code == 403
    
def test_channel_invite_v1_AddMulti(clear):
    """
    Tests that multiple users can be added to channel for invite 
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
    channel_id1 = requests.post(f"{url}/channels/create/v2", json={
        'token': reg_info1['token'],
        'name': 'Channel1',
        'is_public': True
    })
    channel_id1 = channel_id1.json()
    requests.post(f"{url}/channel/invite/v2", json={
        'token': reg_info1['token'],
        'channel_id': channel_id1['channel_id'],
        'u_id': reg_info2['auth_user_id']
    })
    requests.post(f"{url}/channel/invite/v2", json={
        'token': reg_info1['token'],
        'channel_id': channel_id1['channel_id'],
        'u_id': reg_info3['auth_user_id']
    })
    channel_details1 = requests.get(f"{url}/channel/details/v2", json={
        'token': reg_info1['token'],
        'channel_id': channel_id1['channel_id']
    })
    channel_details1 = channel_details1.json()
    assert channel_details1['all_members'][-2]['u_id'] == reg_info2['auth_user_id']
    assert channel_details1['all_members'][-1]['u_id'] == reg_info3['auth_user_id']

def test_channel_invite_invalid_token(clear):
    """
    Test invalid token for invite
    """
    reg_info1 = requests.post(f"{url}/auth/register/v2", json={
        'email': 'Godan@gmail.com',
        'password': 'password',
        'name_first': 'Godan',
        'name_last': 'Liang'
    })
    reg_info1 = reg_info1.json()
    channel_id1 = requests.post(f"{url}/channels/create/v2", json={
        'token': reg_info1['token'],
        'name': 'Channel1',
        'is_public': True
    })
    channel_id1 = channel_id1.json()
    assert requests.post(f"{url}/channel/invite/v2", json={
        'token': 'invalid_token',
        'channel_id': channel_id1['channel_id'],
        'u_id': reg_info1['auth_user_id']
    }).status_code == 400



def test_channel_details_v1_InputErr(clear):
    """
    InputError happens when channel_id is invalid
    """
    reg_info1 = requests.post(f"{url}/auth/register/v2", json={
        'email': 'Godan@gmail.com',
        'password': 'password',
        'name_first': 'Godan',
        'name_last': 'Liang'
    })
    reg_info1 = reg_info1.json()
    assert requests.get(f"{url}/channel/details/v2", json={
        'token': reg_info1['token'],
        'channel_id': INVALID_ID
    }).status_code == 400
    
def test_channel_details_v1_AccessErr(clear):
    """
    AccessError happens when auth is not in channel 
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
    channel_id1 = requests.post(f"{url}/channels/create/v2", json={
        'token': reg_info1['token'],
        'name': 'Channel1',
        'is_public': True
    })
    channel_id1 = channel_id1.json()
    assert requests.get(f"{url}/channel/details/v2", json={
        'token': reg_info2['token'],
        'channel_id': channel_id1['channel_id']
    }).status_code == 403
    
def test_channel_details_v1_OneInv(clear): 
    """
    Tests that correct details are provided when calling function for details
    After inviting one user
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
    channel_id1 = requests.post(f"{url}/channels/create/v2", json={
        'token': reg_info1['token'],
        'name': 'Channel1',
        'is_public': True
    })
    channel_id1 = channel_id1.json()
    requests.post(f"{url}/channel/invite/v2", json={
        'token': reg_info1['token'],
        'channel_id': channel_id1['channel_id'],
        'u_id': reg_info2['auth_user_id']
    })
    channel_details1 = requests.get(f"{url}/channel/details/v2", json={
        'token': reg_info1['token'],
        'channel_id': channel_id1['channel_id']
    })
    channel_details1 = channel_details1.json()
    assert channel_details1['name'] == 'Channel1'
    assert channel_details1['owner_members'][0]['u_id'] == reg_info1['auth_user_id']
    assert channel_details1['all_members'][0]['u_id'] == reg_info1['auth_user_id']
    assert channel_details1['all_members'][1]['u_id'] == reg_info2['auth_user_id'

def test_channel_details_invalid_token(clear):
    """
    Test invalid token for details
    """
    reg_info1 = requests.post(f"{url}/auth/register/v2", json={
        'email': 'Godan@gmail.com',
        'password': 'password',
        'name_first': 'Godan',
        'name_last': 'Liang'
    })
    reg_info1 = reg_info1.json()
    channel_id1 = requests.post(f"{url}/channels/create/v2", json={
        'token': reg_info1['token'],
        'name': 'Channel1',
        'is_public': True
    })
    channel_id1 = channel_id1.json()
    assert requests.get(f"{url}/channel/details/v2", json={
        'token': 'invalid_token',
        'channel_id': channel_id1['channel_id']
    }).status_code == 400

    
    
def test_channel_addowner_v1_InputError1(clear):
    """
    InputError happens when Channel ID is not a valid channel
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
    assert requests.post(f"{url}/channel/addowner/v1", json={
        'token': reg_info1['token'],
        'channel_id': INVALID_ID,
        'u_id': reg_info2['auth_user_id']
    }).status_code == 400
    
def test_channel_addowner_v1_InputError2(clear):
    """
    InputError happens when u_id is already an owner of the channe'
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
    channel_id1 = requests.post(f"{url}/channels/create/v2", json={
        'token': reg_info1['token'],
        'name': 'Channel1',
        'is_public': True
    })
    channel_id1 = channel_id1.json()
    requests.post(f"{url}/channel/addowner/v1", json={
        'token': reg_info1['token'],
        'channel_id': channel_id1['channel_id'],
        'u_id': reg_info2['auth_user_id']
    })
    assert requests.post(f"{url}/channel/addowner/v1", json={
        'token': reg_info1['token'],
        'channel_id': channel_id1['channel_id'],
        'u_id': reg_info2['auth_user_id']
    }).status_code == 400
    assert requests.post(f"{url}/channel/addowner/v1", json={
        'token': reg_info1['token'],
        'channel_id': channel_id1['channel_id'],
        'u_id': reg_info1['auth_user_id']
    }).status_code == 400
    
def test_channel_addowner_v1_AccessError1(clear):
    """
    AccessError happens when authorised user is not an owner of DREAMS or the channel
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
    channel_id1 = requests.post(f"{url}/channels/create/v2", json={
        'token': reg_info1['token'],
        'name': 'Channel1',
        'is_public': True
    })
    channel_id1 = channel_id1.json()
    assert requests.post(f"{url}/channel/addowner/v1", json={
        'token': reg_info2['token']
        'channel_id': channel_id1['channel_id']
        'u_id': reg_info3['auth_user_id']
    }).status_code == 403
    requests.post(f"{url}/channel/invite/v2", json={
        'token': reg_info1['token'],
        'channel_id': channel_id1['channel_id'],
        'u_id': reg_info2['auth_user_id']
    })
    assert requests.post(f"{url}/channel/addowner/v1", json={
        'token': reg_info2['token'],
        'channel_id': channel_id1['channel_id'],
        'u_id': reg_info3['auth_user_id']
    }).status_code == 403
    
def test_channel_addowner_v1_AddMulti(clear):
    """
    Test whether multiple users will be added as owner of the channel properly 
    in correct order
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
    channel_id1 = requests.post(f"{url}/channels/create/v2", json={
        'token': reg_info1['token'],
        'name': 'Channel1',
        'is_public': True
    })
    channel_id1 = channel_id1.json()
    requests.post(f"{url}/channel/addowner/v1", json={
        'token': reg_info1['token'],
        'channel_id': channel_id1['channel_id'],
        'u_id': reg_info2['auth_user_id']
    })
    requests.post(f"{url}/channel/addowner/v1", json={
        'token': reg_info2['token'],
        'channel_id': channel_id1['channel_id'],
        'u_id': reg_info3['auth_user_id']
    })
    channel_details1 = requests.get(f"{url}/channel/details/v2", json={
        'token': reg_info1['token'],
        'channel_id': channel_id1['channel_id']
    })
    channel_details1 = channel_details1.json()
    assert channel_details1['owner_members'][-1]['u_id'] == reg_info3['auth_user_id']
    assert channel_details1['owner_members'][-2]['u_id'] == reg_info2['auth_user_id'] 

def test_channel_addowner_invalid_token(clear):
    """
    Test invalid token for addowner
    """
    reg_info1 = requests.post(f"{url}/auth/register/v2", json={
        'email': 'Godan@gmail.com',
        'password': 'password',
        'name_first': 'Godan',
        'name_last': 'Liang'
    })
    reg_info1 = reg_info1.json()
    channel_id1 = requests.post(f"{url}/channels/create/v2", json={
        'token': reg_info1['token'],
        'name': 'Channel1',
        'is_public': True
    })
    channel_id1 = channel_id1.json()
    assert requests.post(f"{url}/channel/addowner/v1", json={
        'token': 'invalid_token',
        'channel_id': channel_id1['channel_id'],
        'u_id': reg_info1['auth_user_id']
    }).status_code == 400

    
    
def test_channel_removeowner_v1_InputError1(clear):
    """
    InputError happens when Channel ID is not a valid channel
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
    channel_id1 = requests.post(f"{url}/channels/create/v2", json={
        'token': reg_info1['token'],
        'name': 'Channel1',
        'is_public': True
    })
    channel_id1 = channel_id1.json()
    requests.post(f"{url}/channel/addowner/v1", json={
        'token': reg_info1['token'],
        'channel_id': channel_id1['channel_id'],
        'u_id': reg_info2['auth_user_id']
    })
    assert requests.post(f"{url}/channel/removeowner/v1", json={
        'token': reg_info1['token'],
        'channel_id': INVALID_ID,
        'u_id': reg_info2['auth_user_id']
    }).status_code == 400
    
def test_channel_removeowner_v1_InputError2(clear):
    """
    InputError happens when u_id is not an owner of the channel
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
    channel_id1 = requests.post(f"{url}/channels/create/v2", json={
        'token': reg_info1['token'],
        'name': 'Channel1',
        'is_public': True
    })
    channel_id1 = channel_id1.json()
    assert requests.post(f"{url}/channel/removeowner/v1", json={
        'token': reg_info1['token'],
        'channel_id': channel_id1['channel_id'],
        'u_id': reg_info2['auth_user_id']
    }).status_code == 400
    requests.post(f"{url}/channel/invite/v2", json={
        'token': reg_info1['token'],
        'channel_id': channel_id1['channel_id'],
        'u_id': reg_info2['auth_user_id']
    })
    assert requests.post(f"{url}/channel/removeowner/v1", json={
        'token': reg_info1['token'],
        'channel_id': channel_id1['channel_id'],
        'u_id': reg_info2['auth_user_id']
    }).status_code == 400
    
def test_channel_removeowner_v1_InputError3(clear):
    """
    InputError happens when user is the only owner in the channel 
    """
    reg_info1 = requests.post(f"{url}/auth/register/v2", json={
        'email': 'Godan@gmail.com',
        'password': 'password',
        'name_first': 'Godan',
        'name_last': 'Liang'
    })
    reg_info1 = reg_info1.json()
    channel_id1 = requests.post(f"{url}/channels/create/v2", json={
        'token': reg_info1['token'],
        'name': 'Channel1',
        'is_public': True
    })
    channel_id1 = channel_id1.json()
    assert requests.post(f"{url}/channel/removeowner/v1", json={
        'token': reg_info1['token'],
        'channel_id': channel_id1['channel_id'],
        'u_id': reg_info1['auth_user_id']
    }).status_code == 400
    
def test_channel_removeowner_v1_AccessError1(clear):
    """
    AccessError happens when authorised user is not an owner of DREAMS or the channel
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
    channel_id1 = requests.post(f"{url}/channels/create/v2", json={
        'token': reg_info1['token'],
        'name': 'Channel1',
        'is_public': True
    })
    channel_id1 = channel_id1.json()
    requests.post(f"{url}/channel/invite/v2", json={
        'token': reg_info1['token'],
        'channel_id': channel_id1['channel_id'],
        'u_id': reg_info3['auth_user_id']
    })
    assert requests.post(f"{url}/channel/removeowner/v1", json={
        'token': reg_info2['token'],
        'channel_id': channel_id1['channel_id'],
        'u_id': reg_info1['auth_user_id']
    }).status_code == 403
    
def test_channel_removeowner_v1_RemoveMulti(clear):
    """
    Test whether multiple users will be removed as owner of the channel properly
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
    channel_id1 = requests.post(f"{url}/channels/create/v2", json={
        'token': reg_info1['token'],
        'name': 'Channel1',
        'is_public': True
    })
    channel_id1 = channel_id1.json()
    requests.post(f"{url}/channel/addowner/v1", json={
        'token': reg_info1['token'],
        'channel_id': channel_id1['channel_id'],
        'u_id': reg_info2['auth_user_id']
    })
    requests.post(f"{url}/channel/addowner/v1", json={
        'token': reg_info2['token'],
        'channel_id': channel_id1['channel_id'],
        'u_id': reg_info3['auth_user_id']
    })
    requests.post(f"{url}/channel/removeowner/v1", json={
        'token': reg_info3['token'],
        'channel_id': channel_id1['channel_id'],
        'u_id': reg_info2['auth_user_id']
    })
    requests.post(f"{url}/channel/removeowner/v1", json={
        'token': reg_info3['token'],
        'channel_id': channel_id1['channel_id'],
        'u_id': reg_info1['auth_user_id']
    })
    channel_details1 = requests.get(f"{url}/channel/details/v2", json={
        'token': reg_info3['token'],
        'channel_id': channel_id1['channel_id']
    })
    channel_details1 = channel_details1.json()
    assert channel_details1['owner_members'][-1]['u_id'] == reg_info3['auth_user_id'] 
    assert channel_details1['owner_members'][0]['u_id'] == reg_info3['auth_user_id'] 
    
def test_channel_removeowner_invalid_token(clear):
    """
    Test invalid token for removeowner
    """
    reg_info1 = requests.post(f"{url}/auth/register/v2", json={
        'email': 'Godan@gmail.com',
        'password': 'password',
        'name_first': 'Godan',
        'name_last': 'Liang'
    })
    reg_info1 = reg_info1.json()
    channel_id1 = requests.post(f"{url}/channels/create/v2", json={
        'token': reg_info1['token'],
        'name': 'Channel1',
        'is_public': True
    })
    channel_id1 = channel_id1.json()
    assert requests.post(f"{url}/channel/removeowner/v1", json={
        'token': 'invalid_token',
        'channel_id': channel_id1['channel_id'],
        'u_id': reg_info1['auth_user_id']
    }).status_code == 403

    
