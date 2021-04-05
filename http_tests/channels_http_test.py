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
def test_empty_list(clear):
    '''
    Tests for an empty list
    '''
    register_info = requests.post(f"{url}/auth/register/v2", json={
        'email': 'gordon@gmail.com',
        'password': '12345678',
        'name_first': 'Gordon',
        'name_last': 'Liang'
    })
    channels = requests.get(f"{url}/channels/list/v2", json={
        'token': register_info['token']
    })
    channels_json = channels['channels'].json()
    assert channels_json == []
def test_list(clear):
    '''
    Basic test for functionality of channels/list/v2
    '''
    register_info = requests.post(f"{url}/auth/register/v2", json={
        'email': 'gordon@gmail.com',
        'password': '12345678',
        'name_first': 'Gordon',
        'name_last': 'Liang'
    })
    requests.post(f"{url}/channels/create/v2", json={
        'token': register_info['token'],
        'name': 'Channel1',
        'is_public': True
    })
    channels = requests.get(f"{url}/channels/list/v2", json={
        'token': register_info['token']
    })
    channels_json = channels['channels'].json()
    assert 'Channel1' in channels_json.values()
def test_multiple_lists(clear):
    '''
    Tests for multiple lists 
    '''
    register_info = requests.post(f"{url}/auth/register/v2", json={
        'email': 'gordon@gmail.com',
        'password': '12345678',
        'name_first': 'Gordon',
        'name_last': 'Liang'
    })
    requests.post(f"{url}/channels/create/v2", json={
        'token': register_info['token'],
        'name': 'Channel1',
        'is_public': True
    })
    requests.post(f"{url}/channels/create/v2", json={
        'token': register_info['token'],
        'name': 'Channel2',
        'is_public': True
    })
    channels = requests.get(f"{url}/channels/list/v2", json={
        'token': register_info['token']
    })
    channels_json = channels['channels'].json()
    assert 'Channel1' in channels_json.values()
    assert 'Channel2' in channels_json.values()
def test_list_private_channel(clear):
    '''
    Tests if private channels are listed properly
    '''
    register_info = requests.post(f"{url}/auth/register/v2", json={
        'email': 'gordon@gmail.com',
        'password': '12345678',
        'name_first': 'Gordon',
        'name_last': 'Liang'
    })
    requests.post(f"{url}/channels/create/v2", json={
        'token': register_info['token'],
        'name': 'Channel1',
        'is_public': False
    })
    channels = requests.get(f"{url}/channels/list/v2", json={
        'token': register_info['token']
    })
    channels_json = channels['channels'].json()
    assert 'Channel1' in channels_json.values()
def test_channel_list_valid_token(clear):
    '''
    Checks if token given is valid
    '''
    register_info = {
        'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzZXNzaW9uX2lkIjo0fQ.UWh4yaDf6lPdmJroKBXfBZURXskoLULjM7Es_xZSK6U'
    }
    assert requests.get(f"{url}/channels/list/v2", json={
        'token': register_info['token']
    }).status_code == 403

def test_empty_listall(clear):
    '''
    Tests for an empty list
    '''
    register_info = requests.post(f"{url}/auth/register/v2", json={
        'email': 'gordon@gmail.com',
        'password': '12345678',
        'name_first': 'Gordon',
        'name_last': 'Liang'
    })
    channels = requests.get(f"{url}/channels/listall/v2", json={
        'token': register_info['token']
    })
    channels_json = channels['channels'].json()
    assert channels_json == []
def test_listall():
    '''
    Basic test for channels/listall/v2
    '''
    register_info = requests.post(f"{url}/auth/register/v2", json={
        'email': 'gordon@gmail.com',
        'password': '12345678',
        'name_first': 'Gordon',
        'name_last': 'Liang'
    })
    requests.post(f"{url}/channels/create/v2", json={
        'token': register_info['token'],
        'name': 'Channel1',
        'is_public': True
    })
    channels = requests.get(f"{url}/channels/listall/v2", json={
        'token': register_info['token']
    })
    channels_json = channels['channels'].json()
    assert 'Channel1' in channels_json.values()
def test_multiple_listall(clear):
    '''
    Test multiple lists
    '''
    register_info = requests.post(f"{url}/auth/register/v2", json={
        'email': 'gordon@gmail.com',
        'password': '12345678',
        'name_first': 'Gordon',
        'name_last': 'Liang'
    })
    requests.post(f"{url}/channels/create/v2", json={
        'token': register_info['token'],
        'name': 'Channel1',
        'is_public': True
    })
    requests.post(f"{url}/channels/create/v2", json={
        'token': register_info['token'],
        'name': 'Channel2',
        'is_public': True
    })
    channels = requests.get(f"{url}/channels/listall/v2", json={
        'token': register_info['token']
    })
    channels_json = channels['channels'].json()
    assert 'Channel1' in channels_json.values()
    assert 'Channel2' in channels_json.values()
def test_listall_private_channel(clear):
    '''
    Tests if private channels appear in the list
    '''
    register_info = requests.post(f"{url}/auth/register/v2", json={
        'email': 'gordon@gmail.com',
        'password': '12345678',
        'name_first': 'Gordon',
        'name_last': 'Liang'
    })
    requests.post(f"{url}/channels/create/v2", json={
        'token': register_info['token'],
        'name': 'Channel1',
        'is_public': False
    })
    channels = requests.get(f"{url}/channels/listall/v2", json={
        'token': register_info['token']
    })
    channels_json = channels['channels'].json()
    assert 'Channel1' in channels_json.values()
def test_listall_valid_token(clear):
    '''
    Tests for an invalid token
    '''
    register_info = {
        'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzZXNzaW9uX2lkIjo0fQ.UWh4yaDf6lPdmJroKBXfBZURXskoLULjM7Es_xZSK6U'
    }
    assert requests.get(f"{url}/channels/listall/v2", json={
        'token': register_info['token']
    }).status_code == 403

def test_create(clear):
    '''
    Basic test for functionality of channels/
    '''
    register_info = requests.post(f"{url}/auth/register/v2", json={
        'email': 'gordon@gmail.com',
        'password': '12345678',
        'name_first': 'Gordon',
        'name_last': 'Liang'
    })
    requests.post(f"{url}/channels/create/v2", json={
        'token': register_info['token'],
        'name': 'Channel1',
        'is_public': True
    })
    channels = requests.get(f"{url}/channels/listall/v2", json={
        'token': register_info['token']
    })
    channels_json = channels['channels'].json()
    assert 'Channel1' in channels_json.values()
def test_channels_create_input_error(clear):
    '''
    Tests for when name of channel is greater than 20 characters
    '''
    register_info = requests.post(f"{url}/auth/register/v2", json={
        'email': 'gordon@gmail.com',
        'password': '12345678',
        'name_first': 'Gordon',
        'name_last': 'Liang'
    })
    assert requests.post(f"{url}/channels/create/v2", json={
        'token': register_info['token'],
        'name': 'Channel1Channel1Channel1Channel1',
        'is_public': True
    }).status_code == 400
def test_channels_create_invalid_token(clear):
    '''
    Tests for invalid token
    '''
    register_info = {
        'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzZXNzaW9uX2lkIjo0fQ.UWh4yaDf6lPdmJroKBXfBZURXskoLULjM7Es_xZSK6U'
    }
    assert requests.post(f"{url}/channels/create/v2", json={
        'token': register_info['token'],
        'name': 'Channel1',
        'is_public': True
    }).status_code == 403
