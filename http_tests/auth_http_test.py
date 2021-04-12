'''
Implementation of http tests for auth functions and routes
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
#Clears all data
def clear_data():
    requests.delete(config.url + 'clear/v1')

##Tests for login
#Tests whether a user has logged in successfully (successful implementation)
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

#Tests whether input error is raised for incorrect email
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

#Tests whether input error is raised for invalid email
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

#Tests whether input error is raised for incorrect password
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
#Tests whether input error is raised for invalid email
def test_invalid_email_reg(clear_data):
    assert requests.post(config.url + 'auth/register/v2', json={
        'email': 'robby@gmail',
        'password': 'hello1234',
        'name_first': 'tom',
        'name_last': 'brown',
    }).status_code == InputError.code    

#Tests whether input error is raised for shared email
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

#Tests whether input error is raised for invalid password
def test_invalid_password(clear_data):
    assert requests.post(config.url + 'auth/register/v2', json={
        'email': 'robby@gmail',
        'password': 'hi',
        'name_first': 'rob',
        'name_last': 'brown',
    }).status_code == InputError.code  

#Tests whether input error is raised for invalid firstname
def test_invalid_firstname(clear_data):
    assert requests.post(config.url + 'auth/register/v2', json={
        'email': 'robby@gmail',
        'password': 'hello1234',
        'name_first': '',
        'name_last': 'brown',
    }).status_code == InputError.code 

#Tests whether input error is raised for invalid lastname
def test_invalid_lastname(clear_data):
    assert requests.post(config.url + 'auth/register/v2', json={
        'email': 'robby@gmail',
        'password': 'hello1234',
        'name_first': 'robby',
        'name_last': '',
    }).status_code == InputError.code          

##Test for logout
#Tests whether logout is successful (successful implementation)
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
    payload2 = r.json()
    assert payload2["is_success"] == True

#Tests whether input error is raised for invalid token
def test_invalid_token_logout(clear_data):    
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
    assert requests.post(config.url + 'auth/logout/v1', json = {
        'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzZXNzaW9uX2lkIjo1fQ.L6p3XfadFmkykAtJmcBFkXAvAaxa52Tz3lvitd9ZNNo'
    }).status_code == InputError.code
