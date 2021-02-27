import pytest

from src.auth import auth_login_v1
from src.auth import auth_register_v1
from src.error import InputError

#tests for auth_login
def test_login_invalid_email():
    with pytest.raises(Exception):
        auth_login_v1("fafasf@gmail.com", "asdf1234@") == "user_1"
    with pytest.raises(Exception):
        auth_login_v1("asd@gmail.com", "asdfasf1234@") == "user_2"
    with pytest.raises(Exception):
        auth_login_v1("2424ssss@gmail.com", "asasfdf1234@") == "user_3"
    with pytest.raises(Exception):
        auth_login_v1("42542552@gmail.com", "asdasff1234@") == "user_4"

def test_login_valid_email():
    assert ("asdfg.com", "a2sdf" == "invalid mail")
    assert ("asdfg@gmailcom", "as2df" == "invalid mail")    
    assert ("asdfgcom", "asdssf" == "invalid mail")    
    assert ("asdfg@com", "asaadf" == "invalid mail")        

def test_login_email_unshared():
    pass

#def test_login_email_shared():
    #pass

def test_login_incorrect_password():
    pass

#def test_login_correct_password():
    #pass


#test for auth_register
def test_register_invalid_email():
    pass

def test_register_valid_email():
    pass

def test_register_email_unshared():
    pass

def test_register_email_shared():
    pass

def check_password(): #less than 6 characters is a fail
    pass

def firstname_length(): # if firstname < 1 or >50 is a fail
    pass

def lastname_length(): #if lastname < 1 or >50 is a fail
    pass