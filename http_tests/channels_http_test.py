import pytest
import requests
from src.config import port
from src.config import url
from src.other import clear_v1
from src.error import AccessError
from src.error import InputError

@pytest.fixture
def clear():
    clear_v1()
def test_empty_list(clear):
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
    register_info = {
        'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzZXNzaW9uX2lkIjo0fQ.UWh4yaDf6lPdmJroKBXfBZURXskoLULjM7Es_xZSK6U'
    }
    with pytest.raises(AccessError):
        assert requests.get(f"{url}/channels/list/v2", json={
            'token': register_info['token']
        })

def test_empty_listall(clear):
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
    register_info = {
        'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzZXNzaW9uX2lkIjo0fQ.UWh4yaDf6lPdmJroKBXfBZURXskoLULjM7Es_xZSK6U'
    }
    with pytest.raises(AccessError):
        assert requests.get(f"{url}/channels/listall/v2", json={
            'token': register_info['token']
        })

def test_create(clear):
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
    register_info = requests.post(f"{url}/auth/register/v2", json={
        'email': 'gordon@gmail.com',
        'password': '12345678',
        'name_first': 'Gordon',
        'name_last': 'Liang'
    })
    with pytest.raises(InputError):
        assert requests.post(f"{url}/channels/create/v2", json={
            'token': register_info['token'],
            'name': 'Channel1Channel1Channel1Channel1',
            'is_public': True
        })
def test_channels_create_invalid_token(clear):
    register_info = {
        'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzZXNzaW9uX2lkIjo0fQ.UWh4yaDf6lPdmJroKBXfBZURXskoLULjM7Es_xZSK6U'
    }
    with pytest.raises(AccessError):
        assert requests.post(f"{url}/channels/create/v2", json={
            'token': register_info['token'],
            'name': 'Channel1',
            'is_public': True
        })
