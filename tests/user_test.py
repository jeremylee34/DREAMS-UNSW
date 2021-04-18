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
import src.data as data

IMG_URL = "https://cdn.mos.cms.futurecdn.net/YB6aQqKZBVjtt3PuDSkJKe.jpg"
FAKE_URL = "https://cdn.mos.cms.futurecdn.net/YB6aQqKZBVjtt3PuDSkJKe.png"

@pytest.fixture
#Clears all data
def clear_data():
    clear_v1()

##Tests for user_profile_v1
#Tests whether input error is raised for invalid u_id
def test_invalid_uid(clear_data):
    register = auth_register_v1("asdf@gmail.com", "12344545", "K","S")
    with pytest.raises(InputError):
        assert user_profile_v1(register['token'], 2)

#Tests whether correct user is looked at (successful implementation)
def test_profile_success(clear_data):
    register = auth_register_v1("asdf@gmail.com", "12344545", "K","S")
    login = auth_login_v1("asdf@gmail.com", "12344545")
    auth_login_v1("asdf@gmail.com", "12344545")
    profile = user_profile_v1(login['token'], 0)
    assert register['auth_user_id'] == profile['user']['u_id']

#Tests whether access error is raised for invalid token
def test_invalid_token_profile(clear_data):
    auth_register_v1("asdf@gmail.com", "12344545", "K","S")
    with pytest.raises(InputError):
        assert user_profile_v1('invalid_token', 0)    

##Tests for user_profile_setname_v1
#Tests whether input error is raised for invalid firstname
def test_invalid_firstname(clear_data):
    register = auth_register_v1("asdf@gmail.com", "12344545", "K","S")
    with pytest.raises(InputError):
        assert user_profile_setname_v1(register['token'], '', 'johnson')   

#Tests whether input error is raised for invalid lastname
def test_invalid_lastname(clear_data):
    register = auth_register_v1("asdf@gmail.com", "12344545", "K","S")
    with pytest.raises(InputError):
        assert user_profile_setname_v1(register['token'], 'timothy', '') 

#Tests whether user lastname and firstname has been changed (successful implementation)
def test_profile_setname_success(clear_data):
    register = auth_register_v1("asdf@gmail.com", "12344545", "K","S")
    auth_login_v1("asdf@gmail.com", "12344545")
    auth_login_v1("asdf@gmail.com", "12344545")
    result1 = user_profile_v1(register['token'], 0)
    user_profile_setname_v1(register['token'], 'timothy', 'smith')
    result2 = user_profile_v1(register['token'], 0)
    assert result1['user']['name_first'] != result2['user']['name_first'] and result1['user']['name_last'] != result2['user']['name_last']

#Tests whether access error is raised for invalid token
def test_invalid_token_setname(clear_data):
    auth_register_v1("asdf@gmail.com", "12344545", "K","S")
    with pytest.raises(InputError):
        assert user_profile_setname_v1('invalid_token', 'tim', 'blue') 

##Tests for user_profile_setemail_v1
#Tests whether input error is raised for invalid email
def test_invalid_email(clear_data):
    register = auth_register_v1("asdf@gmail.com", "12344545", "K","S")
    with pytest.raises(InputError):
        assert user_profile_setemail_v1(register['token'], 'rob.com')     

#Tests whether input error is raised for shared email
def test_shared_email(clear_data):
    register1 = auth_register_v1("asdf@gmail.com", "12344545", "K","S")
    auth_register_v1("fish@gmail.com", "12344545", "fish","sea")
    with pytest.raises(InputError):
        assert user_profile_setemail_v1(register1['token'], 'fish@gmail.com') 

#Tests whether email has been changed (successful implementation)
def test_profile_email_success(clear_data):
    register = auth_register_v1("asdf@gmail.com", "12344545", "K","S")
    auth_login_v1("asdf@gmail.com", "12344545")
    auth_login_v1("asdf@gmail.com", "12344545")
    result1 = user_profile_v1(register['token'], 0)
    user_profile_setemail_v1(register['token'], 'tom@gmail.com')
    result2 = user_profile_v1(register['token'], 0)
    assert result1['user']['email'] != result2['user']['email']

#Tests whether access error is raised for invalid token
def test_invalid_token_setemail(clear_data):
    auth_register_v1("asdf@gmail.com", "12344545", "K","S")
    with pytest.raises(InputError):
        assert user_profile_setemail_v1('invalid_token', 'tim@gmail.com') 
            

##Tests for user_profile_sethandle_v1
#Tests whether input error is raised for invalid handle
def test_invalid_handle(clear_data):
    register = auth_register_v1("asdf@gmail.com", "12344545", "K","S")
    with pytest.raises(InputError):
        assert user_profile_sethandle_v1(register['token'], 'jo') 

#Tests whether input error is raised for shared handle
def test_shared_handle(clear_data):
    register1 = auth_register_v1("asdf@gmail.com", "12344545", "K","S")
    auth_register_v1("honey@yahoo.com", "12344545", "honey","bear")
    with pytest.raises(InputError):
        assert user_profile_sethandle_v1(register1['token'], 'honeybear')  

#Tests whether handle has been changed (successful implementation)
def test_profile_sethandle_success(clear_data):    
    register = auth_register_v1("asdf@gmail.com", "12344545", "K","S")
    auth_login_v1("asdf@gmail.com", "12344545")
    auth_login_v1("asdf@gmail.com", "12344545")
    result1 = user_profile_v1(register['token'], 0)
    user_profile_sethandle_v1(register['token'], 'hello')
    result2 = user_profile_v1(register['token'], 0)
    assert result1['user']['handle_str'] != result2['user']['handle_str']

#Tests whether access error is raised for invalid token
def test_invalid_token_sethandle(clear_data):
    auth_register_v1("asdf@gmail.com", "12344545", "K","S")
    with pytest.raises(InputError):
        assert user_profile_sethandle_v1('invalid_token', 'honeybear') 
            

##Tests for users_all_v1
#Tests whether all users are returned (successful implementation)
def test_all_users(clear_data):
    register1 = auth_register_v1("asdf@gmail.com", "12344545", "K","S")
    auth_register_v1("honey@yahoo.com", "12344545", "honey","bear")
    user_result = users_all_v1(register1['token'])
    assert len(user_result['users']) == 2 

#Tests whether access error is raised for invalid token
def test_invalid_token_users_all(clear_data):
    auth_register_v1("asdf@gmail.com", "12344545", "K","S")
    with pytest.raises(InputError):
        assert users_all_v1('invalid_token') 

##Tests for user/stats/v1
#checks for invalid token
def test_user_stat_invalid_token(clear_data):
    auth_register_v1("toom@gmail.com", "hello1234", "tom", "brown")
    with pytest.raises(InputError):
        assert user_stats_v1('invalid_token')

def test_empty_stats(clear_data):
    r = auth_register_v1("toom@gmail.com", "hello1234", "tom", "brown")
    auth_login_v1("toom@gmail.com", "hello1234")
    auth_login_v1("toom@gmail.com", "hello1234")
    assert len(user_stats_v1(r['token'])) == 4

def test_multiple_stats(clear_data):
    r = auth_register_v1("toom@gmail.com", "hello1234", "tom", "brown")
    auth_register_v1("tim@gmail.com", "hello1234", "tim", "brown")
    user_stats_v1(r['token'])
    channel = channels_create_v1(r['token'], "Channel1", True)
    message_send_v1(r['token'], channel['channel_id'], 'Hello')
    dm = dm_create_v1(r['token'], [1])
    assert len(user_stats_v1(r['token'])) == 4

def test_multiple_user_stat(clear_data):
    r = auth_register_v1("toom@gmail.com", "hello1234", "tom", "brown")
    s = auth_register_v1("tim@gmail.com", "hello1234", "tim", "brown")
    user_stats_v1(r['token'])
    channel = channels_create_v1(r['token'], "Channel1", True)
    message_send_v1(r['token'], channel['channel_id'], 'Hello')
    dm = dm_create_v1(r['token'], [1])
    assert len(user_stats_v1(s['token'])) == 4

##Tests for users/stats/v1
#checks for how big is the dictionary to test if function is successful
def test_users_stat_invalid_token(clear_data):
    auth_register_v1("toom@gmail.com", "hello1234", "tom", "brown")
    with pytest.raises(InputError):
        assert users_stats_v1('invalid_token')

def test_multiple(clear_data):
    r =  auth_register_v1("toom@gmail.com", "hello1234", "tom", "brown")
    auth_register_v1("tim@gmail.com", "hello1234", "tim", "brown")
    channel = channels_create_v1(r['token'], "Channel1", True)
    message_send_v1(r['token'], channel['channel_id'], 'Hello')
    users_stats_v1(r['token'])
    dm = dm_create_v1(r['token'], [1])
    assert len(users_stats_v1(r['token'])) == 4

def test_removing_dm_and_messages(clear_data):
    r =  auth_register_v1("toom@gmail.com", "hello1234", "tom", "brown")
    s = auth_register_v1("tim@gmail.com", "hello1234", "tim", "brown")
    channel = channels_create_v1(r['token'], "Channel1", True)
    channels_create_v1(s['token'], "Channel2", True)
    dms = dm_create_v1(r['token'], [1])
    dms1 = dm_create_v1(s['token'], [0])  
    message_id = message_send_v1(r['token'], channel['channel_id'], 'Hello')
    message_send_v1(r['token'], channel['channel_id'], 'Hello')
    message_share_v1(s['token'], message_id['message_id'], '', -1, dms['dm_id'])
    message_share_v1(s['token'], message_id['message_id'], '', -1, dms1['dm_id'])
    message_share_v1(s['token'], message_id['message_id'], '', -1, dms['dm_id'])
    message_share_v1(r['token'], message_id['message_id'], '', -1, dms1['dm_id'])
    dm_remove_v1(r['token'], 0) 
    message_remove_v1(r['token'], 0)  
    message_remove_v1(s['token'], 3) 
    users_stats_v1(r['token'])
    dm_remove_v1(s['token'], 1)
    assert len(users_stats_v1(r['token'])) == 4 

def test_users_joined_channels(clear_data):
    r =  auth_register_v1("toom@gmail.com", "hello1234", "tom", "brown")
    s = auth_register_v1("tim@gmail.com", "hello1234", "tim", "brown")
    channel = channels_create_v1(r['token'], "Channel1", True)
    channel_join_v1(s['token'], 0)
    channels_create_v1(r['token'], "Channel2", True)
    assert len(users_stats_v1(r['token'])) == 4

def test_users_joined_dms(clear_data):   
    r =  auth_register_v1("toom@gmail.com", "hello1234", "tom", "brown")
    s = auth_register_v1("tim@gmail.com", "hello1234", "tim", "brown")
    dm_create_v1(r['token'], [1])  
    assert len(users_stats_v1(r['token'])) == 4   

def test_empty_messages_dms(clear_data):
    r =  auth_register_v1("toom@gmail.com", "hello1234", "tom", "brown")
    s = auth_register_v1("tim@gmail.com", "hello1234", "tim", "brown")
    channel = channels_create_v1(r['token'], "Channel1", True) 
    dms = dm_create_v1(r['token'], [1])
    message_id = message_send_v1(r['token'], channel['channel_id'], 'Hello')
    message_share_v1(r['token'], message_id['message_id'], '', -1, dms['dm_id'])
    message_share_v1(r['token'], message_id['message_id'], '', -1, dms['dm_id'])  
    message_share_v1(r['token'], message_id['message_id'], '', -1, dms['dm_id']) 
    message_remove_v1(r['token'], 3) 
    assert len(users_stats_v1(r['token'])) == 4 

##Tests for /user/profile/uploadphoto/v1
'''
    InputError - img_url returns a HTTP status other than 200 (not successful)
'''
def test_user_uploadphoto_invalid_token(clear_data):
    auth_register_v1("toom@gmail.com", "hello1234", "tom", "brown")
    with pytest.raises(InputError):
        assert user_profile_uploadphoto_v1('invalid_token', IMG_URL, 50, 50, 200, 200)

def test_invalid_x_dimensions(clear_data):
    r = auth_register_v1("toom@gmail.com", "hello1234", "tom", "brown")
    with pytest.raises(InputError):
        assert user_profile_uploadphoto_v1(r['token'], IMG_URL, 1800, 50, 200, 50)

def test_invalid_x_dimensions2(clear_data):
    r = auth_register_v1("toom@gmail.com", "hello1234", "tom", "brown")
    with pytest.raises(InputError):
        assert user_profile_uploadphoto_v1(r['token'], IMG_URL, 500, 500, 500, 1000)

def test_invalid_y_dimensions(clear_data):
    r = auth_register_v1("toom@gmail.com", "hello1234", "tom", "brown")
    with pytest.raises(InputError):
        assert user_profile_uploadphoto_v1(r['token'], IMG_URL, 150, 2000, 200, 200) 

def test_invalid_y_dimensions2(clear_data):
    r = auth_register_v1("toom@gmail.com", "hello1234", "tom", "brown")
    with pytest.raises(InputError):
        assert user_profile_uploadphoto_v1(r['token'], IMG_URL, 500, 500, 1000, 500)          

def test_not_jpeg(clear_data):
    r = auth_register_v1("toom@gmail.com", "hello1234", "tom", "brown")
    with pytest.raises(InputError):
        assert user_profile_uploadphoto_v1(r['token'], FAKE_URL, 50, 50, 200, 200)    

def test_img_url_saved(clear_data):
    r = auth_register_v1("toom@gmail.com", "hello1234", "tom", "brown")
    auth_login_v1("toom@gmail.com", "hello1234")
    auth_login_v1("toom@gmail.com", "hello1234")
    assert user_profile_uploadphoto_v1(r['token'], IMG_URL, 50, 50, 200, 200) == {}