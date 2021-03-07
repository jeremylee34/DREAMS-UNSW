import pytest

from src.channel import channel_join_v1
from src.channel import channel_messages_v1
from src.channel import channel_details_v1
from src.channels import channels_create_v1
from src.auth import auth_register_v1
from src.error import InputError
from src.other import clear_v1

@pytest.fixture
def clear_data():
    clear_v1()

@pytest.fixture
def auth_user1():
    auth_id = auth_register_v1("j.lee34@gmail.com", "12345", "Jeremy", "Lee" )
    return auth_id

## test adding to empty channel
def test_join_empty_channel(clear_data, auth_user1):      
    channel_id = channels_create_v1(auth_user1, "First Channel", True)
    channel_join_v1(auth_user1, channel_id)
    channel_details = channel_details_v1(auth_user1, channel_id)
    assert channel_details["all_members"][0] == auth_user1

## AccessError to be thrown when channel is private
def test_access_error(clear_data, auth_user1):  
    channel_id = channels_create_v1(auth_user1, "First Channel", False)
    with pytest.raises(AccessError):
        assert channel_join_v1(auth_user1, channel_id)

## def test_channel_messages_v1:
