'''
Implementation of http tests for user functions and routes
Written by Kanit Srihakorth and Tharushi Gunawardana
'''
import requests
import pytest
from src.config import url
import src.auth
import src.user
import src.other
import src.data
from src.error import InputError, AccessError

@pytest.fixture
#Clears all data
def clear_data():
    requests.delete(f'{url}clear/v1')

##Tests for user/profile/v2
#Tests whether input error is raised for invalid u_id
def test_invalid_uid(clear_data):
    r = requests.post(f'{url}/auth/register/v2', json={
        'email': 'tom@gmail.com',
        'password': 'hello1234',
        'name_first': 'tom',
        'name_last': 'brown',
    })
    payload = r.json()
    assert requests.get(f"{url}/user/profile/v2?token={payload['token']}&u_id=10000").status_code == InputError.code 

#Tests whether input error is raised for invalid token
def test_invalid_token_profile(clear_data):    
    user = requests.post(f'{url}/auth/register/v2', json={
        'email': 'tom@gmail.com',
        'password': 'hello1234',
        'name_first': 'tom',
        'name_last': 'brown',
    }).json()
    
    assert requests.get(f"{url}/user/profile/v2?token=invalid_token&u_id={user['auth_user_id']}").status_code == InputError.code
   

##Tests for user/profile/setname/v2
#Tests whether input error is raised for invalid firstname
def test_invalid_setname_firstname(clear_data):
    r = requests.post(f'{url}/auth/register/v2', json={
        'email': 'tom@gmail.com',
        'password': 'hello1234',
        'name_first': 'tom',
        'name_last': 'brown',
    })
    payload = r.json()
    assert requests.put(f'{url}/user/profile/setname/v2', json={
        'token': payload['token'],
        'name_first': '',
        'name_last': 'smith',
    }).status_code == InputError.code

#Tests whether input error is raised for invalid lastname
def test_invalid_setname_lastname(clear_data):
    r = requests.post(f'{url}/auth/register/v2', json={
        'email': 'tom@gmail.com',
        'password': 'hello1234',
        'name_first': 'tom',
        'name_last': 'brown',
    })
    payload = r.json()
    assert requests.put(f'{url}/user/profile/setname/v2', json={
        'token': payload['token'],
        'name_first': 'john',
        'name_last': '',
    }).status_code == InputError.code

#Tests whether input error is raised for invalid token
def test_invalid_token_setname(clear_data):    
    requests.post(f'{url}/auth/register/v2', json={
        'email': 'tom@gmail.com',
        'password': 'hello1234',
        'name_first': 'tom',
        'name_last': 'brown',
    })
    assert requests.put(f'{url}/user/profile/setname/v2', json={
        'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzZXNzaW9uX2lkIjo1fQ.L6p3XfadFmkykAtJmcBFkXAvAaxa52Tz3lvitd9ZNNo',
        'name_first': 'john',
        'name_last': 'smith',
    }).status_code == InputError.code    

##Tests for user/profile/setemail/v2
#Tests whether input error is raised for invalid email
def test_invalid_setemail(clear_data):
    r = requests.post(f'{url}/auth/register/v2', json={
        'email': 'tom@gmail.com',
        'password': 'hello1234',
        'name_first': 'tom',
        'name_last': 'brown',
    })
    payload = r.json()
    assert requests.put(f'{url}/user/profile/setemail/v2', json={
        'token': payload['token'],
        'email': 'rob.com'
    }).status_code == InputError.code    

#Tests whether input error is raised for already used email
def test_shared_setemail(clear_data):
    r = requests.post(f'{url}/auth/register/v2', json={
        'email': 'tom@gmail.com',
        'password': 'hello1234',
        'name_first': 'tom',
        'name_last': 'brown',
    })
    payload = r.json()
    requests.post(f'{url}/auth/register/v2', json={
        'email': 'rob@gmail.com',
        'password': 'hello1234',
        'name_first': 'rob',
        'name_last': 'blue',
    })    
    assert requests.put(f'{url}/user/profile/setemail/v2', json={
        'token': payload['token'],
        'email': 'rob@gmail.com'
    }).status_code == InputError.code 

#Tests whether input error is raised for invalid token
def test_invalid_token_setemail(clear_data):    
    requests.post(f'{url}/auth/register/v2', json={
        'email': 'tom@gmail.com',
        'password': 'hello1234',
        'name_first': 'tom',
        'name_last': 'brown',
    })
    assert requests.put(f'{url}/user/profile/setemail/v2', json={
        'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzZXNzaW9uX2lkIjo1fQ.L6p3XfadFmkykAtJmcBFkXAvAaxa52Tz3lvitd9ZNNo',
        'email': 'rob@gmail.com'
    }).status_code == InputError.code       

##Tests for user/profile/sethandle/v1
#Tests whether input error is raised for invalid handle
def test_invalid_handle(clear_data):
    r = requests.post(f'{url}/auth/register/v2', json={
        'email': 'tom@gmail.com',
        'password': 'hello1234',
        'name_first': 'tom',
        'name_last': 'brown',
    })
    payload = r.json()
    assert requests.put(f'{url}user/profile/sethandle/v1', json={
        'token': payload['token'],
        'handle_str': 'ao'
    }).status_code == InputError.code  

#Tests whether input error is raised for already used email
def test_shared_handle(clear_data):
    r = requests.post(f'{url}/auth/register/v2', json={
        'email': 'tom@gmail.com',
        'password': 'hello1234',
        'name_first': 'tom',
        'name_last': 'brown',
    })
    payload = r.json()
    requests.post(f'{url}/auth/register/v2', json={
        'email': 'rob@gmail.com',
        'password': 'hello1234',
        'name_first': 'rob',
        'name_last': 'blue',
    })    
    assert requests.put(f'{url}/user/profile/sethandle/v1', json={
        'token': payload['token'],
        'handle_str': 'tombrown'
    }).status_code == InputError.code

#Tests whether input error is raised for invalid token
def test_invalid_token_sethandle(clear_data):    
    requests.post(f'{url}/auth/register/v2', json={
        'email': 'tom@gmail.com',
        'password': 'hello1234',
        'name_first': 'tom',
        'name_last': 'brown',
    })
    assert requests.put(f'{url}/user/profile/sethandle/v1', json={
        'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzZXNzaW9uX2lkIjo1fQ.L6p3XfadFmkykAtJmcBFkXAvAaxa52Tz3lvitd9ZNNo',
        'handle_str': 'robblue',
    }).status_code == InputError.code     

##Tests for users/all/v1
#Tests whether all users are returned (successful implementation)
def test_all_users(clear_data):
    r = requests.post(f'{url}/auth/register/v2', json={
        'email': 'tom@gmail.com',
        'password': 'hello1234',
        'name_first': 'tom',
        'name_last': 'brown',
    })
    payload = r.json()
    requests.post(f'{url}/auth/register/v2', json={
        'email': 'rob@gmail.com',
        'password': 'hello1234',
        'name_first': 'rob',
        'name_last': 'blue',
    }) 
    query_string = f"token={payload['token']}"
    users = requests.get(f'{url}/users/all/v1?{query_string}')
    payload2 = users.json()
    assert len(payload2) == 2  

#Tests whether input error is raised for invalid token
#TODO: MAYBE CHANGING
def test_invalid_token_users_all(clear_data):    
    requests.post(f'{url}/auth/register/v2', json={
        'email': 'tom@gmail.com',
        'password': 'hello1234',
        'name_first': 'tom',
        'name_last': 'brown',
    })
    query_string = 'token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzZXNzaW9uX2lkIjo1fQ.L6p3XfadFmkykAtJmcBFkXAvAaxa52Tz3lvitd9ZNNo'
    assert requests.get(f'{url}/users/all/v1?{query_string}').status_code == InputError.code   

##Tests for user/stats/v1
#checks for how big is the dictionary to test if function is successful
#TODO: MAYBE CHANGING
def test_success_user_stats(clear_data):
    r = requests.post(f'{url}/auth/register/v2', json={
        'email': 'tom@gmail.com',
        'password': 'hello1234',
        'name_first': 'tom',
        'name_last': 'brown',
    })
    payload = r.json()
    assert requests.get(f"{url}user/stats/v1?token={payload['token']}").status_code == 200

##Tests for users/stats/v1
#checks for how big is the dictionary to test if function is successful
def test_success_users_stats(clear_data):
    r = requests.post(f'{url}/auth/register/v2', json={
        'email': 'tom@gmail.com',
        'password': 'hello1234',
        'name_first': 'tom',
        'name_last': 'brown',
    })
    payload = r.json()
    requests.post(f'{url}/auth/register/v2', json={
        'email': 'timmy@gmail.com',
        'password': 'hello1234',
        'name_first': 'tim',
        'name_last': 'blue',
    }) 
    requests.post(f'{url}/auth/register/v2', json={
        'email': 'sam@gmail.com',
        'password': 'hello1234',
        'name_first': 'sam',
        'name_last': 'red',
    })        
    assert requests.get(f"{url}users/stats/v1?token={payload['token']}").status_code == 200

##Tests for /user/profile/uploadphoto/v1
'''
    InputError - img_url returns a HTTP status other than 200 (not successful)
    InputError - x_start, y_start, x_end, y_end are not within the dimensions of the image at the url
    InputError - image uploaded is not a JPEG
'''