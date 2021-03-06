import pytest

from src.channels import channels_list_v1
from src.channels import channels_listall_v1
from src.channels import channels_create_v1
from src.auth import auth_register_v1
from src.error import InputError
from src.other import clear_v1

@pytest.fixture
def clear_data():
    clear_v1()
@pytest.fixture
def auth_id():
    auth_id = auth_register_v1("gordonl@gmail.com", "1234567", "Gordon", "Liang")
    return auth_id
@pytest.fixture
def auth_id2():
    auth_id2 = auth_register_v1("roland@gmail.com", "1234567", "Roland", "Lin")
    return auth_id2
@pytest.fixture
def auth_id3():
    auth_id3 = auth_register_v1("jeremy@gmail.com", "1234567", "Jeremy", "Lee")
    return auth_id3
@pytest.fixture
def channel_list(auth_id):
    channels = channels_list_v1(auth_id['auth_user_id'])
    return channels
@pytest.fixture
def channel_id(auth_id):
    channel_id = channels_create_v1(auth_id['auth_user_id'], "Channel1", True)
    return channel_id
@pytest.fixture
def channel_id2(auth_id2):
    channel_id2 = channels_create_v1(auth_id2['auth_user_id'], "Channel2", True)
    return channel_id2
@pytest.fixture
def channel_id_private(auth_id):
    channel_id = channels_create_v1(auth_id['auth_user_id'], "Channel1", False)
    return channel_id
@pytest.fixture
def channels(auth_id):
    channels = channels_listall_v1(auth_id['auth_user_id'])
    return channels
# Tests channel_list_v1 function when there are no channels created
def test_channels_list_none(clear_data, channel_list):
    assert channel_list['channels'] == []
# Tests channel_list_v1 to see if the function lists the channels correctly
def test_channels_list(clear_data, channel_id, channel_list):
    assert channel_list['channels'][0]['channel_id'] == channel_id['channel_id']
    assert channel_list['channels'][0]['name'] == 'Channel1'
# Tests two different auth_ids and checks if channel_list_v1 lists the correct channel
def test_channels_list_two_channels(clear_data, auth_id, channel_id, channel_id2, channel_list):
    assert channel_list['channels'][0]['channel_id'] == channel_id['channel_id']
    assert channel_list['channels'][0]['name'] == 'Channel1'
    assert len(channel_list['channels']) == 1
# Tests to see if private channel is included 
def test_channels_list_private_channel(clear_data, auth_id, channel_id_private):
    channel_id2 = channels_create_v1(auth_id['auth_user_id'], "Channel2", True)
    channels = channels_list_v1(auth_id['auth_user_id'])
    assert channels['channels'][0]['channel_id'] == channel_id_private['channel_id']
    assert channels['channels'][0]['name'] == 'Channel1'
    assert channels['channels'][1]['channel_id'] == channel_id2['channel_id']
    assert channels['channels'][1]['name'] == 'Channel2'

# Tests if adding no channels works
def test_channels_listall_none(clear_data, auth_id):
    channels = channels_listall_v1(auth_id['auth_user_id'])
    assert channels['channels'] == []
# Tests if multiple channels are added to the channel list
def test_channels_listall(clear_data, auth_id, channel_id, channel_id2, auth_id3):
    channel_id3 = channels_create_v1(auth_id3['auth_user_id'], "Channel3", True)
    channels = channels_listall_v1(auth_id['auth_user_id'])
    assert channels['channels'][0]['channel_id'] == channel_id['channel_id']
    assert channels['channels'][0]['name'] == 'Channel1'
    assert channels['channels'][1]['channel_id'] == channel_id2['channel_id']
    assert channels['channels'][1]['name'] == 'Channel2'
    assert channels['channels'][2]['channel_id'] == channel_id3['channel_id']
    assert channels['channels'][2]['name'] == 'Channel3'
# Tests if private channels are included in the list
def test_channels_listall_private_channel(clear_data, auth_id, channel_id_private):
    channel_id2 = channels_create_v1(auth_id['auth_user_id'], "Channel2", True)
    channels = channels_listall_v1(auth_id['auth_user_id'])
    assert channels['channels'][0]['channel_id'] == channel_id_private['channel_id']
    assert channels['channels'][0]['name'] == 'Channel1'
    assert channels['channels'][1]['channel_id'] == channel_id2['channel_id']
    assert channels['channels'][1]['name'] == 'Channel2'

# Tests if a channel is created
def test_channels_create(clear_data, channel_id, channels):
    assert channels['channels'][0]['channel_id'] == channel_id['channel_id']
    assert channels['channels'][0]['name'] == 'Channel1'
# Tests if multiple channels are created
def test_channels_create_multiple_channels(clear_data, auth_id, channel_id):
    channel_id2 = channels_create_v1(auth_id['auth_user_id'], "Channel2", True)
    channel_id3 = channels_create_v1(auth_id['auth_user_id'], "Channel3", True)
    channels = channels_listall_v1(auth_id['auth_user_id'])
    assert channels['channels'][0]['channel_id'] == channel_id['channel_id']
    assert channels['channels'][0]['name'] == 'Channel1'
    assert channels['channels'][1]['channel_id'] == channel_id2['channel_id']
    assert channels['channels'][1]['name'] == 'Channel2'
    assert channels['channels'][2]['channel_id'] == channel_id3['channel_id']
    assert channels['channels'][2]['name'] == 'Channel3'
# Checks the InputError
def test_channels_create_input_error(clear_data, auth_id, channels):
    with pytest.raises(InputError):
        assert channels_create_v1(auth_id, "Channel1Thisismorethan20", True)
# Checks if entering no name produces an input error
def test_channels_no_name(clear_data, auth_id, channels):
    with pytest.raises(InputError):
        assert channels_create_v1(auth_id, "", True)
# Checks if a private channel is created 
def test_channels_create_private_channel(clear_data, channel_id_private, channels):
    assert channels['channels'][0]['channel_id'] == channel_id_private['channel_id']
    assert channels['channels'][0]['name'] == 'Channel1'