import pytest

from src.auth import auth_login_v1
from src.auth import auth_register_v1
from src.error import InputError

def test_auth_login_v1():
    assert auth_login_v1(tim@gmail.com, 1234) == 1

def test_auth_register_v1():
    assert auth_register_v1(tim@gmail.com, 1234, Tim, Smith).values() == 1