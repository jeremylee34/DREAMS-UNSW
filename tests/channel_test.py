
################################################################################
#########################         IMPORTS          #############################
################################################################################

#Import pytest
import pytest 
import jwt

#Import functions from channel, channels and auth for testing
from src.channel import channel_invite_v1
from src.channel import channel_details_v1
from src.channel import channel_messages_v1
from src.channel import channel_join_v1
from src.channel import channel_leave_v1
from src.channel import channel_addowner_v1
from src.channel import channel_removeowner_v1
from src.auth import auth_register_v1
from src.channels import channels_create_v1
from src.channels import channels_list_v1
from src.message import message_send_v1
from src.user import users_all_v1
from src.user import user_profile_v1

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
    user_token1 = auth_register_v1("Roland@gmail.com", "password", "Roland", "Lin")
    return user_token1

@pytest.fixture
def user_token2(user_token1):
    user_token2 = auth_register_v1("Godan@gmail.com", "password", "Godan", "Liang")
    return user_token2
    
@pytest.fixture
def user_token3(user_token1, user_token2):
    user_token3 = auth_register_v1("Jeremy@gmail.com", "password", "Jeremy", "Lee")
    return user_token3
    
@pytest.fixture
def unadded_user_token(user_token1, user_token2, user_token3):
    user_token = auth_register_v1("Bolin@gmail.com", "password", "Bolin", "Ngo")
    return user_token

@pytest.fixture    
def channel_id1(user_token1):
    channel_id1 = channels_create_v1(user_token1['token'], "Channel1", True)
    return channel_id1
    
@pytest.fixture
def channel_id1_priv(user_token1):
    channel_id1_priv = channels_create_v1(user_token1['token'], "PChannel1", False) 
    return channel_id1_priv
    
@pytest.fixture
def channel_details1(user_token1, channel_id1):
    channel_details1 = channel_details_v1(user_token1['token'], channel_id1['channel_id'])
    return channel_details1
    
@pytest.fixture
def channel_details1_priv(user_token1, channel_id1_priv):
    channel_details1_priv = channel_details_v1(user_token1['token'], channel_id1_priv['channel_id'])
    return channel_details1_priv
    
@pytest.fixture
def public_channel(user_token1):
    new_channel = channels_create_v1(user_token1['token'], "Public channel", True)
    return new_channel

#Fixture for clear to prevent clearing of other fixtures
@pytest.fixture
def clear_data():
    clear_v1()

################################################################################
#####################       channel_invite tests       #########################
################################################################################

def test_channel_invite_v1_InputErr1(clear_data, user_token1):
    """
    Tests when user and channel id are not valid for invite
    """
    with pytest.raises(InputError):
        channel_invite_v1(user_token1['token'], "Invalid", user_token1['auth_user_id'])
        
def test_channel_invite_v1_InputErr2(clear_data, user_token1, channel_id1):
    """
    Tests when invited user_id is not valid for invite
    """
    with pytest.raises(InputError):
        channel_invite_v1(user_token1['token'], channel_id1['channel_id'], "Invalid")

def test_channel_invite_v1_InputErr3(clear_data, user_token1, user_token2):
    """
    Tests when channel_id is not valid for invite       
    """
    with pytest.raises(InputError):
        channel_invite_v1(user_token1['token'], "Invalid", user_token2['auth_user_id'])        
        
def test_channel_invite_v1_AccessErr(clear_data, user_token1, user_token2, channel_id1):
    """
    Tests when auth is not in the channel for invite
    """
    with pytest.raises(AccessError):
        assert channel_invite_v1(user_token2['token'], channel_id1['channel_id'], user_token1['auth_user_id'])
    
def test_channel_invite_v1_Add1(clear_data, user_token1, user_token2, channel_id1):
    """
    Tests that a single user has been added to auth's channel for invite
    """
    channel_invite_v1(user_token1['token'], channel_id1['channel_id'], user_token2['auth_user_id'])
    channel_details1 = channel_details_v1(user_token1['token'], channel_id1['channel_id'])
    assert channel_details1['all_members'][-1]['u_id'] == user_token2['auth_user_id']

def test_channel_invite_v1_AddMulti(clear_data, user_token1, channel_id1, user_token2, user_token3):
    """
    Tests that multiple users can be added to auth's channel for invite
    """
    channel_invite_v1(user_token1['token'], channel_id1['channel_id'], user_token2['auth_user_id'])
    channel_invite_v1(user_token1['token'], channel_id1['channel_id'], user_token3['auth_user_id'])
    channel_details1 = channel_details_v1(user_token1['token'], channel_id1['channel_id'])
    assert channel_details1['all_members'][-2]['u_id'] == user_token2['auth_user_id']
    assert channel_details1['all_members'][-1]['u_id'] == user_token3['auth_user_id']
    
def test_channel_invite_v1_AddPriv(clear_data, user_token1, channel_id1_priv, user_token2):
    """
    Tests that user has been added to auth's private channel for invite
    """
    channel_invite_v1(user_token1['token'], channel_id1_priv['channel_id'], user_token2['auth_user_id'])
    channel_details1 = channel_details_v1(user_token1['token'], channel_id1_priv['channel_id'])
    assert channel_details1['all_members'][-1]['u_id'] == user_token2['auth_user_id']

def test_channel_invite_invalid_token(clear_data, user_token1, channel_id1):
    """
    InputError to be thrown when token is invalid
    """
    with pytest.raises(InputError):
        assert channel_invite_v1(INVALID_TOKEN, channel_id1['channel_id'], user_token1['auth_user_id'])

################################################################################
#####################       channel_details tests      #########################
################################################################################
   
def test_channel_details_v1_AccessErr(clear_data, channel_id1, user_token2):
    """
    Tests when auth is not in the channel for details 
    """
    with pytest.raises(AccessError):
        assert channel_details_v1(user_token2['token'], channel_id1['channel_id'])
        
def test_channel_details_v1_InputErr(clear_data, user_token1):
    """
    Tests when channel_id is not valid for details
    """
    with pytest.raises(InputError):
        assert channel_details_v1(user_token1['token'], "invalid")
        
def test_channel_details_v1_NoInv(clear_data, user_token1, channel_details1):
    """
    Tests that correct details are provided when calling function for details
    Only owner in channel 
    """
    assert channel_details1['name'] == 'Channel1'
    assert channel_details1['owner_members'][0]['u_id'] == user_token1['auth_user_id']
    assert channel_details1['all_members'][0]['u_id'] == user_token1['auth_user_id']
    
def test_channel_details_v1_OneInv(clear_data, user_token1, channel_id1, user_token2):
    """
    Tests that correct details are provided when calling function for details
    After inviting one in channel   
    """
    channel_invite_v1(user_token1['token'], channel_id1['channel_id'], user_token2['auth_user_id'])
    channel_details1 = channel_details_v1(user_token1['token'], channel_id1['channel_id'])
    assert channel_details1['name'] == 'Channel1'
    assert channel_details1['owner_members'][0]['u_id'] == user_token1['auth_user_id']
    assert channel_details1['all_members'][0]['u_id'] == user_token1['auth_user_id']
    assert channel_details1['all_members'][1]['u_id'] == user_token2['auth_user_id']
    
def test_channel_details_v1_Priv(clear_data, user_token1, channel_details1_priv):
    """
    Tests that correct details are provided when calling function for details
    In private channel 
    """
    assert channel_details1_priv['name'] == 'PChannel1'
    assert channel_details1_priv['owner_members'][0]['u_id'] == user_token1['auth_user_id']
    assert channel_details1_priv['all_members'][0]['u_id'] == user_token1['auth_user_id']

def test_channel_details_invalid_token(clear_data, channel_id1):
    """
    InputError to be thrown when token is invalid
    """
    with pytest.raises(InputError):
        assert channel_details_v1(INVALID_TOKEN, channel_id1['channel_id'])

################################################################################
#####################      channel_messages tests      #########################
################################################################################

def test_channel_messages_v1_input_error1(clear_data, user_token1, public_channel):
    """
    InputError to be thrown when channel_id is invalid
    """
    start = 0
    with pytest.raises(InputError):
        assert channel_messages_v1(user_token1['token'], INVALID_ID, start)

def test_channel_messages_v1_input_error2(clear_data, user_token1, public_channel):
    """
    InputError2 to be thrown when start is greater than number of messages in channel
    """
    channel_id = public_channel['channel_id']
    message_send_v1(user_token1['token'], channel_id, "Hello")
    start = 1
    with pytest.raises(InputError):
        assert channel_messages_v1(user_token1['token'], channel_id, start)

def test_channel_messages_v1_access_error(clear_data, user_token1, user_token2, public_channel):
    """
    Accessing auth_user2's messages should throw an Access Error since only
    user_token1 is in the channel (added during public_channel function)
    """
    channel_id = public_channel['channel_id']
    message_send_v1(user_token1['token'], channel_id, "Hello")
    start = 0
    with pytest.raises(AccessError):
        # check user_token1's messages (never added to channel)
        assert channel_messages_v1(user_token2['token'], channel_id, start)

def test_channel_messages_v1_simple(clear_data, user_token1, user_token2, public_channel):
    """
    Test if -1 is returned if start + 50 surpasses total messages
    """
    channel_id = public_channel['channel_id']
    message_send_v1(user_token1['token'], channel_id, "Hello")
    start = 0
    messages = channel_messages_v1(user_token1['token'], channel_id, start)
    assert messages['end'] == -1

def test_channel_messages_v1_many(clear_data, user_token1, user_token2, public_channel):
    """
    Test that all messages are returned if start + 50 is within total
    messages in DM
    """
    channel_id = public_channel['channel_id']
    for i in range(0, 50):
        message_send_v1(user_token1['token'], channel_id, f'message{i}')
    start = 0
    messages = channel_messages_v1(user_token1['token'], channel_id, start)
    assert messages['end'] == 50

def test_channel_messages_invalid_token(clear_data, channel_id1):
    """
    InputError to be thrown when token is invalid
    """
    with pytest.raises(InputError):
        assert channel_messages_v1(INVALID_TOKEN, channel_id1['channel_id'], 0)

################################################################################
#####################        channel_join tests        #########################
################################################################################

def test_channel_join_v1_empty_channel(clear_data, user_token1, public_channel):
    """
    Test adding to empty channel
    """      
    channel_id = public_channel['channel_id']
    channel_join_v1(user_token1['token'], channel_id)
    channel_dict = channel_details_v1(user_token1['token'], channel_id)
    assert channel_dict["all_members"][0]['u_id'] == user_token1['auth_user_id']

def test_channel_join_v1_input_error(clear_data, user_token1, public_channel):
    """
    InputError to be thrown when channel_id is invalid
    """
    with pytest.raises(InputError):
        assert channel_join_v1(user_token1['token'], INVALID_ID)

def test_channel_join_v1_access_error(clear_data, user_token1, user_token2, user_token3):
    """
    AccessError to be thrown when channel is private
    """
    new_channel = channels_create_v1(user_token2['token'], "Private channel", False)
    channel_id = new_channel['channel_id']
    with pytest.raises(AccessError):
        assert channel_join_v1(user_token3['token'], channel_id)

def test_channel_join_v1_check_details(clear_data, user_token1, user_token2, public_channel):
    """
    Test if details are correctly added when adding more than one user
    """
    channel_id = public_channel['channel_id']
    channel_join_v1(user_token1['token'], channel_id)
    channel_join_v1(user_token2['token'], channel_id)
    channel_info = channel_details_v1(user_token1['token'], channel_id)
    assert channel_info['all_members'][user_token1['auth_user_id']]['u_id'] == user_token1['auth_user_id']
    assert channel_info['all_members'][user_token1['auth_user_id']]['name_first'] == 'Roland'
    assert channel_info['all_members'][user_token1['auth_user_id']]['name_last'] == 'Lin'
    assert channel_info['all_members'][user_token2['auth_user_id']]['u_id'] == user_token2['auth_user_id']
    assert channel_info['all_members'][user_token2['auth_user_id']]['name_first'] == 'Godan'
    assert channel_info['all_members'][user_token2['auth_user_id']]['name_last'] == 'Liang'

def test_channel_join_invalid_token(clear_data, channel_id1):
    """
    InputError to be thrown when token is invalid
    """
    with pytest.raises(InputError):
        assert channel_join_v1(INVALID_TOKEN, channel_id1['channel_id'])

def test_channel_join_owner_perm(clear_data):
    """
    Test if a **Dreams** owner can join a private channel even if not in channel
    """
    user_id1 = auth_register_v1("Roland@gmail.com", "password", "Roland", "Lin")
    user_id2 = auth_register_v1("Godan@gmail.com", "password", "Godan", "Liang")
    channel = channels_create_v1(user_id2['token'], "Channel", False)
    channel_join_v1(user_id1['token'], channel['channel_id'])
    details = channel_details_v1(user_id1['token'], channel['channel_id'])
    assert details['all_members'][-1]['name_first'] == 'Roland'
        
################################################################################
#####################      channel_addowner tests      #########################
################################################################################

def test_channel_addowner_v1_InputError1(clear_data, user_token1, user_token2):
    """
    InputError happens when Channel ID is not a valid channel
    """
    with pytest.raises(InputError):
        assert channel_addowner_v1(user_token1['token'], INVALID_ID, user_token2['auth_user_id'])   
        
def test_channel_addowner_v1_InputError2(clear_data, user_token1, channel_id1, user_token2):
    """
    InputError happens when u_id is already an owner of the channe'
    """ 
    channel_addowner_v1(user_token1['token'], channel_id1['channel_id'], user_token2['auth_user_id'])
    with pytest.raises(InputError):
        assert channel_addowner_v1(user_token1['token'], channel_id1['channel_id'], user_token2['auth_user_id'])
    with pytest.raises(InputError):
        assert channel_addowner_v1(user_token1['token'], channel_id1['channel_id'], user_token1['auth_user_id'])
        
def test_channel_addowner_v1_AccessError1(clear_data, user_token1, channel_id1, user_token2, user_token3):
    """
    AccessError happens when authorised user is not an owner of DREAMS or the channel
    """ 
    with pytest.raises(AccessError):
        assert channel_addowner_v1(user_token2['token'], channel_id1['channel_id'], user_token3['auth_user_id'])
    channel_invite_v1(user_token1['token'], channel_id1['channel_id'], user_token2['auth_user_id'])
    with pytest.raises(AccessError):
        assert channel_addowner_v1(user_token2['token'], channel_id1['channel_id'], user_token3['auth_user_id'])
        
def test_channel_addowner_v1_Add1(clear_data, user_token1, channel_id1, user_token2):
    """
    Test whether user will be added as an owner of the channel properly
    """
    channel_addowner_v1(user_token1['token'], channel_id1['channel_id'], user_token2['auth_user_id'])
    channel_details1 = channel_details_v1(user_token1['token'], channel_id1['channel_id'])
    assert channel_details1['owner_members'][-1]['u_id'] == user_token2['auth_user_id']
    
def test_channel_addowner_v1_AddMulti(clear_data, user_token1, channel_id1, user_token2, user_token3):
    """
    Test whether multiple users will be added as owner of the channel properly 
    in correct order
    """
    channel_addowner_v1(user_token1['token'], channel_id1['channel_id'], user_token2['auth_user_id'])
    channel_addowner_v1(user_token2['token'], channel_id1['channel_id'], user_token3['auth_user_id'])
    channel_details1 = channel_details_v1(user_token1['token'], channel_id1['channel_id'])
    assert channel_details1['owner_members'][-1]['u_id'] == user_token3['auth_user_id']
    assert channel_details1['owner_members'][-2]['u_id'] == user_token2['auth_user_id'] 
    
def test_channel_addowner_v1_add_unadded_user(clear_data, user_token1, channel_id1, unadded_user_token):
    """
    Test if adding a user not in channel adds them to all members
    """
    channel_addowner_v1(user_token1['token'], channel_id1['channel_id'], unadded_user_token['auth_user_id'])
    channel_details1 = channel_details_v1(user_token1['token'], channel_id1['channel_id'])
    assert channel_details1['owner_members'][-1]['u_id'] == unadded_user_token['auth_user_id']
    assert channel_details1['all_members'][-1]['u_id'] == unadded_user_token['auth_user_id']

def test_channel_addowner_v1_add_added_user(clear_data, user_token1, user_token2, channel_id1):
    """
    Test if adding a user already in channel adds them to owner members
    """
    channel_invite_v1(user_token1['token'], channel_id1['channel_id'], user_token2['auth_user_id'])
    channel_addowner_v1(user_token1['token'], channel_id1['channel_id'], user_token2['auth_user_id'])
    channel_details1 = channel_details_v1(user_token1['token'], channel_id1['channel_id'])
    assert channel_details1['owner_members'][-1]['u_id'] == user_token2['auth_user_id']

def test_channel_addowner_invalid_token(clear_data, user_token1, channel_id1):
    """
    InputError to be thrown when token is invalid
    """
    with pytest.raises(InputError):
        assert channel_addowner_v1(INVALID_TOKEN, channel_id1['channel_id'], user_token1['auth_user_id'])

################################################################################
#####################     channel_removeowner tests    #########################
################################################################################

def test_channel_removeowner_v1_InputError1(clear_data, user_token1, channel_id1, user_token2):
    """
    InputError happens when Channel ID is not a valid channel
    """
    channel_addowner_v1(user_token1['token'], channel_id1['channel_id'], user_token2['auth_user_id'])
    with pytest.raises(InputError):
        assert channel_removeowner_v1(user_token1['token'], INVALID_ID, user_token2['auth_user_id'])
        
def test_channel_removeowner_v1_InputError2(clear_data, user_token1, channel_id1, user_token2):
    """
    InputError happens when u_id is not an owner of the channel
    """
    with pytest.raises(InputError):
        assert channel_removeowner_v1(user_token1['token'], channel_id1['channel_id'], user_token2['auth_user_id'])
    channel_invite_v1(user_token1['token'], channel_id1['channel_id'], user_token2['auth_user_id'])
    with pytest.raises(InputError):
        assert channel_removeowner_v1(user_token1['token'], channel_id1['channel_id'], user_token2['auth_user_id'])
        
def test_channel_removeowner_v1_InputError3(clear_data, user_token1, channel_id1):
    """
    InputError happens when user is the only owner in the channel 
    """
    with pytest.raises(InputError):
        assert channel_removeowner_v1(user_token1['token'], channel_id1['channel_id'], user_token1['auth_user_id'])
        
def test_channel_removeowner_v1_AccessError1(clear_data, user_token1, channel_id1, user_token2, user_token3):
    """
    AccessError happens when authorised user is not an owner of DREAMS or the channel
    """ 
    channel_addowner_v1(user_token1['token'], channel_id1['channel_id'], user_token3['auth_user_id'])
    with pytest.raises(AccessError):
        assert channel_removeowner_v1(user_token2['token'], channel_id1['channel_id'], user_token1['auth_user_id'])
        
def test_channel_removeowner_v1_Remove1(clear_data, user_token1, channel_id1, user_token2):
    """
    Test whether user will be removed as owner of the channel properly
    """
    channel_addowner_v1(user_token1['token'], channel_id1['channel_id'], user_token2['auth_user_id'])
    channel_removeowner_v1(user_token1['token'], channel_id1['channel_id'], user_token2['auth_user_id'])
    channel_details1 = channel_details_v1(user_token1['token'], channel_id1['channel_id'])
    assert channel_details1['owner_members'][-1]['u_id'] == user_token1['auth_user_id']    
    
def test_channel_removeowner_v1_RemoveMulti(clear_data, user_token1, channel_id1, user_token2, user_token3):
    """
    Test whether multiple users will be removed as owner of the channel properly
    """
    channel_addowner_v1(user_token1['token'], channel_id1['channel_id'], user_token2['auth_user_id'])
    channel_addowner_v1(user_token2['token'], channel_id1['channel_id'], user_token3['auth_user_id'])
    channel_removeowner_v1(user_token3['token'], channel_id1['channel_id'], user_token2['auth_user_id'])
    channel_removeowner_v1(user_token3['token'], channel_id1['channel_id'], user_token1['auth_user_id'])
    channel_details1 = channel_details_v1(user_token3['token'], channel_id1['channel_id'])
    assert channel_details1['owner_members'][-1]['u_id'] == user_token3['auth_user_id'] 
    assert channel_details1['owner_members'][0]['u_id'] == user_token3['auth_user_id'] 

def test_channel_removeowner_invalid_token(clear_data, user_token1, channel_id1):
    """
    InputError to be thrown when token is invalid
    """
    with pytest.raises(InputError):
        assert channel_removeowner_v1(INVALID_TOKEN, channel_id1['channel_id'], user_token1['auth_user_id'])

################################################################################
#####################        channel_leave tests       #########################
################################################################################

def test_channel_leave_v1_InputError1(clear_data, user_token1):
    """
    InputError happens when Channel ID is not a valid channel 
    """
    with pytest.raises(InputError):
        assert channel_leave_v1(user_token1['token'], INVALID_ID)
        
def test_channel_leave_v1_AccessError1(clear_data, channel_id1, user_token2):
    """
    AccessError happens when authorised user is not a member of the channel with
    channel_id 
    """
    with pytest.raises(AccessError):
        assert channel_leave_v1(user_token2['token'], channel_id1['channel_id'])

def test_channel_leave_v1_Leave1(clear_data, user_token1, channel_id1, user_token2):
    """
    Test whether a normal member can leave the channel properly
    """
    channel_invite_v1(user_token1['token'], channel_id1['channel_id'], user_token2['auth_user_id'])
    channel_leave_v1(user_token2['token'], channel_id1['channel_id'])
    channel_details1 = channel_details_v1(user_token1['token'], channel_id1['channel_id'])
    assert channel_details1['all_members'][-1]['u_id'] == user_token1['auth_user_id']
    assert channel_details1['all_members'][0]['u_id'] == user_token1['auth_user_id']

def test_channel_leave_v1_LeaveMulti(clear_data, user_token1, channel_id1, user_token2, user_token3):
    """
    Test whether multiple members can leave the channel properly
    """
    channel_invite_v1(user_token1['token'], channel_id1['channel_id'], user_token2['auth_user_id'])
    channel_invite_v1(user_token1['token'], channel_id1['channel_id'], user_token3['auth_user_id'])
    channel_leave_v1(user_token2['token'], channel_id1['channel_id'])
    channel_leave_v1(user_token3['token'], channel_id1['channel_id'])
    channel_details1 = channel_details_v1(user_token1['token'], channel_id1['channel_id'])
    assert channel_details1['all_members'][-1]['u_id'] == user_token1['auth_user_id']
    assert channel_details1['all_members'][0]['u_id'] == user_token1['auth_user_id']
    
def test_channel_leave_v1_LeaveOwner(clear_data, user_token1, channel_id1, user_token2):
    """
    Test whether a owner can leave the channel properly (not the last owner)
    They must be removed from all_members and owner_members
    """
    channel_addowner_v1(user_token1['token'], channel_id1['channel_id'], user_token2['auth_user_id'])
    channel_leave_v1(user_token2['token'], channel_id1['channel_id'])
    channel_details1 = channel_details_v1(user_token1['token'], channel_id1['channel_id'])
    assert channel_details1['all_members'][-1]['u_id'] == user_token1['auth_user_id']
    assert channel_details1['all_members'][0]['u_id'] == user_token1['auth_user_id']
    assert channel_details1['owner_members'][-1]['u_id'] == user_token1['auth_user_id']
    assert channel_details1['owner_members'][0]['u_id'] == user_token1['auth_user_id']

def test_channel_leave_v1_last_owner(clear_data, user_token1, channel_id1):
    """
    Test that the last owner in a channel can not leave
    """
    channel_leave_v1(user_token1['token'], channel_id1['channel_id'])
    channel_details1 = channel_details_v1(user_token1['token'], channel_id1['channel_id'])
    assert channel_details1['owner_members'][-1]['u_id'] == user_token1['auth_user_id']

def test_channel_leave_invalid_token(clear_data, channel_id1):
    """
    InputError to be thrown when token is invalid
    """
    with pytest.raises(InputError):
        assert channel_leave_v1(INVALID_TOKEN, channel_id1['channel_id'])
