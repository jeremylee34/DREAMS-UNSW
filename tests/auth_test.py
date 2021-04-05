'''
Implementation of tests for auth functions
Written by Kanit Srihakorth and Tharushi Gunawardana
'''
import pytest
import re
from src.auth import auth_register_v1
from src.auth import auth_login_v1
from src.auth import auth_logout_v1
from src.user import user_profile_v1
from src.error import InputError, AccessError
from src.other import clear_v1
from src.data import data

@pytest.fixture
#Clears all user data
def clear_data():
    clear_v1()
    
## Tests for auth_register
#Tests whether email is valid (successful implementation)
def test_register_valid_email(clear_data):
    register = auth_register_v1("asdf@gmail.com", "12344545", "K","S")
    login = auth_login_v1("asdf@gmail.com", "12344545")
    assert register['auth_user_id'] == login['auth_user_id']
    
#Tests whether input error is raised for invalid email
def test_register_invalid_email(clear_data):
    with pytest.raises(InputError):
        assert auth_register_v1("asdfgmail.com", "12344545", "K","S")
    
#Tests whether email is unshared (successful implementation)
def test_register_email_unshared(clear_data):
    register1 = auth_register_v1("same@gmail.com", "12344545", "Me", "Me")
    register2 = auth_register_v1("Notsame@gmail.com", "12344545", "NotMe", "NotMe")
    assert register1['auth_user_id'] != register2['auth_user_id']

#Tests whether input error is raised for shared email
def test_register_email_shared(clear_data):
    auth_register_v1("same@gmail.com", "12344545", "Me", "Me")
    with pytest.raises(InputError):
        assert auth_register_v1("same@gmail.com", "12344545", "NotMe", "NotMe") is None

#Tests whether input error is raised for invalid password
def test_check_password(clear_data): #less than 6 characters is a fail
    with pytest.raises(InputError):
        assert auth_register_v1("honey@outlook.com", "hi", "Tim", "Oreo")

#Tests whether input error is raised for invalid firstname
def test_firstname_length(clear_data):
    with pytest.raises(InputError):
        assert auth_register_v1("honey@outlook.com", "12345678", "", "Oreo")   

#Tests whether input error is raised for invalid lastname
def test_lastname_length(clear_data):
    with pytest.raises(InputError):
        assert auth_register_v1("honey@outlook.com", "12345678", "Tim", "")


## Tests for login    
#Tests whether input error is raised for incorrect password
def test_login_incorrect_password(clear_data):
    auth_register_v1("hiheee@gmail.com", "1234566", "K","S")
    with pytest.raises(InputError):
        assert auth_login_v1("hiheee@gmail.com", "hello1234")

#Tests whether password is correct (successful implementation)
def test_login_correct_password(clear_data):
    register = auth_register_v1("hiheee@gmail.com", "1234455", "K","S")
    login = auth_login_v1("hiheee@gmail.com", "1234455")
    assert register['auth_user_id'] == login['auth_user_id']

#Tests whether input error is raised for invalid email    
def test_login_invalid_email(clear_data):
    auth_register_v1("hiheee@gmail.com", "1234455", "K","S")
    with pytest.raises(InputError):
        assert auth_login_v1("hiheeegmail", "1234455")

#Tests whether input error is raised for incorrect email
def test_login_incorrect_email(clear_data):
    auth_register_v1("hiheee@gmail.com", "1234455", "K","S")
    with pytest.raises(InputError):
        assert auth_login_v1("hiheee123gmail.com", "1234455")

#Tests whether handle is correct length (successful implementation) 
def test_handle_too_long(clear_data):
    register = auth_register_v1("honey@outlook.com", "hello12345", "honeybear", "beehivebears")
    result = user_profile_v1(register['token'], 0)
    assert len(result['handle_str']) <= 20
   
#Tests whether handle is not shared (successful implementation)
def test_handle_same(clear_data):
    register1 = auth_register_v1("hiheee@gmail.com", "1234455", "K","S")
    register2 = auth_register_v1("honey@outlook.com", "12345678", "K", "S") 
    result1 = user_profile_v1(register1['token'], 0)
    result2 = user_profile_v1(register2['token'], 1)
    assert result1['handle_str'] != result2['handle_str']

#Tests whether handle has no spaces (successful implementation)
def test_handle_space(clear_data):
    register = auth_register_v1("honey@outlook.com", "hello12345", "honey bear", "bees")
    result = user_profile_v1(register['token'], 0)
    check = " " in result['handle_str']
    assert check == False

#Tests when handle is too long and is shared (successful implementation)
def test_handle_too_long_and_shared(clear_data):
    auth_register_v1("honey@outlook.com", "hello12345", "honeybear", "beehivebears")
    register = auth_register_v1("tommy@outlook.com", "tommy12345", "honeybear", "beehivebears")
    result = user_profile_v1(register['token'], 1)
    assert len(result['handle_str']) <= 20

##Tests for logout
#Tests whether logout is successful (successful implementation)
def test_logout(clear_data):
    auth_register_v1("asdf@gmail.com", "12344545", "K","S")
    auth_login_v1("asdf@gmail.com", "12344545")
    login = auth_login_v1("asdf@gmail.com", "12344545")
    auth_login_v1("asdf@gmail.com", "12344545")
    result = auth_logout_v1(login['token'])
    assert result['is_success'] == True 

#Tests whether input error is raised for invalid token
def test_invalid_token(clear_data):
    auth_register_v1("asdf@gmail.com", "12344545", "K","S")
    with pytest.raises(AccessError):
        assert auth_logout_v1('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzZXNzaW9uX2lkcyI6NX0.b_nkhJ8W5M5ThXePUyvtyltxuiYkvqZ-j4FEbiMSKyE')