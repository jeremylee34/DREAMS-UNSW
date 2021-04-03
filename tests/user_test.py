import pytest
import re
from src.auth import auth_register_v2
from src.user import user_profile_v2
from src.user import user_profile_setname_v2
from src.user import user_profile_setemail_v2
from src.user import user_profile_sethandle_v1
from src.user import users_all_v1
from src.error import InputError
from src.other import clear_v1
from src.data import data

@pytest.fixture
def clear_data():
    clear_v1()

##Tests for user_profile_v2
def test_invalid_uid(clear_data):
    register = auth_register_v2("asdf@gmail.com", "12344545", "K","S")
    with pytest.raises(InputError):
        assert user_profile_v2(register['token'], 2)

##Tests for user_profile_setname_v2
def test_invalid_firstname(clear_data):
    register = auth_register_v2("asdf@gmail.com", "12344545", "K","S")
    with pytest.raises(InputError):
        assert user_profile_setname_v2(register['token'], '', 'johnson')   

def test_invalid_lastname(clear_data):
    register = auth_register_v2("asdf@gmail.com", "12344545", "K","S")
    with pytest.raises(InputError):
        assert user_profile_setname_v2(register['token'], 'timothy', '')          

##Tests for user_profile_setemail_v2
def test_invalid_email(clear_data):
    register = auth_register_v2("asdf@gmail.com", "12344545", "K","S")
    with pytest.raises(InputError):
        assert user_profile_setemail_v2(register['token'], 'rob.com')     

def test_shared_email(clear_data):
    register1 = auth_register_v2("asdf@gmail.com", "12344545", "K","S")
    register2 = auth_register_v2("fish@gmail.com", "12344545", "fish","sea")
    with pytest.raises(InputError):
        assert user_profile_setemail_v2(register1['token'], 'fish@gmail.com')  

##Tests for user_profile_sethandle_v1
def test_invalid_handle(clear_data):
    register = auth_register_v2("asdf@gmail.com", "12344545", "K","S")
    with pytest.raises(InputError):
        assert user_profile_sethandle_v1(register['token'], 'jo') 

def test_shared_handle(clear_data):
    register1 = auth_register_v2("asdf@gmail.com", "12344545", "K","S")
    register2 = auth_register_v2("honey@yahoo.com", "12344545", "honey","bear")
    with pytest.raises(InputError):
        assert user_profile_sethandle_v1(register1['token'], 'honeybear')        

##Tests for users_all_v1
def test_all_users(clear_data):
    register1 = auth_register_v2("asdf@gmail.com", "12344545", "K","S")
    register2 = auth_register_v2("honey@yahoo.com", "12344545", "honey","bear")
    user_result = users_all_v1(register1['token'])
    assert len(user_result) == 2    