import pytest
import re
import requests

from src.other import clear_v1
from src import config
from src.error import InputError, AccessError
from src.data import data

@pytest.fixture
def clear_data():
    requests.delete(config.url + 'clear/v1')

def test_successful_admin_user_remove(clear_data):
    user1 = requests.post(config.url + 'auth/register/v2', json = {
        'email': 'ska@gmail.com',
        'password': '1234aaaaaa',
        'name_first': 'Tom',
        'name_last': 'Diaaa',
    })

    user2 = requests.post(config.url + 'auth/register/v2', json = {
        'email': 'skada@gmail.com',
        'password': '1234aasaaaa',
        'name_first': 'Brown',
        'name_last': 'Diaam',
    })

    payload1 = user1.json()
    payload2 = user2.json()

    requests.post(config.url + 'admin/userpermission/change/v1', json = {
        'token' : payload1['token'],
        'u_id' : payload2['auth_user_id'],
        'permission_id' : 1,
    })

    requests.delete(config.url + 'admin/user/remove/v1', json = {
        'token': payload1['token'],
        'u_id': payload2['auth_user_id'],
    })

    query_string = f"token={payload1['token']}"
    users = requests.get(config.url + f"users/all/v1?{query_string}")
    payload3 = users.json()
    assert len(payload3) == 1 


def test_invalid_token_successful_admin_user_remove(clear_data):
    requests.post(config.url + 'auth/register/v2', json = {
        'email': 'ska@gmail.com',
        'password': '1234aaaaaa',
        'name_first': 'Tom',
        'name_last': 'diaaa',
    })
    user2 = requests.post(config.url + 'auth/register/v2', json = {
        'email': 'skad@gmail.com',
        'password': '1234aasaaaa',
        'name_first': 'Brown',
        'name_last': 'diaam',
    })
    payload2 = user2.json()
    assert requests.delete(config.url + 'admin/user/remove/v1', json = {
        'token': 'sometoken',
        'u_id': payload2['auth_user_id'],
    }).status_code == AccessError.code
    
def test_invalid_uid_admin_user_remove(clear_data):
    user1 = requests.post(config.url + 'auth/register/v2', json = {
        'email': 'ska@gmail.com',
        'password': '1234aaaaaa',
        'name_first': 'Tom',
        'name_last': 'diaaa',
    })
    requests.post(config.url + 'auth/register/v2', json = {
        'email': 'skad@gmail.com',
        'password': '1234aasaaaa',
        'name_first': 'Brown',
        'name_last': 'diaam',
    })
    payload1 = user1.json()

    assert requests.delete(config.url + 'admin/user/remove/v1', json = {
        'token': payload1['token'],
        'u_id': 99,
    }).status_code == InputError.code

#user permission
def test_successful_admin_userpermission_change_v1(clear_data):
    user1 = requests.post(config.url + 'auth/register/v2', json = {
        'email': 'ska@gmail.com',
        'password': '1234aaaaaa',
        'name_first': 'Tom',
        'name_last': 'diaaa',
    })
    user2 = requests.post(config.url + 'auth/register/v2', json = {
        'email': 'skad@gmail.com',
        'password': '1234aasaaaa',
        'name_first': 'Brown',
        'name_last': 'diaam',
    })
    payload1 = user1.json()
    payload2 = user2.json()
    remove = requests.post(config.url + 'admin/userpermission/change/v1', json = {
        'token' : payload1['token'],
        'u_id' : payload2['auth_user_id'],
        'permission_id' : 1,
    })
    remove == {}

def test_invalid_token_admin_userpermission_change_v1(clear_data):
    requests.post(config.url + 'auth/register/v2', json = {
        'email': 'ska@gmail.com',
        'password': '1234aaaaaa',
        'name_first': 'Tom',
        'name_last': 'diaaa',
    })
    user2 = requests.post(config.url + 'auth/register/v2', json = {
        'email': 'skad@gmail.com',
        'password': '1234aasaaaa',
        'name_first': 'Brown',
        'name_last': 'diaam',
    })
    payload2 = user2.json()
    assert requests.post(config.url + 'admin/userpermission/change/v1', json = {
        'token' : 'asdf',
        'u_id' : payload2['auth_user_id'],
        'permission_id' : 1,
    }).status_code == AccessError.code
    

def test_invalid_u_id_admin_userpermission_change_v1(clear_data):
    user1 = requests.post(config.url + 'auth/register/v2', json = {
        'email': 'ska@gmail.com',
        'password': '1234aaaaaa',
        'name_first': 'Tom',
        'name_last': 'diaaa',
    })
    requests.post(config.url + 'auth/register/v2', json = {
        'email': 'skad@gmail.com',
        'password': '1234aasaaaa',
        'name_first': 'Brown',
        'name_last': 'diaam',
    })
    payload1 = user1.json()
    assert requests.post(config.url + 'admin/userpermission/change/v1', json = {
        'token' : payload1['token'],
        'u_id' : '999',
        'permission_id' : 1,
    }).status_code == InputError.code

def test_invalid_permissin_id_admin_userpermission_change_v1(clear_data):
    user1 = requests.post(config.url + 'auth/register/v2', json = {
        'email': 'ska@gmail.com',
        'password': '1234aaaaaa',
        'name_first': 'Tom',
        'name_last': 'diaaa',
    })
    user2 = requests.post(config.url + 'auth/register/v2', json = {
        'email': 'skad@gmail.com',
        'password': '1234aasaaaa',
        'name_first': 'Brown',
        'name_last': 'diaam',
    })
    payload1 = user1.json()
    payload2 = user2.json()
    assert requests.post(config.url + 'admin/userpermission/change/v1', json = {
        'token' : payload1['token'],
        'u_id' : payload2['auth_user_id'],
        'permission_id' : 999,
    }).status_code == AccessError.code

