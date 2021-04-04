import pytest
import re
from src.auth import auth_register_v2
from src.auth import auth_login_v2
from src.auth import auth_logout_v1
from src.error import InputError
from src.other import clear_v1
from src.data import data

@pytest.fixture
def clear_data():
    clear_v1()
    
# Test for auth_register
def test_register_valid_email(clear_data):
    register = auth_register_v2("asdf@gmail.com", "12344545", "K","S")
    login = auth_login_v2("asdf@gmail.com", "12344545")
    assert register['auth_user_id'] == login['auth_user_id']
    
def test_register_invalid_email(clear_data):
    with pytest.raises(InputError):
        assert auth_register_v2("asdfgmail.com", "12344545", "K","S")
    
def test_register_email_unshared(clear_data):
    register1 = auth_register_v2("same@gmail.com", "12344545", "Me", "Me")
    register2 = auth_register_v2("Notsame@gmail.com", "12344545", "NotMe", "NotMe")
    assert register1['auth_user_id'] != register2['auth_user_id']

# Repeated
def test_register_email_shared(clear_data):
    auth_register_v2("same@gmail.com", "12344545", "Me", "Me")
    with pytest.raises(InputError):
        assert auth_register_v2("same@gmail.com", "12344545", "NotMe", "NotMe") is None

def test_check_password(clear_data): #less than 6 characters is a fail
    with pytest.raises(InputError):
        assert auth_register_v2("honey@outlook.com", "hi", "Tim", "Oreo")

def test_firstname_length(clear_data): # if firstname < 1 or >50 is a fail
    with pytest.raises(InputError):
        assert auth_register_v2("honey@outlook.com", "12345678", "", "Oreo")   

def test_lastname_length(clear_data): #if lastname < 1 or >50 is a fail
    with pytest.raises(InputError):
        assert auth_register_v2("honey@outlook.com", "12345678", "Tim", "")
# Tests for login    
def test_login_incorrect_password(clear_data):
    auth_register_v2("hiheee@gmail.com", "1234566", "K","S")
    with pytest.raises(InputError):
        assert auth_login_v2("hiheee@gmail.com", "1234666")
def test_login_correct_password(clear_data):
    register = auth_register_v2("hiheee@gmail.com", "1234455", "K","S")
    login = auth_login_v2("hiheee@gmail.com", "1234455")
    assert register['auth_user_id'] == login['auth_user_id']
def test_login_invalid_email(clear_data):
    auth_register_v2("hiheee@gmail.com", "1234455", "K","S")
    with pytest.raises(InputError):
        assert auth_login_v2("hiheeegmail", "1234455")
def test_login_incorrect_email(clear_data):
    auth_register_v2("hiheee@gmail.com", "1234455", "K","S")
    with pytest.raises(InputError):
        assert auth_login_v2("hiheee123gmail.com", "1234455")
#register handle
def test_handle_taken(clear_data):
    pass 
    
def test_handle_too_long(clear_data):
    pass
    
def test_handle_same(clear_data):
    pass

def test_handle_nospace(clear_data):
    pass

def test_handle_concatenate(clear_data):
    pass

##Tests for logout
def test_logout(clear_data):
    register = auth_register_v2("asdf@gmail.com", "12344545", "K","S")
    login = auth_login_v2("asdf@gmail.com", "12344545")
    result = auth_logout_v1(register['token'])
    assert result['is_success'] == True    
