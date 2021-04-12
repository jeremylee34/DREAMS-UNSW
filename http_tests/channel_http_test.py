
################################################################################
#########################         IMPORTS          #############################
################################################################################

import pytest
import jwt
import requests
from src.config import url
from src.other import clear_v1
from src.error import InputError
from src.error import AccessError

################################################################################
#########################     GLOBAL VARIABLES     #############################
################################################################################

INPUT_ERROR = 400
ACCESS_ERROR = 403
INVALID_ID = 9999
SECRET = "HELLO"
INVALID_TOKEN = jwt.encode({"session_id": 9999}, SECRET, algorithm = "HS256")

################################################################################
#########################         FIXTURES         #############################
################################################################################

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
def channel_id1(user_token1):
    channel_id1 = requests.post(f"{url}/channels/create/v2", json={
        'token': user_token1['token'],
        'name': "Channel1",
        'is_public': True
    }).json()
    return channel_id1

@pytest.fixture
def channel_id_priv(user_token1):
    channel_id_priv = requests.post(f"{url}/channels/create/v2", json={
        'token': user_token1['token'],
        'name': "PChannel1",
        'is_public': False
    }).json()
    return channel_id_priv

@pytest.fixture
def channel_details1(user_token1, channel_id1):
    channel_details1 = requests.get(f"{url}/channel/details/v2/token={user_token1['token']}&channel_id={channel_id1['channel_id']}").json()
    return channel_details1

@pytest.fixture
def channel_details1_priv(user_token1, channel_id1_priv):
    channel_details1_priv = requests.get(f"{url}/channel/details/v2?token={user_token1['token']}&channel_id={channel_id1_priv['channel_id']}").json()
    return channel_details1_priv

@pytest.fixture
def public_channel(user_token1):
    new_channel = requests.post(f"{url}/channels/create/v2", json={
        'token': user_token1['token'],
        'name': "Public Channel",
        'is_public': True
    }).json()
    return new_channel

################################################################################
#####################       channel_invite tests       #########################
################################################################################

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
    channel_details1 = requests.get(f"{url}/channel/details/v2?token={reg_info1['token']}&channel_id={channel_id1['channel_id']}")
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

################################################################################
#####################       channel_details tests      #########################
################################################################################

def test_channel_details_v1_InputErr(clear, user_token1):
    """
    InputError happens when channel_id is invalid
    """
    assert requests.get(f"{url}/channel/details/v2?token={user_token1['token']}&channel_id={INVALID_ID}").status_code == 400
    
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
    assert requests.get(f"{url}/channel/details/v2?token={reg_info2['token']}&channel_id={channel_id1['channel_id']}").status_code == 403
    
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
    channel_details1 = requests.get(f"{url}/channel/details/v2?token={reg_info1['token']}&channel_id={channel_id1['channel_id']}")
    channel_details1 = channel_details1.json()
    assert channel_details1['name'] == 'Channel1'
    assert channel_details1['owner_members'][0]['u_id'] == reg_info1['auth_user_id']
    assert channel_details1['all_members'][0]['u_id'] == reg_info1['auth_user_id']
    assert channel_details1['all_members'][1]['u_id'] == reg_info2['auth_user_id']

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
    assert requests.get(f"{url}/channel/details/v2?token=invalid_token&channel_id={channel_id1['channel_id']}").status_code == 400

################################################################################
#####################      channel_messages tests      #########################
################################################################################

def test_channel_messages_v1_input_error1(clear, user_token1, public_channel):
    """
    InputError to be thrown when channel_id is invalidW
    """
    assert requests.get(f"{url}/channel/messages/v2?token={user_token1['token']}&channel_id={INVALID_ID}&start=0").status_code == INPUT_ERROR

def test_channel_messages_v1_input_error2(clear, user_token1, public_channel):
    """
    InputError2 to be thrown when start is greater than number of messages in channel
    """
    channel_id = public_channel['channel_id']
    requests.post(f"{url}/message/send/v2", json={
        'token': user_token1['token'],
        'channel_id': channel_id,
        'message': "Hello"
    })
    start = 1
    assert requests.get(f"{url}/channel/messages/v2?token={user_token1['token']}&channel_id={channel_id}&start={start}").status_code == INPUT_ERROR

def test_channel_messages_v1_access_error(clear, user_token1, user_token2, public_channel):
    """
    Accessing auth_user2's messages should throw an Access Error since only
    user_token1 is in the channel (added during public_channel function)
    """
    channel_id = public_channel['channel_id']
    requests.post(f"{url}/message/send/v2", json={
        'token': user_token1['token'],
        'channel_id': channel_id,
        'message': "Hello"
    })
    start = 0
    assert requests.get(f"{url}/channel/messages/v2?token={user_token2['token']}&channel_id={channel_id}&start={start}").status_code == ACCESS_ERROR

def test_channel_messages_v1_simple(clear, user_token1, user_token2, public_channel):
    channel_id = public_channel['channel_id']
    requests.post(f"{url}/message/send/v2", json={
        'token': user_token1['token'],
        'channel_id': channel_id,
        'message': "Hello"
    })
    start = 0
    messages = requests.get(f"{url}/channel/messages/v2?token={user_token1['token']}&channel_id={channel_id}&start={start}").json()
    assert messages['end'] == -1

def test_channel_messages_v1_many(clear, user_token1, user_token2, public_channel):
    channel_id = public_channel['channel_id']
    for i in range(0, 50):
        requests.post(f"{url}/message/send/v2", json={
            'token': user_token1['token'],
            'channel_id': channel_id,
            'message': f"message number {i}"
        })
    start = 0
    messages = requests.get(f"{url}/channel/messages/v2?token={user_token1['token']}&channel_id={channel_id}&start={start}").json()
    print(messages)
    assert messages['end'] == 50

def test_channel_messages_invalid_token(clear, channel_id1):
    print(channel_id1, INVALID_TOKEN)
    assert requests.get(f"{url}/channel/messages/v2?token={INVALID_TOKEN}&channel_id={channel_id1['channel_id']}&start=0").status_code == INPUT_ERROR

################################################################################
#####################        channel_join tests        #########################
################################################################################

def test_channel_join_v1_empty_channel(clear, user_token1, public_channel):
    """
    Test adding to empty channel
    """      
    channel_id = public_channel['channel_id']
    requests.post(f"{url}/channel/join/v2", json={
        'token': user_token1['token'],
        'channel_id': channel_id
    })
    channel_dict = requests.get(f"{url}/channel/details/v2?token={user_token1['token']}&channel_id={channel_id}").json()
    assert channel_dict["all_members"][0]['u_id'] == user_token1['auth_user_id']

def test_channel_join_v1_input_error(clear, user_token1, public_channel):
    """
    InputError to be thrown when channel_id is invalid
    """
    assert requests.post(f"{url}/channel/join/v2", json={
        'token': user_token1['token'],
        'channel_id': INVALID_ID
    }).status_code == INPUT_ERROR

def test_channel_join_v1_access_error(clear, user_token1, user_token2, user_token3):
    """
    AccessError to be thrown when channel is private
    """
    new_channel = requests.post(f"{url}/channels/create/v2", json={
        'token': user_token2['token'],
        'name': "Private Channel",
        'is_public': False
    }).json()
    channel_id = new_channel['channel_id']
    assert requests.post(f"{url}/channel/join/v2", json={
        'token': user_token3['token'],
        'channel_id': channel_id
    }).status_code == ACCESS_ERROR

def test_channel_join_v1_check_details(clear, user_token1, user_token2, public_channel):
    """
    Test if details are correctly added when adding more than one user
    """
    channel_id = public_channel['channel_id']
    requests.post(f"{url}/channel/join/v2", json={
        'token': user_token1['token'],
        'channel_id': channel_id
    })
    requests.post(f"{url}/channel/join/v2", json={
        'token': user_token2['token'],
        'channel_id': channel_id
    })
    channel_info = requests.get(f"{url}/channel/details/v2?token={user_token1['token']}&channel_id={channel_id}").json()
    assert channel_info['all_members'][user_token1['auth_user_id']]['u_id'] == user_token1['auth_user_id']
    assert channel_info['all_members'][user_token1['auth_user_id']]['name_first'] == 'Godan'
    assert channel_info['all_members'][user_token1['auth_user_id']]['name_last'] == 'Liang'
    assert channel_info['all_members'][user_token2['auth_user_id']]['u_id'] == user_token2['auth_user_id']
    assert channel_info['all_members'][user_token2['auth_user_id']]['name_first'] == 'Jeremy'
    assert channel_info['all_members'][user_token2['auth_user_id']]['name_last'] == 'Lee'

def test_channel_join_invalid_token(clear, channel_id1):
    assert requests.post(f"{url}/channel/join/v2", json={
        'token': INVALID_TOKEN,
        'channel_id': channel_id1['channel_id']
    }).status_code == INPUT_ERROR

def test_channel_join_owner_perm(clear, channel_id1, user_token1, user_token2):
    requests.post(f"{url}/channels/create/v2", json={
        'token': user_token2['token'],
        'name': "Channel",
        'is_public': False
    }).json()
    requests.post(f"{url}/channel/join/v2", json={
        'token': user_token1['token'],
        'channel_id': channel_id1['channel_id']
    })
    details = requests.get(f"{url}/channel/details/v2?token={user_token1['token']}&channel_id={channel_id1['channel_id']}").json()
    assert details['all_members'][-1]['name_first'] == 'Godan'

################################################################################
#####################      channel_addowner tests      #########################
################################################################################

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
        'token': reg_info2['token'],
        'channel_id': channel_id1['channel_id'],
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
    channel_details1 = requests.get(f"{url}/channel/details/v2?token={reg_info1['token']}&channel_id={channel_id1['channel_id']}")
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

################################################################################
#####################     channel_removeowner tests    #########################
################################################################################

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
    requests.post(f"{url}/channel/addowner/v1", json={
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
    channel_details1 = requests.get(f"{url}/channel/details/v2?token={reg_info3['token']}&channel_id={channel_id1['channel_id']}")
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
    }).status_code == 400

################################################################################
#####################        channel_leave tests       #########################
################################################################################

def test_channel_leave_v1_InputError1(clear, user_token1):
    """
    InputError happens when Channel ID is not a valid channel 
    """
    assert requests.post(f"{url}/channel/leave/v1", json={
        'token': user_token1['token'],
        'channel_id': INVALID_ID
    }).status_code == INPUT_ERROR

def test_channel_leave_v1_AccessError1(clear, channel_id1, user_token2):
    """
    AccessError happens when authorised user is not a member of the channel with
    channel_id 
    """
    assert requests.post(f"{url}/channel/leave/v1", json={
        'token': user_token2['token'],
        'channel_id': channel_id1['channel_id']
    }).status_code == ACCESS_ERROR

def test_channel_leave_v1_Leave1(clear, user_token1, channel_id1, user_token2):
    """
    Test whether a normal member can leave the channel properly
    """
    requests.post(f"{url}/channel/invite/v2", json={
        'token': user_token1['token'],
        'channel_id': channel_id1['channel_id'],
        'u_id': user_token2['auth_user_id']
    })
    requests.post(f"{url}/channel/leave/v1", json={
        'token': user_token2['token'],
        'channel_id': channel_id1['channel_id']
    })
    channel_details1 = requests.get(f"{url}/channel/details/v2?token={user_token1['token']}&channel_id={channel_id1['channel_id']}").json()
    assert channel_details1['all_members'][-1]['u_id'] == user_token1['auth_user_id']
    assert channel_details1['all_members'][0]['u_id'] == user_token1['auth_user_id']

def test_channel_leave_v1_LeaveMulti(clear, user_token1, channel_id1, user_token2, user_token3):
    """
    Test whether multiple members can leave the channel properly
    """
    requests.post(f"{url}/channel/invite/v2", json={
        'token': user_token1['token'],
        'channel_id': channel_id1['channel_id'],
        'u_id': user_token2['auth_user_id']
    })
    requests.post(f"{url}/channel/invite/v2", json={
        'token': user_token1['token'],
        'channel_id': channel_id1['channel_id'],
        'u_id': user_token3['auth_user_id']
    })
    requests.post(f"{url}/channel/leave/v1", json={
        'token': user_token2['token'],
        'channel_id': channel_id1['channel_id']
    })
    requests.post(f"{url}/channel/leave/v1", json={
        'token': user_token3['token'],
        'channel_id': channel_id1['channel_id']
    })
    channel_details1 = requests.get(f"{url}/channel/details/v2?token={user_token1['token']}&channel_id={channel_id1['channel_id']}").json()
    assert channel_details1['all_members'][-1]['u_id'] == user_token1['auth_user_id']
    assert channel_details1['all_members'][0]['u_id'] == user_token1['auth_user_id']

def test_channel_leave_v1_LeaveOwner(clear, channel_id1, user_token1, user_token2):
    """
    Test whether a owner can leave the channel properly (not the last owner)
    They must be removed from all_members and owner_members
    """
    requests.post(f"{url}/channel/addowner/v1", json={
        'token': user_token1['token'],
        'channel_id': channel_id1['channel_id'],
        'u_id': user_token2['auth_user_id']
    })
    requests.post(f"{url}/channel/leave/v1", json={
        'token': user_token2['token'],
        'channel_id': channel_id1['channel_id']
    })
    channel_details1 = requests.get(f"{url}/channel/details/v2?token={user_token1['token']}&channel_id={channel_id1['channel_id']}").json()
    print(channel_details1)
    assert channel_details1['all_members'][-1]['u_id'] == user_token1['auth_user_id']
    assert channel_details1['all_members'][0]['u_id'] == user_token1['auth_user_id']
    assert channel_details1['owner_members'][0]['u_id'] == user_token1['auth_user_id']

def test_channel_leave_v1_last_owner(clear, user_token1, channel_id1):
    requests.post(f"{url}/channel/leave/v1", json={
        'token': user_token1['token'],
        'channel_id': channel_id1['channel_id']
    })
    channel_details1 = requests.get(f"{url}/channel/details/v2?token={user_token1['token']}&channel_id={channel_id1['channel_id']}").json()
    assert channel_details1['owner_members'][-1]['u_id'] == user_token1['auth_user_id']
    
def test_channel_leave_invalid_token(clear, channel_id1):
    assert requests.post(f"{url}/channel/leave/v1", json={
        'token': INVALID_TOKEN,
        'channel_id': channel_id1['channel_id']
    }).status_code == INPUT_ERROR
