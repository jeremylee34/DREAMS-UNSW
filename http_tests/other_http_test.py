'''
Implementation of http tests for other functions and routes
Written by Kanit Srihakorth and Tharushi Gunawardana
'''
import requests
import pytest
from src import config
import src.auth
import src.other
import src.data
from src.error import InputError, AccessError

@pytest.fixture
def clear_data():
    requests.delete(config.url + 'clear/v1')

##Test for clear
#Tests whether all the users and their information are deleted (successful implementation)
def test_successful_clear(clear_data):    
    requests.post(config.url + 'auth/register/v2', json={
        'email': 'tom@gmail.com',
        'password': 'hello1234',
        'name_first': 'tom',
        'name_last': 'brown',
    })
    requests.post(config.url + 'auth/login/v2', json={
        'email': 'tom@gmail.com',
        'password': 'hello1234',
    })
    requests.post(config.url + 'auth/login/v2', json={
        'email': 'tom@gmail.com',
        'password': 'hello1234',
    }) 
    requests.post(config.url + 'auth/login/v2', json={
        'email': 'tom@gmail.com',
        'password': 'hello1234',
    })
    r = requests.delete(config.url + 'clear/v1')
    payload = r.json()   
    assert payload == {}    