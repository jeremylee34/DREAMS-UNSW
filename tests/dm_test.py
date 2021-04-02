#Import pytest
import pytest 

#Import functions from dm for testing
from src.dm import dm_details_v1
from src.dm import dm_list_v1
from src.dm import dm_create_v1
from src.dm import dm_remove_v1
from src.auth import auth_register_v1

#Import error from src
from src.error import InputError
from src.error import AccessError

#Import other from src
from src.other import clear_v1
import src.data

#Make fixtures
@pytest.fixture
def user_token1():
    user_token1 = auth_register_v1("Roland@gmail.com", "password", "Roland", "Lin")
    return user_token1
    
@pytest.fixture
def user_token2():
    user_token2 = auth_register_v1("Godan@gmail.com", "password", "Godan", "Liang")
    return user_token2
    
@pytest.fixture
def user_token3():
    user_token3 = auth_register_v1("Jeremy@gmail.com", "password", "Jeremy", "Lee")
    return user_token3

#Fixture for clear to prevent clearing of other fixtures
@pytest.fixture
def clear_data():
    clear_v1()

################################################################################
################################################################################
################################################################################

def test_dm_create_v1_input_error(clear_data, user_token1):
    """
    InputError to be thrown when u_id does not refer to valid user
    """
    with pytest.raises(InputError):
        assert dm_create_v1(user_token1, 1000)

def test_dm_create_v1_simple(clear_data, user_token1, user_token2, user_token3):
    u_ids = []
    dm_create_v1(user_token1, )


def test_dm_details_v1_input_error(clear_data, user_token1):
