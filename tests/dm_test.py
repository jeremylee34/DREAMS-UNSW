#Import pytest
import pytest 

#Import functions from dm for testing
from src.dm import dm_invite_v1
from src.dm import dm_leave_v1
from src.dm import dm_messages_v1
from src.dm import dm_create_v1
from src.dm import dm_details_v1
from src.auth import auth_register_v1
from src.message import message_senddm_v1

#Import error from src
from src.error import InputError
from src.error import AccessError

#Import other from src
from src.other import clear_v1
import src.data

#Make fixtures
@pytest.fixture
def user_token1():
    user_token1 = auth_register_v1("Godan@gmail.com", "password", "Godan", "Liang")
    return user_token1
    
@pytest.fixture
def user_token2(user_token1):
    user_token2 = auth_register_v1("Jeremy@gmail.com", "password", "Jeremy", "Lee")
    return user_token2
    
@pytest.fixture
def user_token3(user_token1, user_token2):
    user_token3 = auth_register_v1("Roland@gmail.com", "password", "Roland", "Lin")
    return user_token3

@pytest.fixture
def unadded_user_token(user_token1, user_token2, user_token3):
    user_token = auth_register_v1("Bolin@gmail.com", "password", "Bolin", "Ngo")
    return user_token

@pytest.fixture
def dm_1(user_token1, user_token2, user_token3):
    u_ids = [user_token2['auth_user_id'], user_token3['auth_user_id']]  
    dm_1 = dm_create_v1(user_token1['token'], u_ids)
    return dm_1

@pytest.fixture
def dm_2(user_token1, user_token2):
    u_ids = [user_token2['auth_user_id']]  
    dm_2 = dm_create_v1(user_token1['token'], u_ids)
    return dm_2

#Fixture for clear to prevent clearing of other fixtures
@pytest.fixture
def clear_data():
    clear_v1()

################################################################################
################################################################################
################################################################################

def test_dm_invite_v1_InputError_1(clear_data, user_token1, user_token2):
    """
    InputError happnes when dm_id does not refer to a existing DM
    """
    with pytest.raises(InputError):
        assert dm_invite_v1(user_token1['token'], 69, user_token2['auth_user_id'])
        
def test_dm_invite_v1_InputError_2(clear_data, user_token1, dm_1):
    """
    InputError happens when u_id does not refer to a valid user
    """
    with pytest.raises(InputError):
        assert dm_invite_v1(user_token1['token'], dm_1['dm_id'], 69)
        
def test_dm_invite_v1_InputError3(clear_data, user_token1, dm_2, user_token3):
    """
    Test whether InputError will be raised if user already in DM is invited
    """
    dm_invite_v1(user_token1['token'], dm_2['dm_id'], user_token3['auth_user_id'])
    with pytest.raises(InputError):
        assert dm_invite_v1(user_token1['token'], dm_2['dm_id'], user_token3['auth_user_id'])
        
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
    
  
    
def test_dm_leave_v1_InputError(clear_data, user_token1):
    """
    InputError happens when dm_id does not refer to a existing DM
    """
    with pytest.raises(InputError):
        assert dm_leave_v1(user_token1['token'], 69)
        
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
        

def test_dm_messages_v1_InputError1(clear_data, user_token1):
    """
    InputError happens when dm_id does not refer to a existing DM
    """
    with pytest.raises(InputError):
        assert dm_messages_v1(user_token1['token'], 69, 0)
        
def test_dm_messages_v1_InputError2(clear_data, user_token1, dm_1):
    """
    InputError happens when start is greater than total number of messages in 
    the channel
    """
    message_id = message_senddm_v1(user_token1['token'], dm_1['dm_id'], 'hi')
    with pytest.raises(InputError):
        assert dm_messages_v1(user_token1['token'], dm_1['dm_id'], 1)
    
        
def test_dm_messages_v1_AccessError(clear_data, unadded_user_token, dm_1):
    """
    AccessError happens when authorised user is not a member of the DM
    """
    with pytest.raises(AccessError):
        assert dm_messages_v1(unadded_user_token['token'], dm_1['dm_id'], 0)
        
