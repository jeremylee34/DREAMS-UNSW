import pytest

from src.auth import auth_login_v1
from src.auth import auth_register_v1
from src.error import InputError
from tests.auth_info import users

#tests for auth_login
def test_login_invalid_email():
    pass

def test_login_valid_email():
    pass

def test_email_unshared():
    pass

def test_email_shared():
    pass

def test_incorrect_password():
    pass

def test_correct_password():
    pass


#test for auth_register
def test_update():
    print(users["user1"]["password"])
    pass