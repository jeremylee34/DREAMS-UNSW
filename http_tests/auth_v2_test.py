import pytest
import requests
from src import config
import src.auth_v2
import src.data
from src.error import InputError, AccessError

@pytest.fixture
def clear_data():
    requests.delete(config.url + 'clear/v1')

##Tests for login
def test_successful_login(clear_data):
    r = requests.post(config.url + 'auth/register/v2', json={
        'email': 'tom@gmail.com',
        'password': 'hello1234',
        'name_first': 'tom',
        'name_last': 'brown',
    }) 
    payload = r.json()
    r2 = requests.post(config.url + 'auth/login/v2', json={
            'email': 'tom@gmail.com',
            'password': 'hello1234',
        })
    payload2 = r2.json()
    assert payload['auth_user_id'] == payload2['auth_user_id']  

def test_incorrect_email(clear_data):
    requests.post(config.url + 'auth/register/v2', json={
        'email': 'tom@gmail.com',
        'password': 'hello1234',
        'name_first': 'tom',
        'name_last': 'brown',
    }) 
    assert requests.post(config.url + 'auth/login/v2', json={
            'email': 'tommy@gmail.com',
            'password': 'hello1234',
    }).status_code == InputError.code 

def test_invalid_email(clear_data):
    requests.post(config.url + 'auth/register/v2', json={
        'email': 'tom@gmail.com',
        'password': 'hello1234',
        'name_first': 'tom',
        'name_last': 'brown',
    }) 
    assert requests.post(config.url + 'auth/login/v2', json={
            'email': 'tomm.com',
            'password': 'hello1234',
    }) .status_code == InputError.code      

def test_incorrect_password(clear_data):
    requests.post(config.url + 'auth/register/v2', json={
        'email': 'tom@gmail.com',
        'password': 'hello1234',
        'name_first': 'tom',
        'name_last': 'brown',
    }) 
    assert requests.post(config.url + 'auth/login/v2', json={
        'email': 'tom@gmail.com',
        'password': 'hlo1234',
    }).status_code == InputError.code      


##Tests for register
def test_invalid_email_reg(clear_data):
    assert requests.post(config.url + 'auth/register/v2', json={
        'email': 'robby@gmail',
        'password': 'hello1234',
        'name_first': 'tom',
        'name_last': 'brown',
    }).status_code == InputError.code    

def test_shared_email(clear_data):
    requests.post(config.url + 'auth/register/v2', json={
        'email': 'tom@gmail.com',
        'password': 'hello1234',
        'name_first': 'tom',
        'name_last': 'brown',
    })
    assert requests.post(config.url + 'auth/register/v2', json={
        'email': 'tom@gmail.com',
        'password': 'tommy123',
        'name_first': 'tommy',
        'name_last': 'blue',
    }).status_code == InputError.code
def test_invalid_password(clear_data):
    assert requests.post(config.url + 'auth/register/v2', json={
        'email': 'robby@gmail',
        'password': 'hi',
        'name_first': 'rob',
        'name_last': 'brown',
    }).status_code == InputError.code  
def test_invalid_firstname(clear_data):
    assert requests.post(config.url + 'auth/register/v2', json={
        'email': 'robby@gmail',
        'password': 'hello1234',
        'name_first': '',
        'name_last': 'brown',
    }).status_code == InputError.code 
def test_invalid_lastname(clear_data):
    assert requests.post(config.url + 'auth/register/v2', json={
        'email': 'robby@gmail',
        'password': 'hello1234',
        'name_first': 'robby',
        'name_last': '',
    }).status_code == InputError.code          

##Test for logout
def test_successful_logout(clear_data):    
    x = requests.post(config.url + 'auth/register/v2', json={
        'email': 'tom@gmail.com',
        'password': 'hello1234',
        'name_first': 'tom',
        'name_last': 'brown',
    })
    payload = x.json() 
    requests.post(config.url + 'auth/login/v2', json={
        'email': 'tom@gmail.com',
        'password': 'hello1234',
    })              
    r = requests.post(config.url + 'auth/logout/v1', json = {
        'token': payload['token']
    })
    payload = r.json()
    assert payload["is_success"] == True