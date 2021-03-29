import pytest
import requests

@pytest.fixture
def url():
    port = 8080
    new_url = f"http://localhost:{port}/"
    return new_url
def test_empty_list(url):
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
def test_list(url):
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
    assert 'Channel1' in channels_json

def test_multiple_lists(url):
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
    assert 'Channel1' in channels_json
    assert 'Channel2' in channels_json
def test_empty_listall(url):
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
def test_listall(url):
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
    assert 'Channel1' in channels_json

def test_multiple_listall(url):
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
    assert 'Channel1' in channels_json
    assert 'Channel2' in channels_json

def test_create(url):
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
    assert 'Channel1' in channels_json
