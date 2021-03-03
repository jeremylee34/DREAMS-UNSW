import pytest

from src.channels import channels_list_v1
from src.channels import channels_listall_v1
from src.channels import channels_create_v1
from src.auth import auth_register_v1
from src.error import InputError

def test_channels_list_none():
    auth_id = auth_register_v1("gordonl@gmail.com", "12345", "Gordon", "Liang")
    channels = channels_list_v1(auth_id)
    assert channels is None
def test_channels_list():
    auth_id = auth_register_v1("gordonl@gmail.com", "12345", "Gordon", "Liang")
    channel_id = channels_create_v1(auth_id, "Channel1", True)
    channels = channels_list_v1(auth_id)
    assert channels[0]['channel_id'] == channel_id
    assert channels[0]['name'] == 'Channel1'
def test_channels_list_two_channels():
    auth_id = auth_register_v1("gordonl@gmail.com", "12345", "Gordon", "Liang")
    auth_id2 = auth_register_v1("roland@gmail.com", "12345", "Roland", "Lin")
    channel_id = channels_create_v1(auth_id, "Channel1", True)
    channels_create_v1(auth_id2, "Channel2", True)
    channels = channels_list_v1(auth_id)
    assert channels[0]['channel_id'] == channel_id
    assert channels[0]['name'] == 'Channel1'
    assert channels[1] is None
def test_channels_list_private_channel():
    auth_id = auth_register_v1("gordonl@gmail.com", "12345", "Gordon", "Liang")
    channel_id = channels_create_v1(auth_id, "Channel1", False)
    channel_id2 = channels_create_v1(auth_id, "Channel2", True)
    channels = channels_list_v1(auth_id)
    assert channels[0]['channel_id'] == channel_id
    assert channels[0]['name'] == 'Channel1'
    assert channels[1]['channel_id'] == channel_id2
    assert channels[1]['name'] == 'Channel2'


def test_channels_listall_none():
    auth_id = auth_register_v1("dosirac@gmail.com", "12345", "Jeremy", "Lee")
    channels = channels_listall_v1(auth_id)
    assert channels is None
def test_channels_listall():
    auth_id = auth_register_v1("dosirac@gmail.com", "12345", "Jeremy", "Lee")
    auth_id2 = auth_register_v1("gordonl@gmail.com", "12345", "Gordon", "Liang")
    auth_id3 = auth_register_v1("roland@gmail.com", "12345", "Roland", "Lin")
    channel_id = channels_create_v1(auth_id, "Channel1", True)
    channel_id2 = channels_create_v1(auth_id2, "Channel2", True)
    channel_id3 = channels_create_v1(auth_id3, "Channel3", True)
    channels = channels_listall_v1(auth_id)
    assert channels[0]['channel_id'] == channel_id
    assert channels[0]['name'] == 'Channel1'
    assert channels[1]['channel_id'] == channel_id2
    assert channels[1]['name'] == 'Channel2'
    assert channels[2]['channel_id'] == channel_id3
    assert channels[2]['name'] == 'Channel3'
def test_channels_listall_private_channel():
    auth_id = auth_register_v1("roland@gmail.com", "12345", "Roland", "Lin")
    channel_id = channels_create_v1(auth_id, "Channel1", False)
    channel_id2 = channels_create_v1(auth_id, "Channel2", True)
    channels = channels_listall_v1(auth_id)
    assert channels[0]['channel_id'] == channel_id
    assert channels[0]['name'] == 'Channel1'
    assert channels[1]['channel_id'] == channel_id2
    assert channels[1]['name'] == 'Channel2'


def test_channels_create():
    auth_id = auth_register_v1("roland@gmail.com", "12345", "Roland", "Lin")
    channel_id = channels_create_v1(auth_id, "Channel1", True)
    channels = channels_listall_v1(auth_id)
    assert channels[0]['channel_id'] == channel_id
    assert channels[0]['name'] == 'Channel1'
def test_channels_create_multiple_channels():
    auth_id = auth_register_v1("roland@gmail.com", "12345", "Roland", "Lin")
    channel_id = channels_create_v1(auth_id, "Channel1", True)
    channel_id2 = channels_create_v1(auth_id, "Channel2", True)
    channel_id3 = channels_create_v1(auth_id, "Channel3", True)
    channels = channels_listall_v1(auth_id)
    assert channels[0]['channel_id'] == channel_id
    assert channels[0]['name'] == 'Channel1'
    assert channels[1]['channel_id'] == channel_id2
    assert channels[1]['name'] == 'Channel2'
    assert channels[2]['channel_id'] == channel_id3
    assert channels[2]['name'] == 'Channel3'
def test_channels_create_input_error():
    auth_id = auth_register_v1("roland@gmail.com", "12345", "Roland", "Lin")
    channels_create_v1(auth_id, "Channel1Thisismorethan20", True)
    channels = channels_listall_v1(auth_id)
    with pytest.raises(InputError):
        assert len(channels[0]['name']) > 20
def test_channels_create_private_channel():
    auth_id = auth_register_v1("roland@gmail.com", "12345", "Roland", "Lin")
    channel_id = channels_create_v1(auth_id, "Channel1Thisismorethan20", False)
    channels = channels_listall_v1(auth_id)
    assert channels[0]['channel_id'] == channel_id
    assert channels[0]['name'] == 'Channel1'