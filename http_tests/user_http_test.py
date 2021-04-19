'''
Implementation of http tests for user functions and routes
Written by Kanit Srihakorth and Tharushi Gunawardana
'''
import requests
import pytest
from src.config import url
import src.auth
import src.channels
import src.dm
import src.message
import src.user
import src.other
from src.error import InputError, AccessError

<<<<<<< HEAD
IMG_URL = "https://cdn.mos.cms.futurecdn.net/YB6aQqKZBVjtt3PuDSkJKe.jpg"
FAKE_URL = "https://cdn.mos.cms.futurecdn.net/YB6aQqKZBVjtt3PuDSkJKe.png"
FAKE_URL2 = "https://cdn.mos.cms/YB6aQqKZBVjtt3PuDSkJKe.jpg"
=======
>>>>>>> master

@pytest.fixture
#Clears all data
def clear_data():
    requests.delete(f'{url}/clear/v1')

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
    assert requests.get(f"{url}/user/profile/v2?token={payload['token']}&u_id=1000").status_code == InputError.code

#Tests whether access error is raised for invalid token
def test_invalid_token_profile(clear_data):    
    requests.post(f'{url}/auth/register/v2', json={
        'email': 'tom@gmail.com',
        'password': 'hello1234',
        'name_first': 'tom',
        'name_last': 'brown',
    })
    
    assert requests.get(f'{url}/user/profile/v2?token=invalid_token&u_id=0').status_code == InputError.code
   

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

#Tests whether access error is raised for invalid token
def test_invalid_token_setname(clear_data):    
    requests.post(f'{url}/auth/register/v2', json={
        'email': 'tom@gmail.com',
        'password': 'hello1234',
        'name_first': 'tom',
        'name_last': 'brown',
    })
    assert requests.put(f'{url}/user/profile/setname/v2', json={
        'token': 'invalid_token',
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

#Tests whether access error is raised for invalid token
def test_invalid_token_setemail(clear_data):    
    requests.post(f'{url}/auth/register/v2', json={
        'email': 'tom@gmail.com',
        'password': 'hello1234',
        'name_first': 'tom',
        'name_last': 'brown',
    })
    assert requests.put(f'{url}/user/profile/setemail/v2', json={
        'token': 'invalid_token',
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

#Tests whether access error is raised for invalid token
def test_invalid_token_sethandle(clear_data):    
    requests.post(f'{url}/auth/register/v2', json={
        'email': 'tom@gmail.com',
        'password': 'hello1234',
        'name_first': 'tom',
        'name_last': 'brown',
    })
    assert requests.put(f'{url}/user/profile/sethandle/v1', json={
        'token': 'invalid_token',
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
    assert len(payload2['users']) == 2  

#Tests whether access error is raised for invalid token
def test_invalid_token_users_all(clear_data):    
    requests.post(f'{url}/auth/register/v2', json={
        'email': 'tom@gmail.com',
        'password': 'hello1234',
        'name_first': 'tom',
        'name_last': 'brown',
    })
<<<<<<< HEAD
    query_string = 'token=invalid_token'
    assert requests.get(f'{url}/users/all/v1?{query_string}').status_code == InputError.code    

##Tests for user/stats/v1
#checks for how big is the dictionary to test if function is successful
def test_success_user_stats(clear_data):
    r = requests.post(f'{url}/auth/register/v2', json={
        'email': 'tom@gmail.com',
        'password': 'hello1234',
        'name_first': 'tom',
        'name_last': 'brown',
    }).json()
    requests.post(f'{url}/auth/register/v2', json={
        'email': 'tim@gmail.com',
        'password': 'hello1234',
        'name_first': 'tim',
        'name_last': 'brown',
    })
    c = requests.post(f'{url}/channels/create/v2', json={
        'token': r['token'],
        'name': 'channel1',
        'is_public': True,
    }).json()
    requests.post(f'{url}/dm/create/v1', json={
        'token': r['token'],
        'u_ids': [1],
    })
    requests.post(f'{url}/message/send/v2', json={
        'token': r['token'],
        'channel_id': c['channel_id'],
        'message': 'Hello'
    })    
    assert requests.get(f"{url}user/stats/v1?token={r['token']}").status_code == 200

##Tests for users/stats/v1
#checks for how big is the dictionary to test if function is successful
def test_success_users_stats(clear_data):
    r = requests.post(f'{url}/auth/register/v2', json={
        'email': 'tom@gmail.com',
        'password': 'hello1234',
        'name_first': 'tom',
        'name_last': 'brown',
    }).json()
    requests.post(f'{url}/auth/register/v2', json={
        'email': 'tim@gmail.com',
        'password': 'hello1234',
        'name_first': 'tim',
        'name_last': 'brown',
    }).json()
    c = requests.post(f'{url}/channels/create/v2', json={
        'token': r['token'],
        'name': 'channel1',
        'is_public': True,
    }).json()
    requests.post(f'{url}/dm/create/v1', json={
        'token': r['token'],
        'u_ids': [1],
    })
    requests.post(f'{url}/message/send/v2', json={
        'token': r['token'],
        'channel_id': 0,
        'message': 'Hello'
    })         
    assert requests.get(f"{url}users/stats/v1?token={r['token']}").status_code == 200

##Tests for /user/profile/uploadphoto/v1
'''
    InputError - img_url returns a HTTP status other than 200 (not successful)
    InputError - x_start, y_start, x_end, y_end are not within the dimensions of the image at the url
    InputError - image uploaded is not a JPEG
'''
def test_invalid_token_uploadphoto(clear_data):
    requests.post(f'{url}/auth/register/v2', json={
        'email': 'timmy@gmail.com',
        'password': 'hello1234',
        'name_first': 'tim',
        'name_last': 'blue',
    })  
    assert requests.post(f'{url}/user/profile/uploadphoto/v1', json={
        'token': 'invalid_token',
        'img_url': IMG_URL,
        'x_start': 50,
        'y_start': 50,
        'x_end': 200,
        'y_end': 200,
    }).status_code == InputError.code

def test_invalid_x_dim(clear_data):
    r = requests.post(f'{url}/auth/register/v2', json={
        'email': 'timmy@gmail.com',
        'password': 'hello1234',
        'name_first': 'tim',
        'name_last': 'blue',
    }).json() 
    assert requests.post(f'{url}/user/profile/uploadphoto/v1', json={
        'token': r['token'],
        'img_url': IMG_URL,
        'x_start': 1800,
        'y_start': 50,
        'x_end': 200,
        'y_end': 50,
    }).status_code == InputError.code   

def test_invalid_y_dim(clear_data):
    r = requests.post(f'{url}/auth/register/v2', json={
        'email': 'timmy@gmail.com',
        'password': 'hello1234',
        'name_first': 'tim',
        'name_last': 'blue',
    }).json() 
    assert requests.post(f'{url}/user/profile/uploadphoto/v1', json={
        'token': r['token'],
        'img_url': IMG_URL,
        'x_start': 150,
        'y_start': 20000,
        'x_end': 200,
        'y_end': 200,
    }).status_code == InputError.code 

def test_invalid_img_url(clear_data):
    r = requests.post(f'{url}/auth/register/v2', json={
        'email': 'timmy@gmail.com',
        'password': 'hello1234',
        'name_first': 'tim',
        'name_last': 'blue',
    }).json() 
    assert requests.post(f'{url}/user/profile/uploadphoto/v1', json={
        'token': r['token'],
        'img_url': FAKE_URL,
        'x_start': 50,
        'y_start': 50,
        'x_end': 200,
        'y_end': 200,
    }).status_code == InputError.code

def test_valid_img_url(clear_data):
    r = requests.post(f'{url}/auth/register/v2', json={
        'email': 'timmy@gmail.com',
        'password': 'hello1234',
        'name_first': 'tim',
        'name_last': 'blue',
    }).json() 
    assert requests.post(f'{url}/user/profile/uploadphoto/v1', json={
        'token': r['token'],
        'img_url': IMG_URL,
        'x_start': 50,
        'y_start': 50,
        'x_end': 200,
        'y_end': 200,
    }).status_code == 200

def test_invalid_img_url2(clear_data):
    r = requests.post(f'{url}/auth/register/v2', json={
        'email': 'timmy@gmail.com',
        'password': 'hello1234',
        'name_first': 'tim',
        'name_last': 'blue',
    }).json() 
    assert requests.post(f'{url}/user/profile/uploadphoto/v1', json={
        'token': r['token'],
        'img_url': FAKE_URL,
        'x_start': 50,
        'y_start': 50,
        'x_end': 200,
        'y_end': 200,
    }).status_code == InputError.code   
=======
    query_string = 'token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzZXNzaW9uX2lkIjo1fQ.L6p3XfadFmkykAtJmcBFkXAvAaxa52Tz3lvitd9ZNNo'
    assert requests.get(f'{url}/users/all/v1?{query_string}').status_code == InputError.code       
>>>>>>> master
