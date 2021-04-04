#Import pytest
import pytest 

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

#Import error from src
from src.error import InputError
from src.error import AccessError

#Import data from src
import src.data

#Import other from src
from src.other import clear_v1

#Make fixtures
@pytest.fixture
def auth_id1():
    auth_id1 = auth_register_v1("Roland@gmail.com", "password", "Roland", "Lin")
    return auth_id1

@pytest.fixture
def auth_id2(auth_id1):
    auth_id2 = auth_register_v1("Godan@gmail.com", "password", "Godan", "Liang")
    return auth_id2
    
@pytest.fixture
def auth_id3(auth_id1, auth_id2):
    auth_id3 = auth_register_v1("Jeremy@gmail.com", "password", "Jeremy", "Lee")
    return auth_id3
    
@pytest.fixture    
def channel_id1(auth_id1):
    channel_id1 = channels_create_v1(auth_id1['token'], "Channel1", True)
    return channel_id1
    
@pytest.fixture
def channel_id1_priv(auth_id1):
    channel_id1_priv = channels_create_v1(auth_id1['token'], "PChannel1", False) 
    return channel_id1_priv
    
@pytest.fixture
def channel_details1(auth_id1, channel_id1):
    channel_details1 = channel_details_v1(auth_id1['token'], channel_id1['channel_id'])
    return channel_details1
    
@pytest.fixture
def channel_details1_priv(auth_id1, channel_id1_priv):
    channel_details1_priv = channel_details_v1(auth_id1['token'], channel_id1_priv['channel_id'])
    return channel_details1_priv
    
@pytest.fixture
def public_channel(auth_id1):
    new_channel = channels_create_v1(auth_id1['token'], "Public channel", True)
    return new_channel

#Fixture for clear to prevent clearing of other fixtures
@pytest.fixture
def clear_data():
    clear_v1()
        
################################################################################
################################################################################
##########################      ROLAND's TESTS    ##############################
################################################################################
################################################################################

#Tests when user and channel id are not valid for invite
def test_channel_invite_v1_InputErr1(clear_data, auth_id1):
    with pytest.raises(InputError):
        channel_invite_v1(auth_id1['token'], "Invalid", "Invalid")
        
#Tests when invited user_id is not valid for invite
def test_channel_invite_v1_InputErr2(clear_data, auth_id1, channel_id1):
    with pytest.raises(InputError):
        channel_invite_v1(auth_id1['token'], channel_id1['channel_id'], "Invalid")

#Tests when channel_id is not valid for invite       
def test_channel_invite_v1_InputErr3(clear_data, auth_id1, auth_id2):
    with pytest.raises(InputError):
        channel_invite_v1(auth_id1['token'], "Invalid", auth_id2['auth_user_id'])        
        
#Tests when auth is not in the channel for invite
def test_channel_invite_v1_AccessErr(clear_data, auth_id1, auth_id2, channel_id1):
    with pytest.raises(AccessError):
        assert channel_invite_v1(auth_id2['token'], channel_id1['channel_id'], auth_id1['auth_user_id'])
    
#Tests that a single user has been added to auth's channel for invite
def test_channel_invite_v1_Add1(clear_data, auth_id1, auth_id2, channel_id1):
    channel_invite_v1(auth_id1['token'], channel_id1['channel_id'], auth_id2['auth_user_id'])
    channel_details1 = channel_details_v1(auth_id1['token'], channel_id1['channel_id'])
    assert channel_details1['all_members'][-1]['u_id'] == auth_id2['auth_user_id']

#Tests that multiple users can be added to auth's channel for invite
def test_channel_invite_v1_AddMulti(clear_data, auth_id1, channel_id1, auth_id2, auth_id3):
    channel_invite_v1(auth_id1['token'], channel_id1['channel_id'], auth_id2['auth_user_id'])
    channel_invite_v1(auth_id1['token'], channel_id1['channel_id'], auth_id3['auth_user_id'])
    channel_details1 = channel_details_v1(auth_id1['token'], channel_id1['channel_id'])
    assert channel_details1['all_members'][-2]['u_id'] == auth_id2['auth_user_id']
    assert channel_details1['all_members'][-1]['u_id'] == auth_id3['auth_user_id']
    
#Tests that user has been added to auth's private channel for invite
def test_channel_invite_v1_AddPriv(clear_data, auth_id1, channel_id1_priv, auth_id2):
    channel_invite_v1(auth_id1['token'], channel_id1_priv['channel_id'], auth_id2['auth_user_id'])
    channel_details1 = channel_details_v1(auth_id1['token'], channel_id1_priv['channel_id'])
    assert channel_details1['all_members'][-1]['u_id'] == auth_id2['auth_user_id']
    
#Tests when auth is not in the channel for details    
def test_channel_details_v1_AccessErr(clear_data, channel_id1, auth_id2):
    with pytest.raises(AccessError):
        assert channel_details_v1(auth_id2['token'], channel_id1['channel_id'])
        
#Tests when channel_id is not valid for details
def test_channel_details_v1_InputErr(clear_data, auth_id1):
    with pytest.raises(InputError):
        assert channel_details_v1(auth_id1['token'], "invalid")
        
#Tests that correct details are provided when calling function for details
#Only owner in channel 
def test_channel_details_v1_NoInv(clear_data, auth_id1, channel_details1):
    assert channel_details1['name'] == 'Channel1'
    assert channel_details1['owner_members'][0]['u_id'] == auth_id1['auth_user_id']
    assert channel_details1['all_members'][0]['u_id'] == auth_id1['auth_user_id']
    
#Tests that correct details are provided when calling function for details
#After inviting one in channel 
def test_channel_details_v1_OneInv(clear_data, auth_id1, channel_id1, auth_id2):
    channel_invite_v1(auth_id1['token'], channel_id1['channel_id'], auth_id2['auth_user_id'])
    channel_details1 = channel_details_v1(auth_id1['token'], channel_id1['channel_id'])
    assert channel_details1['name'] == 'Channel1'
    assert channel_details1['owner_members'][0]['u_id'] == auth_id1['auth_user_id']
    assert channel_details1['all_members'][0]['u_id'] == auth_id1['auth_user_id']
    assert channel_details1['all_members'][1]['u_id'] == auth_id2['auth_user_id']
    
#Tests that correct details are provided when calling function for details
#In private channel 
def test_channel_details_v1_Priv(clear_data, auth_id1, channel_details1_priv):
    assert channel_details1_priv['name'] == 'PChannel1'
    assert channel_details1_priv['owner_members'][0]['u_id'] == auth_id1['auth_user_id']
    assert channel_details1_priv['all_members'][0]['u_id'] == auth_id1['auth_user_id']
     
################################################################################
################################################################################
##########################      JEREMY's TESTS    ##############################
################################################################################
################################################################################

def test_channel_join_v1_empty_channel(clear_data, auth_id1, public_channel):
    """
    Test adding to empty channel
    """      
    channel_id = public_channel['channel_id']
    channel_join_v1(auth_id1['token'], channel_id)
    channel_dict = channel_details_v1(auth_id1['token'], channel_id)
    assert channel_dict["all_members"][0]['u_id'] == auth_id1['auth_user_id']

def test_channel_join_v1_input_error(clear_data, auth_id1, public_channel):
    """
    InputError to be thrown when channel_id is invalid
    """
    channel_id = 99999
    with pytest.raises(InputError):
        assert channel_join_v1(auth_id1['token'], channel_id)


def test_channel_join_v1_access_error(clear_data, auth_id1, auth_id2):
    """
    AccessError to be thrown when channel is private
    """

    new_channel = channels_create_v1(auth_id2['token'], "Private channel", False)
    
    channel_id = new_channel['channel_id']
    with pytest.raises(AccessError):
        assert channel_join_v1(auth_id2['token'], channel_id)

def test_channel_join_v1_check_details(clear_data, auth_id1, auth_id2, public_channel):
    """
    Test if details are correctly added when adding more than one user
    """
    channel_id = public_channel['channel_id']
    channel_join_v1(auth_id1['token'], channel_id)
    channel_join_v1(auth_id2['token'], channel_id)
    channel_info = channel_details_v1(auth_id1['token'], channel_id)
    assert channel_info['all_members'][auth_id1['auth_user_id']]['u_id'] == auth_id1['auth_user_id']
    assert channel_info['all_members'][auth_id1['auth_user_id']]['name_first'] == 'Roland'
    assert channel_info['all_members'][auth_id1['auth_user_id']]['name_last'] == 'Lin'
    assert channel_info['all_members'][auth_id2['auth_user_id']]['u_id'] == auth_id2['auth_user_id']
    assert channel_info['all_members'][auth_id2['auth_user_id']]['name_first'] == 'Godan'
    assert channel_info['all_members'][auth_id2['auth_user_id']]['name_last'] == 'Liang'

def test_channel_messages_v1_input_error1(clear_data, auth_id1, public_channel):
    """
    InputError to be thrown when channel_id is invalid
    """
    channel_id = 99999
    start = 0
    with pytest.raises(InputError):
        assert channel_messages_v1(auth_id1['token'], channel_id, start)


def test_channel_messages_v1_input_error2(clear_data, auth_id1, public_channel):
    """
    InputError2 to be thrown when start is greater than number of messages in channel
    """
    channel_id = public_channel['channel_id']
    start = 1
    message_id = message_send_v1(auth_id1['token'], channel_id, "Hello")
    with pytest.raises(InputError):
        assert channel_messages_v1(auth_id1['token'], channel_id, start)

def test_channel_messages_v1_access_error(clear_data, auth_id1, auth_id2, public_channel):
    """
    Accessing auth_user2's messages should throw an Access Error since only
    auth_id1 is in the channel (added during public_channel function)
    """
    channel_id = public_channel['channel_id']
    message_id = message_send_v1(auth_id1['token'], channel_id, "Hello")
    start = 0
    with pytest.raises(AccessError):
        # check auth_id1's messages (never added to channel)
        assert channel_messages_v1(auth_id2['token'], channel_id, start)
    
