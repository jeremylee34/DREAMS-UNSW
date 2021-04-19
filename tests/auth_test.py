'''
Implementation of tests for auth functions
Written by Kanit Srihakorth and Tharushi Gunawardana
''' 
import pytest
import re
from src.auth import auth_register_v1
from src.auth import auth_login_v1
from src.auth import auth_logout_v1
from src.auth import auth_passwordreset_request_v1
from src.auth import auth_passwordreset_reset_v1
from src.user import user_profile_v1
from src.error import InputError, AccessError
from src.other import clear_v1
from src.data import data
from src.helper import check_secret_code
from src.helper import get_secret_code
from src.helper import generate_secret_code

@pytest.fixture
def clear_data():
    '''
    Clears all user data
    '''
    clear_v1()

@pytest.fixture
def user_token1():
    '''
    Registers first user
    '''
    user_token1 = auth_register_v1("firstUser@gmail.com", "password", "Paras", "Mins")
    return user_token1

@pytest.fixture
def user_token2():
    '''
    Registers second user
    '''
    user_token2 = auth_register_v1("secondUser@gmail.com", "password", "Goyas", "Lsiwe")
    return user_token2

@pytest.fixture
def user_token3():
    '''
    Registers third user
    '''
    user_token3 = auth_register_v1("thirdUser@gmail.com", "password", "Taraa", "safba")
    return user_token3

@pytest.fixture
def login_user_token1():
    '''
    Login first user
    '''
    login_user_token1 = auth_login_v1("firstUser@gmail.com", "password")
    return login_user_token1

@pytest.fixture
def login_user_token2():
    '''
    Login second user
    '''
    login_user_token2 = auth_login_v1("secondUser@gmail.com", "password")
    return login_user_token2

@pytest.fixture
def login_user_token3():
    '''
    Login third user
    '''
    login_user_token3 = auth_login_v1("thirdUser@gmail.com", "password")
    return login_user_token3

########### Tests for auth_register ###########

def test_register_valid_email(clear_data, user_token1, login_user_token1):
    '''
    Tests whether email is valid (successful implementation)
    '''
    assert user_token1['auth_user_id'] == login_user_token1['auth_user_id']
    
def test_register_invalid_email(clear_data):
    '''
    Tests whether input error is raised for invalid email
    '''
    with pytest.raises(InputError):
        assert auth_register_v1("asdfgmail.com", "12344545", "K","S")
    
def test_register_email_unshared(clear_data, user_token1, user_token2):
    '''
    Tests whether email is unshared (successful implementation)
    '''
    assert user_token1['auth_user_id'] != user_token2['auth_user_id']

def test_register_email_shared(clear_data, user_token1):
    '''
    Tests whether input error is raised for shared email
    '''
    with pytest.raises(InputError):
        assert auth_register_v1("firstUser@gmail.com", "12344545", "NotMe", "NotMe")

def test_check_password(clear_data):
    '''
    Tests whether input error is raised for invalid password
    '''
    with pytest.raises(InputError):
        assert auth_register_v1("honey@outlook.com", "hi", "Tim", "Oreo")

def test_firstname_length(clear_data):
    '''
    Tests whether input error is raised for invalid firstname
    '''
    with pytest.raises(InputError):
        assert auth_register_v1("honey@outlook.com", "12345678", "", "Oreo")   

def test_lastname_length(clear_data):
    '''
    Tests whether input error is raised for invalid lastname
    '''
    with pytest.raises(InputError):
        assert auth_register_v1("honey@outlook.com", "12345678", "Tim", "")

########### Tests for login   ###########  

def test_login_incorrect_password(clear_data, user_token1):
    '''
    Tests whether input error is raised for incorrect password
    '''
    with pytest.raises(InputError):
        assert auth_login_v1("firstUser@gmail.com", "wrongpassword")

def test_login_correct_password(clear_data, user_token1, login_user_token1):
    '''
    Tests whether password is correct (successful implementation)
    '''
    assert user_token1['auth_user_id'] == login_user_token1['auth_user_id']

def test_login_invalid_email(clear_data, user_token1):
    '''
    Tests whether input error is raised for invalid email    
    '''
    with pytest.raises(InputError):
        assert auth_login_v1("firstUsergmail.com", "1234455")

def test_login_incorrect_email(clear_data, user_token1):
    '''
    Tests whether input error is raised for incorrect email
    '''
    with pytest.raises(InputError):
        assert auth_login_v1("hiheasdee123gmail.com", "1234455")

def test_handle_too_long(clear_data, user_token1):
    '''
    Tests whether handle is correct length (successful implementation) 
    '''
    result = user_profile_v1(user_token1['token'], 0)
    assert len(result['user']['handle_str']) <= 20
   
def test_handle_same(clear_data, user_token1, user_token2):
    '''
    Tests whether handle is not shared (successful implementation)
    '''
    result1 = user_profile_v1(user_token1['token'], 0)
    result2 = user_profile_v1(user_token2['token'], 1)
    assert result1['user']['handle_str'] != result2['user']['handle_str']

def test_handle_space(clear_data, user_token1):
    '''
    Tests whether handle has no spaces (successful implementation)
    '''
    result = user_profile_v1(user_token1['token'], 0)
    check = " " in result['user']['handle_str']
    assert check == False

def test_handle_too_long_and_shared(clear_data):
    '''
    Tests when handle is too long and is shared (successful implementation)
    '''
    auth_register_v1("honey@outlook.com", "hello12345", "honeybear", "beehivebearsasa")
    register = auth_register_v1("tommy@outlook.com", "tommy12345", "honeybear", "beehivebearsasa")
    result = user_profile_v1(register['token'], 1)
    assert len(result['user']['handle_str']) <= 20
    assert result['user']['handle_str'] == 'honeybearbeehivebea0'

########### Tests for logout   ###########  

def test_logout(clear_data, user_token1, login_user_token1):
    '''
    Tests whether logout is successful (successful implementation)
    '''
    result = auth_logout_v1(login_user_token1['token'])
    assert result['is_success'] == True 

def test_invalid_token(clear_data, user_token1):
    '''
    Tests whether input error is raised for invalid token
    '''
    with pytest.raises(AccessError):
        assert auth_logout_v1('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzZXNzaW9uX2lkcyI6NX0.b_nkhJ8W5M5ThXePUyvtyltxuiYkvqZ-j4FEbiMSKyE')

########### Tests for passwordreset/request   ###########  

def test_pssword_req_invalid_email(clear_data):
    '''
    Test if email is invalid
    '''
    with pytest.raises(InputError):
        auth_passwordreset_request_v1('asdasdmail.com')

def test_pssword_req_invalid_user(clear_data, user_token1):
    '''
    Test if user is registered user
    '''
    with pytest.raises(InputError):
        auth_passwordreset_request_v1('ABC@gmail.com')

########### Tests for passwordreset/reset   ###########  

def test_reset_get_secret_code(clear_data, user_token1):
    '''
    Test if secret code helper function worked
    '''
    with pytest.raises(InputError):
        assert get_secret_code('67')

def test_invalid_reset_code(clear_data, user_token1):
    '''
    Tests whether input error is raised for invalid reset code (reset code is not the same as given reset code for user) 
    '''
    auth_passwordreset_request_v1("firstUser@gmail.com")
    with pytest.raises(InputError):
        assert auth_passwordreset_reset_v1('asdf', 'hello1234')

def test_reset_invalid_secretcode(clear_data, user_token1):
    '''
    Tests whether input error is raised for invalid secretcode
    '''
    auth_passwordreset_request_v1("firstUser@gmail.com")
    with pytest.raises(InputError):
        assert auth_passwordreset_reset_v1('1', 'hiasdasdasd')

def test_reset_valid_secretcode_but_wrong(clear_data, user_token1):
    '''
    Tests whether valid secret code actually is secret code or not
    '''
    auth_passwordreset_request_v1("firstUser@gmail.com")
    with pytest.raises(InputError):
        assert auth_passwordreset_reset_v1('ASDFAS', 'hiasdasdasd')

def test_reset_newpass(clear_data, user_token1):
    '''
    Check if new_password actually work
    '''
    auth_passwordreset_request_v1("firstUser@gmail.com")
    secret_code = get_secret_code(user_token1['auth_user_id'])
    auth_passwordreset_reset_v1(secret_code, 'newpasswordomg')
    user_login = auth_login_v1("firstUser@gmail.com", 'newpasswordomg')
    assert user_login['auth_user_id'] == 0

def test_reset_invalid_password(clear_data, user_token1):
    '''
    Tests whether input error is raised for invalid password
    '''
    auth_passwordreset_request_v1("firstUser@gmail.com")
    secret_code = get_secret_code(user_token1['auth_user_id'])
    with pytest.raises(InputError):
        assert auth_passwordreset_reset_v1(secret_code, '1')

########### Tests for secret code helper funcs   ###########

def test_gen_secret_code_email_invalid(clear_data, user_token1):
    '''
    Test whether email is invalid or not
    '''  
    with pytest.raises(InputError):
        assert generate_secret_code('yea@gmail.com')

def test_gen_secret_code_email_valid(clear_data, user_token1):
    '''
    Test whether email is valid or not
    '''  
    assert generate_secret_code('firstUser@gmail.com') != '0'

def test_gen_secret_code_email_valid2(clear_data, user_token1, user_token2):
    '''
    Test whether email is invalid or not
    '''  
    auth_passwordreset_request_v1("firstUser@gmail.com")
    assert generate_secret_code('secondUser@gmail.com') != '0'

def test_check_secret_code(clear_data, user_token1):
    '''
    Test whether condition is passed or not
    '''  
    assert check_secret_code('aaaaaa') == 0