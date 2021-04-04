import requests
import pytest
from src import config
import src.auth
import src.user
import src.other
import src.data
from src.error import InputError, AccessError

@pytest.fixture
def clear_data():
    requests.delete(config.url + 'clear/v1')

##Tests for user/profile/v2
def test_invalid_uid(clear_data):
    r = requests.post(config.url + 'auth/register/v2', json={
        'email': 'tom@gmail.com',
        'password': 'hello1234',
        'name_first': 'tom',
        'name_last': 'brown',
    })
    payload = r.json()
    query_string = f"token={payload['token']}" + '&u_id=2'
    assert requests.get(config.url + f"user/profile/v2?{query_string}").status_code == InputError.code 

##Tests for user/profile/setname/v2
def test_invalid_setname_firstname(clear_data):
    r = requests.post(config.url + 'auth/register/v2', json={
        'email': 'tom@gmail.com',
        'password': 'hello1234',
        'name_first': 'tom',
        'name_last': 'brown',
    })
    payload = r.json()
    assert requests.put(config.url + 'user/profile/setname/v2', json={
        'token': payload['token'],
        'name_first': '',
        'name_last': 'smith',
    }).status_code == InputError.code

def test_invalid_setname_lastname(clear_data):
    r = requests.post(config.url + 'auth/register/v2', json={
        'email': 'tom@gmail.com',
        'password': 'hello1234',
        'name_first': 'tom',
        'name_last': 'brown',
    })
    payload = r.json()
    assert requests.put(config.url + 'user/profile/setname/v2', json={
        'token': payload['token'],
        'name_first': 'john',
        'name_last': '',
    }).status_code == InputError.code

##Tests for user/profile/setemail/v2
def test_invalid_setemail(clear_data):
    r = requests.post(config.url + 'auth/register/v2', json={
        'email': 'tom@gmail.com',
        'password': 'hello1234',
        'name_first': 'tom',
        'name_last': 'brown',
    })
    payload = r.json()
    assert requests.put(config.url + 'user/profile/setemail/v2', json={
        'token': payload['token'],
        'email': 'rob.com'
    }).status_code == InputError.code    

def test_shared_setemail(clear_data):
    r = requests.post(config.url + 'auth/register/v2', json={
        'email': 'tom@gmail.com',
        'password': 'hello1234',
        'name_first': 'tom',
        'name_last': 'brown',
    })
    payload = r.json()
    requests.post(config.url + 'auth/register/v2', json={
        'email': 'rob@gmail.com',
        'password': 'hello1234',
        'name_first': 'rob',
        'name_last': 'blue',
    })    
    assert requests.put(config.url + 'user/profile/setemail/v2', json={
        'token': payload['token'],
        'email': 'rob@gmail.com'
    }).status_code == InputError.code   

##Tests for user/profile/sethandle/v1
def test_invalid_handle(clear_data):
    r = requests.post(config.url + 'auth/register/v2', json={
        'email': 'tom@gmail.com',
        'password': 'hello1234',
        'name_first': 'tom',
        'name_last': 'brown',
    })
    payload = r.json()
    assert requests.put(config.url + 'user/profile/sethandle/v1', json={
        'token': payload['token'],
        'handle_str': 'ao'
    }).status_code == InputError.code  

def test_shared_handle(clear_data):
    r = requests.post(config.url + 'auth/register/v2', json={
        'email': 'tom@gmail.com',
        'password': 'hello1234',
        'name_first': 'tom',
        'name_last': 'brown',
    })
    payload = r.json()
    requests.post(config.url + 'auth/register/v2', json={
        'email': 'rob@gmail.com',
        'password': 'hello1234',
        'name_first': 'rob',
        'name_last': 'blue',
    })    
    assert requests.put(config.url + 'user/profile/sethandle/v1', json={
        'token': payload['token'],
        'handle_str': 'tombrown'
    }).status_code == InputError.code

##Tests for users/all/v1
def test_all_users(clear_data):
    r = requests.post(config.url + 'auth/register/v2', json={
        'email': 'tom@gmail.com',
        'password': 'hello1234',
        'name_first': 'tom',
        'name_last': 'brown',
    })
    payload = r.json()
    requests.post(config.url + 'auth/register/v2', json={
        'email': 'rob@gmail.com',
        'password': 'hello1234',
        'name_first': 'rob',
        'name_last': 'blue',
    }) 
    query_string = f"token={payload['token']}"
    users = requests.get(config.url + f"users/all/v1?{query_string}")
    payload2 = users.json()
    assert len(payload2) == 2  