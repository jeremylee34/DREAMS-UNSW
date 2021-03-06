#Import pytest
import pytest 

#Import functions from channel, channels and auth for testing
from src.channel import channel_invite_v1
from src.channel import channel_details_v1
from src.channel import channel_messages_v1
from src.channel import channel_join_v1
from src.auth import auth_register_v1
from src.channels import channels_create_v1

#Import error from src
import src.error

#Import data from src
import src.data

#Import other from src
import src.other





#Make fixtures
@pytest.fixture
def auth_id1():
    auth_id1 = auth_register_v1("Roland@gmail.com", "password", "Roland", "Lin")
    return auth_id1
    
@pytest.fixture
def auth_id2():
    auth_id2 = auth_register_v1("Godan@gmail.com", "password", "Godan", "Liang")
    return auth_id2
    
@pytest.fixture
def auth_id3():
    auth_id3 = auth_register_v1("Jeremy@gmail.com", "password", "Jeremy", "Lee")
    return auth_id3
    
@pytest.fixture    
def channel_id1(auth_id1):
    channel_id1 = channels_create_v1(auth_id1, "Channel1", True)
    return channel_id1
    
@pytest.fixture
def channel_id1_priv(auth_id1):
    channel_id1_priv = channels_create_v1(auth_id1, "PChannel1", False) 
    return channel_id1_priv
    
@pytest.fixture
def channel_list1(auth_id1):
    channel_list1 = channels_list_v1(auth_id1)
    return channel_list1
        
@pytest.fixture
def channel_details1(channel_id1):
    channel_details1 = channel_details_v1(auth_id1, channel_id1)
    return channel_details1
    
@pytest.fixture
def channel_details1_priv(channel_id1_priv):
    channel_details1_priv = channel_details_v1(auth_id1, channel_id1_priv)
    return channel_details1_priv
        
        
        
        
        
#Tests when user and channel id are not valid for invite
def test_channel_invite_v1_InputErr1(auth_id1):
    clear_v1()
    with pytest.raises(InputError):
        assert channel_invite_v1(auth_id1, notvalid, notvalid)
        
#Tests when invited user_id is not valid for invite
def test_channel_invite_v1_InputErr2(channel_id1):
    clear_v1()
    with pytest.raises(InputError):
        assert channel_invite_v1(auth_id1, channel_id1, notvalid)

#Tests when channel_id is not valid for invite       
def test_channel_invite_v1_InputErr3(auth_id1, auth_id2):
    clear_v1()
    with pytest.raises(InputError):
        assert channel_invite_v1(auth_id1, notvalid, auth_id2)        
        
#Tests when auth is not in the channel for invite
def test_channel_invite_v1_AccessErr(auth_id2, channel_id1):
    clear_v1()
    with pytest.raises(AccessError):
        assert channel_invite_v1(auth_id2, channel_id1, auth_id1)
    
#Tests that a single user has been added to auth's channel for invite
def test_channel_invite_v1_Add1(auth_id2, channel_id1, channel_list1):
    clear_v1()
    channel_invite_v1(auth_id1, channel_id1, auth_id2)
    assert channel_list1[0]['all_members'][-1]['u_id'] == auth_id2 

#Tests that multiple users can be added to auth's channel for invite
def test_channel_invite_v1_AddMulti(channel_id1, channel_list1, auth_id2, auth_id3):
    clear_v1()
    channel_invite_v1(auth_id1, channel_id1, auth_id2)
    channel_invite_v1(auth_id1, channel_id1, auth_id2)
    assert channel_list1[0]['all_members'][-2]['u_id'] == auth_id2
    assert channel_list1[0]['all_members'][-1]['u_id'] == auth_id3
    
#Tests that user has been added to auth's private channel for invite
def test_channel_invite_v1_AddPriv(channel_id1_priv, auth_id2, channel_list1):
    clear_v1()
    channel_invite_v1(auth_id1, channel_id1_priv, auth_id2)
    assert channel_list1[0]['all_members'][-1]['u_id'] == auth_id2
    
    
    
    

#Tests when auth is not in the channel for details    
def test_channel_details_v1_AccessErr(channel_id1, auth_id2):
    clear_v1()
    with pytest.raises(AccessError):
        assert channel_details_v1(auth_id2, channel_id1)
        
#Tests when channel_id is not valid for details
def test_channel_details_v1_InputErr(auth_id1):
    clear_v1()
    with pytest.raises(InputError):
        assert channel_details_v1(auth_id1, notvalid)
        
#Tests that correct details are provided when calling function for details
#Only owner in channel 
def test_channel_details_v1_NoInv(channel_details1):
    clear_v1()
    assert channel_details1['name'] == 'Channel1'
    assert channel_details1['owner_members'][0]['u_id'] == auth_id1
    assert channel_details1['all_members'][0]['u_id'] == auth_id1
    
#Tests that correct details are provided when calling function for details
#After inviting one in channel 
def test_channel_details_v1_OneInv(channel_id1, auth_id2):
    clear_v1()
    channel_invite_v1(auth_id1, channel_id1, auth_id2)
    channel_details1 = channel_details_v1(auth_id1, channel_id1)
    assert channel_details1['name'] == 'Channel1'
    assert channel_details1['owner_members'][0]['u_id'] == auth_id1
    assert channel_details1['all_members'][0]['u_id'] == auth_id1
    assert channel_details1['all_members'][1]['u_id'] == auth_id2
    
#Tests that correct details are provided when calling function for details
#In private channel 
def test_channel_details_v1_Priv(channel_details1_priv):
    clear_v1()
    assert channel_details1_priv['name'] == 'PChannel1'
    assert channel_details1_priv['owner_members'][0]['u_id'] == auth_id1
    assert channel_details1_priv['all_members'][0]['u_id] == auth_id1
    
    
    
    
    
def test_channel_messages_v1():
    pass
def test_channel_join_v1():
    pass
