import pytest
import re
import requests

from src.other import clear_v1
# from src import config
from src.config import url
from src.error import InputError, AccessError
from src.data import data

@pytest.fixture
def clear_data():
    '''
    Clears data in data file
    '''
    requests.delete(f'{url}/clear/v1')

def test_successful_admin_user_remove(clear_data):
    '''
    Basic test for functionality of admin_user_remove function
    '''
    user1 = requests.post(f'{url}/auth/register/v2', json = {
        'email': 'ska@gmail.com',
        'password': '1234aaaaaa',
        'name_first': 'Tom',
        'name_last': 'Diaaa',
    })

    user2 = requests.post(f'{url}/auth/register/v2', json = {
        'email': 'skada@gmail.com',
        'password': '1234aasaaaa',
        'name_first': 'Brown',
        'name_last': 'Diaam',
    })

    payload1 = user1.json()
    payload2 = user2.json()

    requests.post(f'{url}/admin/userpermission/change/v1', json = {
        'token' : payload1['token'],
        'u_id' : payload2['auth_user_id'],
        'permission_id' : 1,
    })

    requests.delete(f'{url}/admin/user/remove/v1', json = {
        'token': payload1['token'],
        'u_id': payload2['auth_user_id'],
    })

    query_string = f"token={payload1['token']}"
    users = requests.get(f"{url}/users/all/v1?{query_string}")
    payload3 = users.json()
    assert len(payload3) == 1 


def test_invalid_token_successful_admin_user_remove(clear_data):
    '''
    Test if admin_user_remove function token is invalid
    '''
    requests.post(f'{url}/auth/register/v2', json = {
        'email': 'ska@gmail.com',
        'password': '1234aaaaaa',
        'name_first': 'Tom',
        'name_last': 'diaaa',
    })
    user2 = requests.post(f'{url}/auth/register/v2', json = {
        'email': 'skad@gmail.com',
        'password': '1234aasaaaa',
        'name_first': 'Brown',
        'name_last': 'diaam',
    })
    payload2 = user2.json()
    assert requests.delete(f'{url}/admin/user/remove/v1', json = {
        'token': 'sometoken',
        'u_id': payload2['auth_user_id'],
    }).status_code == AccessError.code
    
def test_invalid_uid_admin_user_remove(clear_data):
    '''
    Test if admin_user_remove function u_id is invalid
    '''
    user1 = requests.post(f'{url}/auth/register/v2', json = {
        'email': 'ska@gmail.com',
        'password': '1234aaaaaa',
        'name_first': 'Tom',
        'name_last': 'diaaa',
    })
    requests.post(f'{url}/auth/register/v2', json = {
        'email': 'skad@gmail.com',
        'password': '1234aasaaaa',
        'name_first': 'Brown',
        'name_last': 'diaam',
    })
    payload1 = user1.json()

    assert requests.delete(f'{url}/admin/user/remove/v1', json = {
        'token': payload1['token'],
        'u_id': 99,
    }).status_code == InputError.code

def test_successful_admin_userpermission_change_v1(clear_data):
    '''
    Basic test for admin_userpermission_change functionality
    '''
    user1 = requests.post(f'{url}/auth/register/v2', json = {
        'email': 'ska@gmail.com',
        'password': '1234aaaaaa',
        'name_first': 'Tom',
        'name_last': 'diaaa',
    })
    user2 = requests.post(f'{url}/auth/register/v2', json = {
        'email': 'skad@gmail.com',
        'password': '1234aasaaaa',
        'name_first': 'Brown',
        'name_last': 'diaam',
    })
    payload1 = user1.json()
    payload2 = user2.json()
    assert requests.post(f'{url}/admin/userpermission/change/v1', json = {
        'token' : payload1['token'],
        'u_id' : payload2['auth_user_id'],
        'permission_id' : 1,
    }).status_code == 200

def test_invalid_token_admin_userpermission_change_v1(clear_data):
    '''
    Test if admin_userpermission_change function token is invalid
    '''
    requests.post(f'{url}/auth/register/v2', json = {
        'email': 'ska@gmail.com',
        'password': '1234aaaaaa',
        'name_first': 'Tom',
        'name_last': 'diaaa',
    })
    user2 = requests.post(f'{url}/auth/register/v2', json = {
        'email': 'skad@gmail.com',
        'password': '1234aasaaaa',
        'name_first': 'Brown',
        'name_last': 'diaam',
    })
    payload2 = user2.json()
    assert requests.post(f'{url}/admin/userpermission/change/v1', json = {
        'token' : 'asdf',
        'u_id' : payload2['auth_user_id'],
        'permission_id' : 1,
    }).status_code == AccessError.code
    

def test_invalid_u_id_admin_userpermission_change_v1(clear_data):
    '''
    Test if admin_userpermission_change function u_id is invalid
    '''
    user1 = requests.post(f'{url}/auth/register/v2', json = {
        'email': 'ska@gmail.com',
        'password': '1234aaaaaa',
        'name_first': 'Tom',
        'name_last': 'diaaa',
    })
    requests.post(f'{url}/auth/register/v2', json = {
        'email': 'skad@gmail.com',
        'password': '1234aasaaaa',
        'name_first': 'Brown',
        'name_last': 'diaam',
    })
    payload1 = user1.json()
    assert requests.post(f'{url}/admin/userpermission/change/v1', json = {
        'token' : payload1['token'],
        'u_id' : '999',
        'permission_id' : 1,
    }).status_code == InputError.code

def test_invalid_permissin_id_admin_userpermission_change_v1(clear_data):
    '''
    Test if admin_userpermission_change function permissin_id is invalid
    '''
    user1 = requests.post(f'{url}/auth/register/v2', json = {
        'email': 'ska@gmail.com',
        'password': '1234aaaaaa',
        'name_first': 'Tom',
        'name_last': 'diaaa',
    })
    user2 = requests.post(f'{url}/auth/register/v2', json = {
        'email': 'skad@gmail.com',
        'password': '1234aasaaaa',
        'name_first': 'Brown',
        'name_last': 'diaam',
    })
    payload1 = user1.json()
    payload2 = user2.json()
    assert requests.post(f'{url}/admin/userpermission/change/v1', json = {
        'token' : payload1['token'],
        'u_id' : payload2['auth_user_id'],
        'permission_id' : 999,
    }).status_code == AccessError.code
