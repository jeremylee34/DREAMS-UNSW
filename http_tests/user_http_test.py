'''
Implementation of http tests for user functions and routes
Written by Kanit Srihakorth and Tharushi Gunawardana
'''
import requests
import pytest
from src import config
import src.auth
import src.user
import src.other
import src.data
from src.error import InputError, AccessError

@pytest.fixture
#Clears all data
def clear_data():
    requests.delete(config.url + 'clear/v1')

##Tests for user/profile/v2
#Tests whether input error is raised for invalid u_id
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

#Tests whether access error is raised for invalid token
def test_invalid_token_profile(clear_data):    
    requests.post(config.url + 'auth/register/v2', json={
        'email': 'tom@gmail.com',
        'password': 'hello1234',
        'name_first': 'tom',
        'name_last': 'brown',
    })
    query_string = 'token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzZXNzaW9uX2lkIjo1fQ.L6p3XfadFmkykAtJmcBFkXAvAaxa52Tz3lvitd9ZNNo&u_id=0'           
    assert requests.get(config.url + f"user/profile/v2?{query_string}").status_code == AccessError.code
   

##Tests for user/profile/setname/v2
#Tests whether input error is raised for invalid firstname
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

#Tests whether input error is raised for invalid lastname
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

#Tests whether access error is raised for invalid token
def test_invalid_token_setname(clear_data):    
    requests.post(config.url + 'auth/register/v2', json={
        'email': 'tom@gmail.com',
        'password': 'hello1234',
        'name_first': 'tom',
        'name_last': 'brown',
    })
    assert requests.put(config.url + 'user/profile/setname/v2', json={
        'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzZXNzaW9uX2lkIjo1fQ.L6p3XfadFmkykAtJmcBFkXAvAaxa52Tz3lvitd9ZNNo',
        'name_first': 'john',
        'name_last': 'smith',
    }).status_code == AccessError.code    

##Tests for user/profile/setemail/v2
#Tests whether input error is raised for invalid email
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

#Tests whether input error is raised for already used email
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

#Tests whether access error is raised for invalid token
def test_invalid_token_setemail(clear_data):    
    requests.post(config.url + 'auth/register/v2', json={
        'email': 'tom@gmail.com',
        'password': 'hello1234',
        'name_first': 'tom',
        'name_last': 'brown',
    })
    assert requests.put(config.url + 'user/profile/setemail/v2', json={
        'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzZXNzaW9uX2lkIjo1fQ.L6p3XfadFmkykAtJmcBFkXAvAaxa52Tz3lvitd9ZNNo',
        'email': 'rob@gmail.com'
    }).status_code == AccessError.code       

##Tests for user/profile/sethandle/v1
#Tests whether input error is raised for invalid handle
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

#Tests whether input error is raised for already used email
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

#Tests whether access error is raised for invalid token
def test_invalid_token_sethandle(clear_data):    
    requests.post(config.url + 'auth/register/v2', json={
        'email': 'tom@gmail.com',
        'password': 'hello1234',
        'name_first': 'tom',
        'name_last': 'brown',
    })
    assert requests.put(config.url + 'user/profile/sethandle/v1', json={
        'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzZXNzaW9uX2lkIjo1fQ.L6p3XfadFmkykAtJmcBFkXAvAaxa52Tz3lvitd9ZNNo',
        'handle_str': 'robblue',
    }).status_code == AccessError.code     

##Tests for users/all/v1
#Tests whether all users are returned (successful implementation)
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

#Tests whether access error is raised for invalid token
def test_invalid_token_users_all(clear_data):    
    requests.post(config.url + 'auth/register/v2', json={
        'email': 'tom@gmail.com',
        'password': 'hello1234',
        'name_first': 'tom',
        'name_last': 'brown',
    })
    query_string = 'token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzZXNzaW9uX2lkIjo1fQ.L6p3XfadFmkykAtJmcBFkXAvAaxa52Tz3lvitd9ZNNo'
    assert requests.get(config.url + f"users/all/v1?{query_string}").status_code == AccessError.code   