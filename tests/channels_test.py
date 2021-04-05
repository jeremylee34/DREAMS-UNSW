import pytest

from src.channels import channels_list_v1
from src.channels import channels_listall_v1
from src.channels import channels_create_v1
from src.auth import auth_register_v1
from src.error import InputError
from src.error import AccessError
from src.other import clear_v1

@pytest.fixture
def clear():
    '''
    Clears data in the data file
    '''
    clear_v1()
@pytest.fixture
def auth_id():
    '''
    Registers a user
    '''
    user = auth_register_v1("gordonl@gmail.com", "1234567", "Gordon", "Liang")
    return user
@pytest.fixture
def auth_id2():
    '''
    Registers another user
    '''
    user2 = auth_register_v1("roland@gmail.com", "1234567", "Roland", "Lin")
    return user2
@pytest.fixture
def auth_id3():
    '''
    Registers another user
    '''
    user3 = auth_register_v1("jeremy@gmail.com", "1234567", "Jeremy", "Lee")
    return user3
@pytest.fixture
def channel_list(auth_id):
    '''
    Lists a channel specified
    '''
    channels = channels_list_v1(auth_id['token'])
    return channels
@pytest.fixture
def channel_id(auth_id):
    '''
    Creates a channel with specified token
    '''
    channel_id = channels_create_v1(auth_id['token'], "Channel1", True)
    return channel_id
@pytest.fixture
def channel_id2(auth_id2):
    '''
    Creates another channel with specified token
    '''
    channel_id2 = channels_create_v1(auth_id2['token'], "Channel2", True)
    return channel_id2
@pytest.fixture
def channel_id_private(auth_id):
    '''
    Creates a private channel withs specified token
    '''
    channel_id = channels_create_v1(auth_id['token'], "Channel1", False)
    return channel_id
@pytest.fixture
def channels(auth_id):
    '''
    Lists all channels
    '''
    channels = channels_listall_v1(auth_id['token'])
    return channels

def test_channels_list_none(clear, channel_list):
    '''
    Tests channel_list_v1 function when there are no channels created
    '''
    assert channel_list['channels'] == []
def test_channels_list(clear, channel_id, channel_list):
    '''
    Tests channel_list_v1 to see if the function lists the channels correctly
    '''
    assert channel_list['channels'][0]['channel_id'] == channel_id['channel_id']
    assert channel_list['channels'][0]['name'] == 'Channel1'
def test_channels_list_two_channels(clear, auth_id, channel_id, channel_id2, channel_list):
    '''
    Tests two different auth_ids and checks if channel_list_v1 lists only lists one of them
    '''
    assert channel_list['channels'][0]['channel_id'] == channel_id['channel_id']
    assert channel_list['channels'][0]['name'] == 'Channel1'
    assert len(channel_list['channels']) == 1
# Tests to see if private channel is included
def test_channels_list_private_channel(clear, auth_id, channel_id_private):
    channel_id2 = channels_create_v1(auth_id['token'], "Channel2", True)
    channels = channels_list_v1(auth_id['token'])
    assert channels['channels'][0]['channel_id'] == channel_id_private['channel_id']
    assert channels['channels'][0]['name'] == 'Channel1'
    assert channels['channels'][1]['channel_id'] == channel_id2['channel_id']
    assert channels['channels'][1]['name'] == 'Channel2'
def test_channel_list_invalid_id(clear, auth_id):
    with pytest.raises(AccessError):
        assert channels_list_v1('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzZXNzaW9uX2lkIjo0fQ.UWh4yaDf6lPdmJroKBXfBZURXskoLULjM7Es_xZSK6U')

# Tests if adding no channels works properly for listall function
def test_channels_listall_none(clear, auth_id):
    channels = channels_listall_v1(auth_id['token'])
    assert channels['channels'] == []
# Tests if multiple channels are added to the channel list
def test_channels_listall(clear, auth_id, channel_id, channel_id2, auth_id3):
    channel_id3 = channels_create_v1(auth_id3['token'], "Channel3", True)
    channels = channels_listall_v1(auth_id['token'])
    assert channels['channels'][0]['channel_id'] == channel_id['channel_id']
    assert channels['channels'][0]['name'] == 'Channel1'
    assert channels['channels'][1]['channel_id'] == channel_id2['channel_id']
    assert channels['channels'][1]['name'] == 'Channel2'
    assert channels['channels'][2]['channel_id'] == channel_id3['channel_id']
    assert channels['channels'][2]['name'] == 'Channel3'
# Tests if private channels are included in the list
def test_channels_listall_private_channel(clear, auth_id, channel_id_private):
    channel_id2 = channels_create_v1(auth_id['token'], "Channel2", True)
    channels = channels_listall_v1(auth_id['token'])
    assert channels['channels'][0]['channel_id'] == channel_id_private['channel_id']
    assert channels['channels'][0]['name'] == 'Channel1'
    assert channels['channels'][1]['channel_id'] == channel_id2['channel_id']
    assert channels['channels'][1]['name'] == 'Channel2'
def test_channel_listall_invalid_id(clear, auth_id):
    with pytest.raises(AccessError):
        assert channels_listall_v1('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzZXNzaW9uX2lkIjo0fQ.UWh4yaDf6lPdmJroKBXfBZURXskoLULjM7Es_xZSK6U')

# Tests if a channel is created
def test_channels_create(clear, channel_id, channels):
    assert channels['channels'][0]['channel_id'] == channel_id['channel_id']
    assert channels['channels'][0]['name'] == 'Channel1'
# Tests if multiple channels are created
def test_channels_create_multiple_channels(clear, auth_id, channel_id):
    channel_id2 = channels_create_v1(auth_id['token'], "Channel2", True)
    channel_id3 = channels_create_v1(auth_id['token'], "Channel3", True)
    channels = channels_listall_v1(auth_id['token'])
    assert channels['channels'][0]['channel_id'] == channel_id['channel_id']
    assert channels['channels'][0]['name'] == 'Channel1'
    assert channels['channels'][1]['channel_id'] == channel_id2['channel_id']
    assert channels['channels'][1]['name'] == 'Channel2'
    assert channels['channels'][2]['channel_id'] == channel_id3['channel_id']
    assert channels['channels'][2]['name'] == 'Channel3'
# Checks the InputError
def test_channels_create_input_error(clear, auth_id, channels):
    with pytest.raises(InputError):
        assert channels_create_v1(auth_id['token'], "Channel1Thisismorethan20", True)
# Checks if entering no name produces an input error
def test_channels_no_name(clear, auth_id, channels):
    with pytest.raises(InputError):
        assert channels_create_v1(auth_id['token'], "", True)
# Checks if a private channel is created
def test_channels_create_private_channel(clear, channel_id_private, channels):
    assert channels['channels'][0]['channel_id'] == channel_id_private['channel_id']
    assert channels['channels'][0]['name'] == 'Channel1'
def test_channels_create_invalid_id(clear, auth_id):
    with pytest.raises(AccessError):
        assert channels_create_v1('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzZXNzaW9uX2lkIjo0fQ.UWh4yaDf6lPdmJroKBXfBZURXskoLULjM7Es_xZSK6U', "Channel1", True)
