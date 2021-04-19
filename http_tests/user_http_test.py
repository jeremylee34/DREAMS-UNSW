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

IMG_URL = "https://cdn.mos.cms.futurecdn.net/YB6aQqKZBVjtt3PuDSkJKe.jpg"
FAKE_URL = "https://cdn.mos.cms.futurecdn.net/YB6aQqKZBVjtt3PuDSkJKe.png"
FAKE_URL2 = "https://cdn.mos.cms/YB6aQqKZBVjtt3PuDSkJKe.jpg"

@pytest.fixture
def clear_data():
    '''
    Clears all data
    '''    
    requests.delete(f'{url}/clear/v1')

@pytest.fixture
def user():
    '''
    Calls auth_register_v1 to register user
    '''    
    user = requests.post(f'{url}/auth/register/v2', json={
        'email': 'tom@gmail.com',
        'password': 'hello1234',
        'name_first': 'tom',
        'name_last': 'brown',
    }).json()
    return user   

@pytest.fixture
def user2():
    '''
    Calls auth_register_v1 to register second user
    '''    
    user2 = requests.post(f'{url}/auth/register/v2', json={
        'email': 'tim@gmail.com',
        'password': 'hello1234',
        'name_first': 'tim',
        'name_last': 'blue',
    }).json()
    return user2     

##Tests for user/profile/v2
def test_invalid_uid(clear_data, user):
    '''
    Tests whether input error is raised for invalid u_id
    '''     
    assert requests.get(f"{url}/user/profile/v2?token={user['token']}&u_id=1000").status_code == InputError.code

def test_invalid_token_profile(clear_data, user):    
    '''
    Tests whether input error is raised for invalid token
    '''       
    assert requests.get(f'{url}/user/profile/v2?token=invalid_token&u_id=0').status_code == InputError.code
   
##Tests for user/profile/setname/v2
def test_invalid_setname_firstname(clear_data, user):
    '''
    Tests whether input error is raised for invalid firstname
    '''     
    assert requests.put(f'{url}/user/profile/setname/v2', json={
        'token': user['token'],
        'name_first': '',
        'name_last': 'smith',
    }).status_code == InputError.code

def test_invalid_setname_lastname(clear_data, user):
    '''
    Tests whether input error is raised for invalid lastname
    '''       
    assert requests.put(f'{url}/user/profile/setname/v2', json={
        'token': user['token'],
        'name_first': 'john',
        'name_last': '',
    }).status_code == InputError.code

def test_invalid_token_setname(clear_data, user):    
    '''
    Tests whether input error is raised for invalid token
    '''       
    assert requests.put(f'{url}/user/profile/setname/v2', json={
        'token': 'invalid_token',
        'name_first': 'john',
        'name_last': 'smith',
    }).status_code == InputError.code    

##Tests for user/profile/setemail/v2
def test_invalid_setemail(clear_data, user):
    '''
    Tests whether input error is raised for invalid email
    '''       
    assert requests.put(f'{url}/user/profile/setemail/v2', json={
        'token': user['token'],
        'email': 'rob.com'
    }).status_code == InputError.code    

def test_shared_setemail(clear_data, user, user2): 
    '''
    Tests whether input error is raised for shared email
    '''       
    assert requests.put(f'{url}/user/profile/setemail/v2', json={
        'token': user['token'],
        'email': 'tim@gmail.com'
    }).status_code == InputError.code 

def test_invalid_token_setemail(clear_data, user):    
    '''
    Tests whether input error is raised for invalid token
    '''       
    assert requests.put(f'{url}/user/profile/setemail/v2', json={
        'token': 'invalid_token',
        'email': 'rob@gmail.com'
    }).status_code == InputError.code         

##Tests for user/profile/sethandle/v1
def test_invalid_handle(clear_data, user):
    '''
    Tests whether input error is raised for invalid handle
    '''       
    assert requests.put(f'{url}user/profile/sethandle/v1', json={
        'token': user['token'],
        'handle_str': 'ao'
    }).status_code == InputError.code  

def test_shared_handle(clear_data, user, user2):  
    '''
    Tests whether input error is raised for shared email
    '''       
    assert requests.put(f'{url}/user/profile/sethandle/v1', json={
        'token': user2['token'],
        'handle_str': 'tombrown'
    }).status_code == InputError.code

def test_invalid_token_sethandle(clear_data, user):    
    '''
    Tests whether input error is raised for invalid token
    '''       
    assert requests.put(f'{url}/user/profile/sethandle/v1', json={
        'token': 'invalid_token',
        'handle_str': 'robblue',
    }).status_code == InputError.code        

##Tests for users/all/v1
def test_all_users(clear_data, user, user2):
    '''
    Tests whether all users are returned (successful implementation)
    '''       
    query_string = f"token={user['token']}"
    users = requests.get(f'{url}/users/all/v1?{query_string}')
    payload = users.json()
    assert len(payload['users']) == 2  

def test_invalid_token_users_all(clear_data, user):    
    '''
    Tests whether input error is raised for invalid token
    '''       
    query_string = 'token=invalid_token'
    assert requests.get(f'{url}/users/all/v1?{query_string}').status_code == InputError.code    

##Tests for user/stats/v1
def test_success_user_stats(clear_data, user, user2):
    '''
    Tests whether user_stats are returned (successful implementation)
    '''       
    c = requests.post(f'{url}/channels/create/v2', json={
        'token': user['token'],
        'name': 'channel1',
        'is_public': True,
    }).json()
    requests.post(f'{url}/dm/create/v1', json={
        'token': user['token'],
        'u_ids': [1],
    })
    requests.post(f'{url}/message/send/v2', json={
        'token': user['token'],
        'channel_id': c['channel_id'],
        'message': 'Hello'
    })    
    assert requests.get(f"{url}user/stats/v1?token={user['token']}").status_code == 200

def test_invalid_token_user_stat(clear_data, user):
    '''
    Tests whether input error is raised for invalid token
    '''       
    assert requests.get(f"{url}user/stats/v1?token=invalid_token").status_code == InputError.code
   

##Tests for users/stats/v1
def test_success_users_stats(clear_data, user, user2):
    '''
    Tests whether dreams_stats are returned (successful implementation)
    '''     
    c = requests.post(f'{url}/channels/create/v2', json={
        'token': user['token'],
        'name': 'channel1',
        'is_public': True,
    }).json()
    requests.post(f'{url}/dm/create/v1', json={
        'token': user['token'],
        'u_ids': [1],
    })
    requests.post(f'{url}/message/send/v2', json={
        'token': user['token'],
        'channel_id': 0,
        'message': 'Hello'
    })         
    assert requests.get(f"{url}users/stats/v1?token={user['token']}").status_code == 200

def test_invalid_token_users_stat(clear_data, user):
    '''
    Tests whether input error is raised for invalid token
    '''       
    assert requests.get(f"{url}users/stats/v1?token=invalid_token").status_code == InputError.code

##Tests for /user/profile/uploadphoto/v1
def test_invalid_token_uploadphoto(clear_data, user):
    '''
    Tests whether input error is raised for invalid token
    '''      
    assert requests.post(f'{url}/user/profile/uploadphoto/v1', json={
        'token': 'invalid_token',
        'img_url': IMG_URL,
        'x_start': 50,
        'y_start': 50,
        'x_end': 200,
        'y_end': 200,
    }).status_code == InputError.code

def test_invalid_x_dim(clear_data, user):
    '''
    Tests whether input error is raised for invalid x dimensions
    '''      
    assert requests.post(f'{url}/user/profile/uploadphoto/v1', json={
        'token': user['token'],
        'img_url': IMG_URL,
        'x_start': 1800,
        'y_start': 50,
        'x_end': 200,
        'y_end': 50,
    }).status_code == InputError.code   

def test_invalid_y_dim(clear_data, user):
    '''
    Tests whether input error is raised for invalid y dimensions
    '''      
    assert requests.post(f'{url}/user/profile/uploadphoto/v1', json={
        'token': user['token'],
        'img_url': IMG_URL,
        'x_start': 150,
        'y_start': 20000,
        'x_end': 200,
        'y_end': 200,
    }).status_code == InputError.code 

def test_invalid_img_url(clear_data, user):
    '''
    Tests whether input error is raised if image is not JPG
    '''     
    assert requests.post(f'{url}/user/profile/uploadphoto/v1', json={
        'token': user['token'],
        'img_url': FAKE_URL,
        'x_start': 50,
        'y_start': 50,
        'x_end': 200,
        'y_end': 200,
    }).status_code == InputError.code

def test_valid_img_url(clear_data, user):
    '''
    Tests whether user_profile_uploadphoto_v1 works (successful implementation)
    '''     
    assert requests.post(f'{url}/user/profile/uploadphoto/v1', json={
        'token': user['token'],
        'img_url': IMG_URL,
        'x_start': 60,
        'y_start': 60,
        'x_end': 200,
        'y_end': 200,
    }).status_code == 200

def test_invalid_img_url2(clear_data, user, user2):
    '''
    Tests whether input error is raised for invalid url
    '''      
    assert requests.post(f'{url}/user/profile/uploadphoto/v1', json={
        'token': user['token'],
        'img_url': FAKE_URL,
        'x_start': 50,
        'y_start': 50,
        'x_end': 200,
        'y_end': 200,
    }).status_code == InputError.code   
