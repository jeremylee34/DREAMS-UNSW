'''
Implementation of tests for user functions
Written by Kanit Srihakorth and Tharushi Gunawardana
'''

import pytest
import re
from src.auth import auth_register_v1
from src.auth import auth_login_v1
from src.user import user_profile_v1
from src.user import user_profile_setname_v1
from src.user import user_profile_setemail_v1
from src.user import user_profile_sethandle_v1
from src.user import user_profile_uploadphoto_v1
from src.user import user_stats_v1
from src.user import users_stats_v1
from src.user import users_all_v1
from src.message import message_send_v1, message_share_v1, message_remove_v1
from src.channels import channels_create_v1
from src.channel import channel_join_v1
from src.dm import dm_create_v1, dm_remove_v1
from src.error import InputError, AccessError
from src.other import clear_v1

IMG_URL = "https://cdn.mos.cms.futurecdn.net/YB6aQqKZBVjtt3PuDSkJKe.jpg"
FAKE_URL = "https://cdn.mos.cms.futurecdn.net/YB6aQqKZBVjtt3PuDSkJKe.png"
FAKE_URL2 = "https://cdn.mos.cms/YB6aQqKZBVjtt3PuDSkJKe.jpg"

@pytest.fixture
def clear_data():
    '''
    Clears all data
    '''
    clear_v1()

@pytest.fixture
def user(): 
    '''
    Calls auth_register_v1 to register user
    '''
    user = auth_register_v1("asdf@gmail.com", "12344545", "K","S")
    return user

@pytest.fixture
def user2():
    '''
    Calls auth_register_v1 to register second user
    '''    
    user2 = auth_register_v1("fish@gmail.com", "12344545", "fish","sea")
    return user2

@pytest.fixture
def login1():
    '''
    Calls auth_login_v1 to login user
    '''    
    login1 = auth_login_v1("asdf@gmail.com", "12344545")
    return login1

@pytest.fixture
def login2():
    '''
    Calls auth_login_v1 to login user again
    '''     
    login2 = auth_login_v1("asdf@gmail.com", "12344545")
    return login2  

@pytest.fixture
def profile(user):
    '''
    Calls user_profile_v1 to get user information
    '''     
    profile = user_profile_v1(user['token'], 0)
    return profile 

##Tests for user_profile_v1
def test_invalid_uid(clear_data, user):
    '''
    Tests whether input error is raised for invalid u_id
    '''     
    with pytest.raises(InputError):
        assert user_profile_v1(user['token'], 2)

def test_profile_success(clear_data, user, login1, login2, profile):
    '''
    Tests whether correct user is looked at (successful implementation)
    '''     
    assert user['auth_user_id'] == profile['user']['u_id']

def test_invalid_token_profile(clear_data, user):
    '''
    Tests whether input error is raised for invalid token
    '''     
    with pytest.raises(InputError):
        assert user_profile_v1('invalid_token', 0)    

##Tests for user_profile_setname_v1
def test_invalid_firstname(clear_data, user):
    '''
    Tests whether input error is raised for invalid firstname
    ''' 
    with pytest.raises(InputError):
        assert user_profile_setname_v1(user['token'], '', 'johnson')   

def test_invalid_lastname(clear_data, user):
    '''
    Tests whether input error is raised for invalid lastname
    '''     
    with pytest.raises(InputError):
        assert user_profile_setname_v1(user['token'], 'timothy', '') 

def test_profile_setname_success(clear_data, user, login1, login2, profile):
    '''
    Tests whether user lastname and firstname has been changed (successful implementation)
    '''     
    user_profile_setname_v1(user['token'], 'timothy', 'smith')
    result = user_profile_v1(user['token'], 0)
    assert profile['user']['name_first'] != result['user']['name_first'] and profile['user']['name_last'] != result['user']['name_last']

def test_invalid_token_setname(clear_data, user):
    '''
    Tests whether access error is raised for invalid token
    '''       
    with pytest.raises(InputError):
        assert user_profile_setname_v1('invalid_token', 'tim', 'blue') 

##Tests for user_profile_setemail_v1
def test_invalid_email(clear_data, user):
    '''
    Tests whether input error is raised for invalid email
    '''       
    with pytest.raises(InputError):
        assert user_profile_setemail_v1(user['token'], 'rob.com')     

def test_shared_email(clear_data, user, user2):
    '''
    Tests whether input error is raised for shared email
    '''       
    with pytest.raises(InputError):
        assert user_profile_setemail_v1(user['token'], 'fish@gmail.com') 

def test_profile_email_success(clear_data, user, login1, login2, profile):
    '''
    Tests whether email has been changed (successful implementation)
    '''       
    user_profile_setemail_v1(user['token'], 'tom@gmail.com')
    result = user_profile_v1(user['token'], 0)
    assert profile['user']['email'] != result['user']['email']

def test_invalid_token_setemail(clear_data, user):
    '''
    Tests whether access error is raised for invalid token
    '''       
    with pytest.raises(InputError):
        assert user_profile_setemail_v1('invalid_token', 'tim@gmail.com') 
            

##Tests for user_profile_sethandle_v1
def test_invalid_handle(clear_data, user):
    '''
    Tests whether input error is raised for invalid handle
    '''      
    with pytest.raises(InputError):
        assert user_profile_sethandle_v1(user['token'], 'jo') 

def test_shared_handle(clear_data, user, user2):
    '''
    Tests whether input error is raised for shared handle
    '''     
    with pytest.raises(InputError):
        assert user_profile_sethandle_v1(user['token'], 'fishsea')  

def test_profile_sethandle_success(clear_data, user, login1, login2, profile):    
    '''
    Tests whether handle has been changed (successful implementation)
    '''      
    user_profile_sethandle_v1(user['token'], 'hello')
    result = user_profile_v1(user['token'], 0)
    assert profile['user']['handle_str'] != result['user']['handle_str']

def test_invalid_token_sethandle(clear_data, user):
    '''
    Tests whether access error is raised for invalid token
    '''      
    with pytest.raises(InputError):
        assert user_profile_sethandle_v1('invalid_token', 'honeybear') 
            

##Tests for users_all_v1
def test_all_users(clear_data, user, user2):
    '''
    Tests whether all users are returned (successful implementation)
    '''      
    user_result = users_all_v1(user['token'])
    assert len(user_result['users']) == 2 

def test_invalid_token_users_all(clear_data, user):
    '''
    Tests whether input error is raised for invalid token
    '''      
    with pytest.raises(InputError):
        assert users_all_v1('invalid_token') 

##Tests for user/stats/v1
def test_user_stat_invalid_token(clear_data, user):
    '''
    Tests whether input error is raised for invalid token
    '''      
    with pytest.raises(InputError):
        assert user_stats_v1('invalid_token')

def test_empty_stats(clear_data, user, login1, login2): 
    '''
    Tests whether stats are returned for no data (successful implementation)
    '''      
    stats = user_stats_v1(user['token'])
    assert len(stats['user_stats']) == 4

def test_multiple_stats(clear_data, user, user2):
    '''
    Tests whether stats are returned multiple times (successful implementation)
    '''      
    user_stats_v1(user['token'])
    channel = channels_create_v1(user['token'], "Channel1", True)
    message_send_v1(user['token'], channel['channel_id'], 'Hello')
    dm_create_v1(user['token'], [1])
    stats = user_stats_v1(user2['token'])
    assert len(stats['user_stats']) == 4

def test_multiple_user_stat(clear_data, user, user2):
    '''
    Tests whether one user's stats are returned when there are multiple users (successful implementation)
    '''      
    user_stats_v1(user['token'])
    channel = channels_create_v1(user['token'], "Channel1", True)
    message_send_v1(user['token'], channel['channel_id'], 'Hello')
    dm_create_v1(user['token'], [1])
    stats = user_stats_v1(user['token'])
    assert len(stats['user_stats']) == 4

##Tests for users/stats/v1
def test_users_stat_invalid_token(clear_data, user):
    '''
    Tests whether input error is raised for invalid token
    '''         
    with pytest.raises(InputError):
        assert users_stats_v1('invalid_token')

def test_multiple(clear_data, user, user2):
    '''
    Tests dreams_stats are returned when multiple users are registered (successful implementation)
    '''      
    channel = channels_create_v1(user['token'], "Channel1", True)
    message_send_v1(user['token'], channel['channel_id'], 'Hello')
    users_stats_v1(user['token'])
    dm_create_v1(user['token'], [1])
    stats = users_stats_v1(user['token'])
    assert len(stats['dreams_stats']) == 4

def test_removing_dm_and_messages(clear_data, user, user2):
    '''
    Tests dreams_stats are returned when dms and messages are removed (successful implementation)
    '''       
    channel = channels_create_v1(user['token'], "Channel1", True)
    channels_create_v1(user2['token'], "Channel2", True)
    dms = dm_create_v1(user['token'], [1])
    dms1 = dm_create_v1(user2['token'], [0])  
    message_id = message_send_v1(user['token'], channel['channel_id'], 'Hello')
    message_send_v1(user['token'], channel['channel_id'], 'Hello')
    message_share_v1(user2['token'], message_id['message_id'], '', -1, dms['dm_id'])
    message_share_v1(user2['token'], message_id['message_id'], '', -1, dms1['dm_id'])
    message_share_v1(user2['token'], message_id['message_id'], '', -1, dms['dm_id'])
    message_share_v1(user['token'], message_id['message_id'], '', -1, dms1['dm_id'])
    dm_remove_v1(user['token'], 0) 
    message_remove_v1(user['token'], 0)  
    message_remove_v1(user2['token'], 3) 
    users_stats_v1(user['token'])
    dm_remove_v1(user2['token'], 1)
    stats = users_stats_v1(user['token'])
    assert len(stats['dreams_stats']) == 4

def test_users_joined_channels(clear_data, user, user2):
    '''
    Tests dreams_stats are returned when multiple users have joined channels (successful implementation)
    '''       
    channels_create_v1(user['token'], "Channel1", True)
    channel_join_v1(user2['token'], 0)
    channels_create_v1(user['token'], "Channel2", True)
    stats = users_stats_v1(user['token'])
    assert len(stats['dreams_stats']) == 4

def test_users_joined_dms(clear_data, user, user2):   
    '''
    Tests dreams_stats are returned when multiple users have joined dms (successful implementation)
    '''      
    dm_create_v1(user['token'], [1])  
    stats = users_stats_v1(user['token'])
    assert len(stats['dreams_stats']) == 4  

def test_empty_messages_dms(clear_data, user, user2):
    '''
    Tests dreams_stats are returned when a message is removed in a dm (successful implementation)
    '''      
    channel = channels_create_v1(user['token'], "Channel1", True) 
    dms = dm_create_v1(user['token'], [1])
    message_id = message_send_v1(user['token'], channel['channel_id'], 'Hello')
    message_share_v1(user['token'], message_id['message_id'], '', -1, dms['dm_id'])
    message_share_v1(user['token'], message_id['message_id'], '', -1, dms['dm_id'])  
    message_share_v1(user['token'], message_id['message_id'], '', -1, dms['dm_id']) 
    message_remove_v1(user['token'], 3) 
    stats = users_stats_v1(user['token'])
    assert len(stats['dreams_stats']) == 4

##Tests for /user/profile/uploadphoto/v1
def test_user_uploadphoto_invalid_token(clear_data, user):
    '''
    Tests whether input error is raised for invalid token
    '''      
    with pytest.raises(InputError):
        assert user_profile_uploadphoto_v1('invalid_token', IMG_URL, 50, 50, 200, 200)

def test_invalid_x_dimensions(clear_data, user):
    '''
    Tests whether input error is raised for invalid x dimensions
    '''      
    with pytest.raises(InputError):
        assert user_profile_uploadphoto_v1(user['token'], IMG_URL, 1800, 50, 200, 50)

def test_invalid_x_dimensions2(clear_data, user):
    '''
    Tests whether input error is raised for x dimensions being the same
    '''      
    with pytest.raises(InputError):
        assert user_profile_uploadphoto_v1(user['token'], IMG_URL, 500, 500, 500, 1000)

def test_invalid_y_dimensions(clear_data, user):
    '''
    Tests whether input error is raised for invallid y dimensions
    '''      
    with pytest.raises(InputError):
        assert user_profile_uploadphoto_v1(user['token'], IMG_URL, 150, 2000, 200, 200) 

def test_invalid_y_dimensions2(clear_data, user):
    '''
    Tests whether input error is raised for y dimensions being the same
    '''       
    with pytest.raises(InputError):
        assert user_profile_uploadphoto_v1(user['token'], IMG_URL, 500, 500, 1000, 500)          

def test_not_jpeg(clear_data, user):
    '''
    Tests whether input error is raised if image is not JPG
    '''       
    with pytest.raises(InputError):
        assert user_profile_uploadphoto_v1(user['token'], FAKE_URL, 50, 50, 200, 200)    

def test_img_url_saved(clear_data, user, login1, login2):
    '''
    Tests whether user_profile_uploadphoto_v1 works (successful implementation)
    '''      
    assert user_profile_uploadphoto_v1(user['token'], IMG_URL, 50, 50, 200, 200) == {}

def test_img_url_invalid(clear_data, user, login1, login2):
    '''
    Tests whether input error is raised for invalid url
    '''      
    with pytest.raises(InputError):
        assert user_profile_uploadphoto_v1(user['token'], FAKE_URL2, 50, 50, 200, 200)
