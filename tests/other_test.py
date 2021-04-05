import pytest
from src.auth import auth_register_v1
from src.auth import auth_login_v1
from src.other import clear_v1
from src.data import data

@pytest.fixture
#Clears all data
def clear_data():
    clear_v1()

#Tests whether all the users and their information are deleted (successful implementation)
def test_clear(clear_data):
    auth_register_v1("asdf@gmail.com", "12344545", "K","S")
    auth_login_v1("asdf@gmail.com", "12344545")
    auth_login_v1("asdf@gmail.com", "12344545")
    auth_login_v1("asdf@gmail.com", "12344545")
    result = clear_v1()
    assert result == {}