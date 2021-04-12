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
from src.user import users_all_v1
from src.error import InputError, AccessError
from src.other import clear_v1
from src.data import data

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
    assert register['auth_user_id'] == profile['u_id']

#Tests whether input error is raised for invalid token
def test_invalid_token_profile(clear_data):
    auth_register_v1("asdf@gmail.com", "12344545", "K","S")
    with pytest.raises(InputError):
        assert user_profile_v1('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzZXNzaW9uX2lkcyI6NX0.b_nkhJ8W5M5ThXePUyvtyltxuiYkvqZ-j4FEbiMSKyE', 0)    

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
    assert result1['name_first'] != result2['name_first'] and result1['name_last'] != result2['name_last']

#Tests whether input error is raised for invalid token
def test_invalid_token_setname(clear_data):
    auth_register_v1("asdf@gmail.com", "12344545", "K","S")
    with pytest.raises(InputError):
        assert user_profile_setname_v1('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzZXNzaW9uX2lkcyI6NX0.b_nkhJ8W5M5ThXePUyvtyltxuiYkvqZ-j4FEbiMSKyE', 'tim', 'blue') 

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
    assert result1['email'] != result2['email']

#Tests whether input error is raised for invalid token
def test_invalid_token_setemail(clear_data):
    auth_register_v1("asdf@gmail.com", "12344545", "K","S")
    with pytest.raises(InputError):
        assert user_profile_setemail_v1('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzZXNzaW9uX2lkcyI6NX0.b_nkhJ8W5M5ThXePUyvtyltxuiYkvqZ-j4FEbiMSKyE', 'tim@gmail.com') 
            

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
    assert result1['handle_str'] != result2['handle_str']

#Tests whether input error is raised for invalid token
def test_invalid_token_sethandle(clear_data):
    auth_register_v1("asdf@gmail.com", "12344545", "K","S")
    with pytest.raises(InputError):
        assert user_profile_sethandle_v1('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzZXNzaW9uX2lkcyI6NX0.b_nkhJ8W5M5ThXePUyvtyltxuiYkvqZ-j4FEbiMSKyE', 'honeybear') 
            

##Tests for users_all_v1
#Tests whether all users are returned (successful implementation)
def test_all_users(clear_data):
    register1 = auth_register_v1("asdf@gmail.com", "12344545", "K","S")
    auth_register_v1("honey@yahoo.com", "12344545", "honey","bear")
    user_result = users_all_v1(register1['token'])
    assert len(user_result) == 2 

#Tests whether input error is raised for invalid token
def test_invalid_token_users_all(clear_data):
    auth_register_v1("asdf@gmail.com", "12344545", "K","S")
    with pytest.raises(InputError):
        assert users_all_v1('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzZXNzaW9uX2lkcyI6NX0.b_nkhJ8W5M5ThXePUyvtyltxuiYkvqZ-j4FEbiMSKyE') 

##Tests for user/stats/v1
#checks for how big is the dictionary to test if function is successful

##Tests for users/stats/v1
#checks for how big is the dictionary to test if function is successful

##Tests for /user/profile/uploadphoto/v1
'''
    InputError - img_url returns a HTTP status other than 200 (not successful)
    InputError - x_start, y_start, x_end, y_end are not within the dimensions of the image at the url
    InputError - image uploaded is not a JPEG
'''
