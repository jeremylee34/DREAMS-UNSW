################################################################################
#########################         IMPORTS          #############################
################################################################################

#Import pytest
import pytest 
import jwt

#Import functions from dm for testing
from src.dm import dm_details_v1
from src.dm import dm_list_v1
from src.dm import dm_create_v1
from src.dm import dm_remove_v1
from src.dm import dm_invite_v1
from src.dm import dm_leave_v1
from src.dm import dm_messages_v1
from src.dm import dm_create_v1

from src.auth import auth_register_v1
from src.user import user_profile_v1
from src.message import message_senddm_v1

#Import error from src
from src.error import InputError
from src.error import AccessError

#Import other from src
from src.other import clear_v1

################################################################################
#########################     GLOBAL VARIABLES     #############################
################################################################################

INVALID_ID = 1000
SECRET = "HELLO"
INVALID_TOKEN = jwt.encode({"session_id": 9999}, SECRET, algorithm = "HS256")

################################################################################
#########################         FIXTURES         #############################
################################################################################

#Make fixtures
@pytest.fixture
def user_token1():
    user_toke1 = auth_register_v1("Godan@gmail.com", "password", "Godan", "Liang")
    return user_toke1
    
@pytest.fixture
def user_token2(user_token1):
    user_toke2 = auth_register_v1("Jeremy@gmail.com", "password", "Jeremy", "Lee")
    return user_toke2
    
@pytest.fixture
def user_token3(user_token1, user_token2):
    user_toke3 = auth_register_v1("Roland@gmail.com", "password", "Roland", "Lin")
    return user_toke3

@pytest.fixture
def unadded_user_token(user_token1, user_token2, user_token3):
    user_toke = auth_register_v1("Bolin@gmail.com", "password", "Bolin", "Ngo")
    return user_toke

@pytest.fixture
def dm_1(user_token1, user_token2, user_token3):
    u_ids = [user_token2['auth_user_id'], user_token3['auth_user_id']]  
    dm = dm_create_v1(user_token1['token'], u_ids)
    return dm

@pytest.fixture
def dm_2(user_token1, user_token2):
    u_ids = [user_token2['auth_user_id']]  
    dm = dm_create_v1(user_token1['token'], u_ids)
    return dm

#Fixture for clear to prevent clearing of other fixtures
@pytest.fixture
def clear_data():
    clear_v1()

################################################################################
#########################      dm_details tests    #############################
################################################################################
    
def test_dm_details_v1_input_error(clear_data, user_token1, dm_1):
    """
    InputError to be thrown when DM ID is not a valid DM
    """
    with pytest.raises(InputError):
        assert dm_details_v1(user_token1['token'], INVALID_ID)

def test_dm_details_v1_access_error(clear_data, user_token1, dm_1, unadded_user_token):
    """
    AccessError to be thrown when authorised user is not a member of this DM with dm_id
    """
    with pytest.raises(AccessError):
        assert dm_details_v1(unadded_user_token['token'], dm_1['dm_id'])

def test_dm_details_v1_simple(clear_data, user_token1, user_token2, user_token3, dm_1):
    """
    Testing whether dm_details_v1 returns the correct name and members
    """
    dm_details = dm_details_v1(user_token1['token'], dm_1['dm_id'])
    user_profile_dict1 = user_profile_v1(user_token1['token'], user_token1['auth_user_id'])
    handle1 = user_profile_dict1['handle_str']
    user_profile_dict2 = user_profile_v1(user_token2['token'], user_token2['auth_user_id'])
    handle2 = user_profile_dict2['handle_str']
    user_profile_dict3 = user_profile_v1(user_token3['token'], user_token3['auth_user_id'])
    handle3 = user_profile_dict3['handle_str']
    assert dm_details['name'] == f"{handle1}, {handle2}, {handle3}"
    assert user_profile_dict1 in dm_details['members']
    assert user_profile_dict2 in dm_details['members']
    assert user_profile_dict3 in dm_details['members']

def test_dm_details_v1_invalid_token(clear_data, dm_1):
    """
    InputError to be thrown when token is invalid
    """
    with pytest.raises(InputError):
        assert dm_details_v1(INVALID_TOKEN, dm_1['dm_id'])

################################################################################
#########################       dm_list tests      #############################
################################################################################

def test_dm_list_v1(clear_data, user_token1, dm_1, dm_2):
    """
    Testing whether dm_list_v1 returns the list of DMs correctly
    """
    dms = dm_list_v1(user_token1['token'])
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

def test_dm_list_v1_invalid_token(clear_data):
    """
    InputError to be thrown when token is invalid
    """
    with pytest.raises(InputError):
        assert dm_list_v1(INVALID_TOKEN)

################################################################################
#########################      dm_create tests     #############################
################################################################################

def test_dm_create_v1_input_error(clear_data, user_token1):
    """
    InputError to be thrown when u_id does not refer to valid user
    """
    with pytest.raises(InputError):
        assert dm_create_v1(user_token1['token'], [INVALID_ID])

def test_dm_create_v1_simple(clear_data, user_token1, user_token2, user_token3):
    """
    Testing whether dm_create_v1 returns the correct dm_id and dm_name
    """
    u_ids = [user_token2['auth_user_id'], user_token3['auth_user_id']]  
    dm_1 = dm_create_v1(user_token1['token'], u_ids)
    assert dm_1['dm_id'] == 0
    user_profile_dict1 = user_profile_v1(user_token1['token'], user_token1['auth_user_id'])
    handle1 = user_profile_dict1['handle_str']
    user_profile_dict2 = user_profile_v1(user_token2['token'], user_token2['auth_user_id'])
    handle2 = user_profile_dict2['handle_str']
    user_profile_dict3 = user_profile_v1(user_token3['token'], user_token3['auth_user_id'])
    handle3 = user_profile_dict3['handle_str']
    assert dm_1['dm_name'] == f"{handle1}, {handle2}, {handle3}"

def test_dm_create_v1_invalid_token(clear_data, user_token1):
    """
    InputError to be thrown when token is invalid
    """
    with pytest.raises(InputError):
        assert dm_create_v1(INVALID_TOKEN, [user_token1['auth_user_id']])

################################################################################
#########################      dm_remove tests     #############################
################################################################################

def test_dm_remove_v1_input_error(clear_data, user_token1):
    """
    InputError to be thrown when dm_id does not refer to a valid DM
    """
    with pytest.raises(InputError):
        assert dm_remove_v1(user_token1['token'], INVALID_ID)

def test_dm_remove_v1_access_error(clear_data, unadded_user_token, dm_1):
    """
    AccessError to be thrown when the user is not the original DM creator
    """
    with pytest.raises(AccessError):
        assert dm_remove_v1(unadded_user_token['token'], dm_1['dm_id'])

def test_dm_remove_v1(clear_data, user_token1, dm_1):
    """
    Testing whether dm is removed. If dm is removed, dm_details_v1 should raise
    InputError since dm is removed.
    """
    dm_remove_v1(user_token1['token'], dm_1['dm_id'])
    with pytest.raises(InputError):
        assert dm_details_v1(user_token1['token'], dm_1['dm_id'])

def test_dm_remove_v1_invalid_token(clear_data, dm_1):
    """
    InputError to be thrown when token is invalid
    """
    with pytest.raises(InputError):
        assert dm_remove_v1(INVALID_TOKEN, dm_1['dm_id'])

################################################################################
#########################      dm_invite tests     #############################
################################################################################

def test_dm_invite_v1_InputError_1(clear_data, user_token1, user_token2):
    """
    InputError happnes when dm_id does not refer to a existing DM
    """
    with pytest.raises(InputError):
        assert dm_invite_v1(user_token1['token'], INVALID_ID, user_token2['auth_user_id'])
        
def test_dm_invite_v1_InputError_2(clear_data, user_token1, dm_1):
    """
    InputError happens when u_id does not refer to a valid user
    """
    with pytest.raises(InputError):
        assert dm_invite_v1(user_token1['token'], dm_1['dm_id'], INVALID_ID)
        
def test_dm_invite_v1_AccessError(clear_data, unadded_user_token, dm_2, user_token3):
    """
    AccessError happens when authorised user is not already a member of the DM
    """
    with pytest.raises(AccessError):
        assert dm_invite_v1(unadded_user_token['token'], dm_2['dm_id'], user_token3['auth_user_id'])
        
def test_dm_invite_v1_Invite1(clear_data, user_token1, dm_2, user_token3):
    """
    Test whether user will be invited and added to the specified DM
    """
    dm_invite_v1(user_token1['token'], dm_2['dm_id'], user_token3['auth_user_id'])
    dm_details = dm_details_v1(user_token1['token'], dm_2['dm_id'])
    assert dm_details['members'][-1]['u_id'] == user_token3['auth_user_id']
    
def test_dm_invite_v1_Invite2(clear_data, user_token1, dm_2, user_token3, unadded_user_token):
    """
    Test whether two users can be invited and added to the specified DM properly
    """
    dm_invite_v1(user_token1['token'], dm_2['dm_id'], user_token3['auth_user_id'])
    dm_invite_v1(user_token1['token'], dm_2['dm_id'], unadded_user_token['auth_user_id'])
    dm_details = dm_details_v1(user_token1['token'], dm_2['dm_id'])
    assert dm_details['members'][-2]['u_id'] == user_token3['auth_user_id']
    assert dm_details['members'][-1]['u_id'] == unadded_user_token['auth_user_id']

def test_dm_invite_v1_invalid_token(clear_data, dm_1, user_token1):
    """
    InputError to be thrown when token is invalid
    """
    with pytest.raises(InputError):
        assert dm_invite_v1(INVALID_TOKEN, dm_1['dm_id'], user_token1['auth_user_id'])

################################################################################
#########################      dm_leave tests      #############################
################################################################################    

def test_dm_leave_v1_InputError(clear_data, user_token1):
    """
    InputError happens when dm_id does not refer to a existing DM
    """
    with pytest.raises(InputError):
        assert dm_leave_v1(user_token1['token'], INVALID_ID)
        
def test_dm_leave_v1_AccessError(clear_data, unadded_user_token, dm_2):
    """
    AccessError happens when authorised user is not a member of the DM
    """
    with pytest.raises(AccessError):
        assert dm_leave_v1(unadded_user_token['token'], dm_2['dm_id'])
        
def test_dm_leave_v1_Leave1(clear_data, user_token1, user_token2, user_token3, dm_2):
    """
    Test whether a user can leave the specified DM properly and changes are made
    If the most recent user has left properly, the -1 index of members will be of the previous user
    """
    dm_invite_v1(user_token1['token'], dm_2['dm_id'], user_token3['auth_user_id'])    
    dm_leave_v1(user_token3['token'], dm_2['dm_id'])
    dm_details = dm_details_v1(user_token1['token'], dm_2['dm_id'])    
    assert dm_details['members'][-1]['u_id'] == user_token2['auth_user_id']
    
def test_dm_leave_v1_LeaveAll(clear_data, user_token1, user_token3, user_token2, dm_2):
    """
    Test whether multiple users can leave the specified DM properly
    If all members of the DM leave, the members list for that DM should be empty
    Therefore, calling dm_details_v1 for anyone should raise an AccessError as the user is no longer part of the DM
    """
    dm_invite_v1(user_token1['token'], dm_2['dm_id'], user_token3['auth_user_id'])
    dm_leave_v1(user_token3['token'], dm_2['dm_id'])
    dm_leave_v1(user_token2['token'], dm_2['dm_id'])
    dm_leave_v1(user_token1['token'], dm_2['dm_id'])
    with pytest.raises(AccessError):        
        assert dm_details_v1(user_token1['token'], dm_2['dm_id'])
    with pytest.raises(AccessError):        
        assert dm_details_v1(user_token2['token'], dm_2['dm_id'])
    with pytest.raises(AccessError):        
        assert dm_details_v1(user_token3['token'], dm_2['dm_id'])

def test_dm_leave_v1_invalid_token(clear_data, dm_1):
    """
    InputError to be thrown when token is invalid
    """
    with pytest.raises(InputError):
        assert dm_leave_v1(INVALID_TOKEN, dm_1['dm_id'])

################################################################################
#########################     dm_messages tests    #############################
################################################################################        

def test_dm_messages_v1_InputError1(clear_data, user_token1):
    """
    InputError happens when dm_id does not refer to a existing DM
    """
    with pytest.raises(InputError):
        assert dm_messages_v1(user_token1['token'], INVALID_ID, 0)
        
def test_dm_messages_v1_InputError2(clear_data, user_token1, dm_1):
    """
    InputError happens when start is greater than total number of messages in 
    the channel
    """
    message_id = message_senddm_v1(user_token1['token'], dm_1['dm_id'], 'hi')
    with pytest.raises(InputError):
        assert dm_messages_v1(user_token1['token'], dm_1['dm_id'], 1)
    
        
def test_dm_messages_v1_AccessError(clear_data, unadded_user_token, dm_1, user_token1):
    """
    AccessError happens when authorised user is not a member of the DM
    """
    message_id = message_senddm_v1(user_token1['token'], dm_1['dm_id'], 'hi')
    with pytest.raises(AccessError):
        assert dm_messages_v1(unadded_user_token['token'], dm_1['dm_id'], 0)


def test_dm_messages_v1_simple(clear_data, dm_1, user_token1):
    """
    AccessError happens when authorised user is not a member of the DM
    """
    message_id = message_senddm_v1(user_token1['token'], dm_1['dm_id'], 'hi')
    messages = dm_messages_v1(user_token1['token'], dm_1['dm_id'], 0)
    assert messages['end'] == -1

def test_dm_messages_v1_many_messages(clear_data, dm_1, user_token1):
    """
    Test that all messages are returned if start + 50 is within total
    messages in DM
    """
    for i in range(0, 50):
        message_id = message_senddm_v1(user_token1['token'], dm_1['dm_id'], 'hi')
    messages = dm_messages_v1(user_token1['token'], dm_1['dm_id'], 0)
    assert messages['end'] == 50

def test_dm_messages_v1_invalid_token(clear_data, dm_1):
    """
    InputError to be thrown when token is invalid
    """
    with pytest.raises(InputError):
        assert dm_messages_v1(INVALID_TOKEN, dm_1['dm_id'], 0)


