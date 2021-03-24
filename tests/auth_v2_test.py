import pytest
import json
import requests
from src import config
import src.auth_v2
import src.data
from src.error import InputError, AccessError

def test_system():


#for auth/login/v2
    #Valid email
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
    #InputError - Invalid email

    #with pytest.raises(InputError):
    assert requests.post(config.url + 'auth/register/v2', json = {
            'email': 'tomgmail.com',
            'password': 'hello1234',
            'name_first': 'tom',
            'name_last': 'brown',
    }).status_code == 400

    """   
    #InputError - Email entered doesn't belong to user
    requests.post(config.url + 'auth/register/v2', json = {
        'email': 'tom @gmail.com.com',
        'password': 'hello1234',
        'name_first': 'tom',
        'name_last': 'brown',
    }) 
    assert requests.post(config.url + 'auth/login/v2', json = {
        'email': 'timothy@gmail.com',
        'password': 'hello1234',
    }).status_code == 400 

#for auth/register/v2
    #InputError - Invalid email
    assert requests.post(config.url + 'auth/register/v2', json = {
        'email': 'tom@gmail.com',
        'password': 'hello1234',
        'name_first': 'tom',
        'name_last': 'brown',
    }).status_code == 400  
    #InputError - Email is already used by someone else
    requests.post(config.url + 'auth/register/v2', json = {
        'email': 'tom@gmail.com',
        'password': 'hello1234',
        'name_first': 'tom',
        'name_last': 'brown',
    })
    assert requests.post(config.url + 'auth/register/v2', json = {
        'email': 'tom@gmail.com',
        'password': 'hello1234',
        'name_first': 'tim',
        'name_last': 'blue',
    }).status_code == 400          
    #InputError - password is less than 6 characters
    assert requests.post(config.url + 'auth/register/v2', json = {
        'email': 'tom@gmail.com',
        'password': 'hi',
        'name_first': 'tom',
        'name_last': 'brown',
    }).status_code == 400         
    #InputError - firstname is <1 or >50
    assert requests.post(config.url + 'auth/register/v2', json = {
        'email': 'tom@gmail.com',
        'password': 'hello12345',
        'name_first': '',
        'name_last': 'brown',
    }).status_code == 400   
    #InputError - lastname is <1 or >50
    assert requests.post(config.url + 'auth/register/v2', json = {
        'email': 'tom@gmail.com',
        'password': 'hello12345',
        'name_first': 'tom',
        'name_last': ''
    }).status_code == 400  
    """

#auth/logout/v1
    #tests for successful logout
    """assert requests.post(config.url + 'auth/logout/v1', json = {
        'token': ''
    }).status_code == 200  
     """
