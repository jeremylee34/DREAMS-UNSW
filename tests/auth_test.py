import pytest
import re
from src.auth import auth_login_v1
from src.auth import auth_register_v1
from src.error import InputError
from src.other import clear_v1
from src.data import data

@pytest.fixture
def clear_data():
    clear_v1()
    
def test_login_incorrect_password(clear_data):
    auth_register_v1("hiheee@gmail.com", "1234566", "K","S")
    with pytest.raises(InputError):
        assert auth_login_v1("hiheee@gmail.com", "1234666")


def test_login_correct_password(clear_data):
    auth_user_id1 = auth_register_v1("hiheee@gmail.com", "1234455", "K","S")
    auth_user_id2 = auth_login_v1("hiheee@gmail.com", "1234455")
    assert auth_user_id1 == auth_user_id2

#test for auth_register
def test_register_valid_email(clear_data):
    auth_user_id1 = auth_register_v1("asdf@gmail.com", "12344545", "K","S")
    auth_user_id2 = auth_login_v1("asdf@gmail.com", "12344545")
    assert auth_user_id1 == auth_user_id2
    
def test_register_invalid_email(clear_data):
    with pytest.raises(InputError):
        assert auth_register_v1("asdfgmail.com", "12344545", "K","S")
    
def test_register_email_unshared(clear_data):
    auth_user_id1 = auth_register_v1("same@gmail.com", "12344545", "Me", "Me")
    auth_user_id2 = auth_register_v1("Notsame@gmail.com", "12344545", "NotMe", "NotMe")
    assert(auth_user_id1 != auth_user_id2)

#repeated
def test_register_email_shared(clear_data):
    auth_register_v1("same@gmail.com", "12344545", "Me", "Me")
    with pytest.raises(InputError):
        assert auth_register_v1("same@gmail.com", "12344545", "NotMe", "NotMe") is None

def check_password_test(clear_data): #less than 6 characters is a fail
    with pytest.raises(InputError):
        assert auth_register_v1("honey@outlook.com", "hi", "Tim", "Oreo")

def firstname_length_test(clear_data): # if firstname < 1 or >50 is a fail
    with pytest.raises(InputError):
        assert auth_register_v1("honey@outlook.com", "hi", "", "Oreo")   

def lastname_length_test(clear_data): #if lastname < 1 or >50 is a fail
    with pytest.raises(InputError):
        assert auth_register_v1("honey@outlook.com", "hi", "Tim", "")
    
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