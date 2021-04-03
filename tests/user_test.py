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

def test_profile_success(clear_data):
    register = auth_register_v2("asdf@gmail.com", "12344545", "K","S")
    profile = user_profile_v2(register['token'], 0)
    assert register['auth_user_id'] == profile['u_id']

##Tests for user_profile_setname_v2
def test_invalid_firstname(clear_data):
    register = auth_register_v2("asdf@gmail.com", "12344545", "K","S")
    with pytest.raises(InputError):
        assert user_profile_setname_v2(register['token'], '', 'johnson')   

def test_invalid_lastname(clear_data):
    register = auth_register_v2("asdf@gmail.com", "12344545", "K","S")
    with pytest.raises(InputError):
        assert user_profile_setname_v2(register['token'], 'timothy', '') 

def test_profile_setname_success(clear_data):
    register = auth_register_v2("asdf@gmail.com", "12344545", "K","S")
    result1 = user_profile_v2(register['token'], 0)
    setname = user_profile_setname_v2(register['token'], 'timothy', 'smith')
    result2 = user_profile_v2(register['token'], 0)
    assert result1['name_first'] != result2['name_first'] and result1['name_last'] != result2['name_last']

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

def test_profile_email_success(clear_data):
    register = auth_register_v2("asdf@gmail.com", "12344545", "K","S")
    result1 = user_profile_v2(register['token'], 0)
    setemail = user_profile_setemail_v2(register['token'], 'tom@gmail.com')
    result2 = user_profile_v2(register['token'], 0)
    assert result1['email'] != result2['email']

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

def test_profile_sethandle_success(clear_data):    
    register = auth_register_v2("asdf@gmail.com", "12344545", "K","S")
    result1 = user_profile_v2(register['token'], 0)
    sethandle = user_profile_sethandle_v1(register['token'], 'hello')
    result2 = user_profile_v2(register['token'], 0)
    assert result1['handle'] != result2['handle']

##Tests for users_all_v1
def test_all_users(clear_data):
    register1 = auth_register_v2("asdf@gmail.com", "12344545", "K","S")
    register2 = auth_register_v2("honey@yahoo.com", "12344545", "honey","bear")
    user_result = users_all_v1(register1['token'])
    assert len(user_result) == 2    