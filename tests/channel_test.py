import pytest

from src.channel import channel_join_v1
from src.channel import channel_messages_v1
from src.channel import channel_details_v1
from src.channels import channels_create_v1
from src.auth import auth_register_v1
from src.error import InputError
from src.error import AccessError
from src.other import clear_v1
import src.data

@pytest.fixture
def clear_data():
    clear_v1()

@pytest.fixture
def auth_user1():
    auth_id = auth_register_v1("j.lee34@gmail.com", "123456789", "Jeremy", "Lee" )
    return auth_id['auth_user_id']

"""
Test adding to empty channel
"""
def test_channel_join_v1_empty_channel(clear_data, auth_user1):      
    new_channel = channels_create_v1(auth_user1, "Empty channel", True)
    channel_id = new_channel['channel_id']
    channel_join_v1(auth_user1, channel_id)
    channel_dict = channel_details_v1(auth_user1, channel_id)
    assert channel_dict["all_members"][0]['u_id'] == auth_user1

"""
AccessError to be thrown when channel is private
"""
def test_channel_join_v1_access_error(clear_data, auth_user1):  
    new_channel = channels_create_v1(auth_user1, "Private channel", False)
    channel_id = new_channel['channel_id']
    with pytest.raises(AccessError):
        assert channel_join_v1(auth_user1, channel_id)

"""
InputError to be thrown when channel is private
"""
def test_channel_join_v1_input_error(clear_data, auth_user1):
    new_channel = channels_create_v1(auth_user1, "Public channel", True)
    channel_id = 99999
    with pytest.raises(InputError):
        assert channel_join_v1(auth_user1, channel_id)