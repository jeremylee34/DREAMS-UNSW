'''
Http tests for channels functions 
Written by Gordon Liang
'''
import pytest
import requests
from src.config import url

@pytest.fixture
def clear():
    '''
    Clears data in data file
    '''
    requests.delete(f"{url}/clear/v1")
@pytest.fixture
def register_info():
    '''
    Registers a user
    '''
    register_info = requests.post(f"{url}/auth/register/v2", json={
        'email': 'gordon@gmail.com',
        'password': '12345678',
        'name_first': 'Gordon',
        'name_last': 'Liang'
    })
    register_info = register_info.json()
    return register_info
@pytest.fixture
def channels(register_info):
    '''
    Lists the channels a given user is part of 
    '''
    channels = requests.get(f"{url}/channels/list/v2?token={register_info['token']}").json()
    return channels
@pytest.fixture
def create(register_info):
    '''
    Creates a channel
    '''
    requests.post(f"{url}/channels/create/v2", json={
        'token': register_info['token'],
        'name': 'Channel1',
        'is_public': True
    })
@pytest.fixture
def all_channels(register_info):
    '''
    Lists all the channels in Dreams
    '''
    all_channels = requests.get(f"{url}/channels/listall/v2?token={register_info['token']}").json()
    return all_channels
@pytest.fixture
def create2(register_info):
    '''
    Creates another channel
    '''
    requests.post(f"{url}/channels/create/v2", json={
        'token': register_info['token'],
        'name': 'Channel2',
        'is_public': True
    })
def test_empty_list(clear, channels):
    '''
    Tests for an empty list
    '''
    assert channels['channels'] == []
def test_list(clear, register_info, create, channels):
    '''
    Basic test for functionality of channels/list/v2
    '''
    assert channels['channels'][0]['name'] == "Channel1"
def test_multiple_lists(clear, register_info, create, create2, channels):
    '''
    Tests for multiple lists 
    '''
    assert channels['channels'][0]['name'] == "Channel1"
    assert channels['channels'][1]['name'] == "Channel2"
def test_list_private_channel(clear, register_info, create, channels):
    '''
    Tests if private channels are listed properly
    '''
    assert channels['channels'][0]['name'] == "Channel1"
def test_channel_list_valid_token(clear):
    '''
    Checks if token given is valid
    '''
    assert requests.get(f"{url}/channels/list/v2?token=1").status_code == 400

def test_empty_listall(clear, register_info, all_channels):
    '''
    Tests for an empty list
    '''
    assert all_channels['channels'] == []
def test_listall(clear, register_info, create, all_channels):
    '''
    Basic test for channels/listall/v2
    '''
    assert all_channels['channels'][0]['name'] == "Channel1"
def test_multiple_listall(clear, register_info, create, create2, all_channels):
    '''
    Test multiple lists
    '''
    assert all_channels['channels'][0]['name'] == "Channel1"
    assert all_channels['channels'][1]['name'] == "Channel2"
def test_listall_private_channel(clear, register_info, create, all_channels):
    '''
    Tests if private channels appear in the list
    '''
    assert all_channels['channels'][0]['name'] == "Channel1"
def test_listall_valid_token(clear):
    '''
    Tests for an invalid token
    '''
    assert requests.get(f"{url}/channels/listall/v2?token=1").status_code == 400

def test_create(clear, register_info, create, all_channels):
    '''
    Basic test for functionality of channels/
    '''
    assert all_channels['channels'][0]['name'] == "Channel1"


def test_channels_create_input_error(clear, register_info):
    '''
    Tests for when name of channel is greater than 20 characters
    '''
    assert requests.post(f"{url}/channels/create/v2", json={
        'token': register_info['token'],
        'name': 'Channel1Channel1Channel1Channel1',
        'is_public': True
    }).status_code == 400
def test_channels_create_invalid_token(clear):
    '''
    Tests for invalid token
    '''
    assert requests.post(f"{url}/channels/create/v2", json={
        'token': 1,
        'name': 'Channel1',
        'is_public': True
    }).status_code == 400

