#Import pytest
import pytest 

#Import functions from dm for testing
from src.dm import dm_details_v1
from src.dm import dm_list_v1
from src.dm import dm_create_v1
from src.dm import dm_remove_v1
from src.auth import auth_register_v1
from src.user import user_profile_v1

#Import error from src
from src.error import InputError
from src.error import AccessError

#Import other from src
from src.other import clear_v1
import src.data

#Make fixtures
@pytest.fixture
def user_token1():
    user_token1 = auth_register_v1("Godan@gmail.com", "password", "Godan", "Liang")
    return user_token1
    
@pytest.fixture
def user_token2():
    user_token2 = auth_register_v1("Jeremy@gmail.com", "password", "Jeremy", "Lee")
    return user_token2
    
@pytest.fixture
def user_token3():
    user_token3 = auth_register_v1("Roland@gmail.com", "password", "Roland", "Lin")
    return user_token3

@pytest.fixture
def dm_1(user_token1, user_token2, user_token3):
    u_ids = [user_token2['auth_user_id'], user_token3['auth_user_id']]  
    dm_1 = dm_create_v1(user_token1['token'], u_ids)
    return dm_1

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
        assert dm_create_v1(user_token1['token'], 1000)

def test_dm_create_v1_simple(clear_data, user_token1, user_token2, user_token3):
    """
    Testing whether dm_create_v1 returns the correct dm_id and dm_name
    """
    u_ids = [user_token2['auth_user_id'], user_token3['auth_user_id']]  
    dm_1 = dm_create_v1(user_token1['token'], u_ids)
    assert dm_1['dm_id'] == 1
    user_profile_dict1 = user_profile_v1(user_token1['token'], user_token1['auth_user_id'])
    handle1 = user_profile_dict1['handle_str']
    user_profile_dict2 = user_profile_v1(user_token2['token'], user_token2['auth_user_id'])
    handle2 = user_profile_dict2['handle_str']
    user_profile_dict3 = user_profile_v1(user_token3['token'], user_token3['auth_user_id'])
    handle3 = user_profile_dict3['handle_str']
    assert dm_1['dm_name'] == f"{handle1}, {handle2}, {handle3}"

def test_dm_create_v1_ownership(clear_data, user_token1):
    """
    Testing whether dm_create_v1 sets the owner correctly
    """
    u_ids = [user_token2['auth_user_id'], user_token3['auth_user_id']]  
    dm_1 = dm_create_v1(user_token1['token'], u_ids)
    user_profile_dict1 = user_profile_v1(user_token1['token'], user_token1['auth_user_id'])
    user_u_id = user_profile_dict1['u_id']
    assert dm_1['owner'] == user_u_id

def test_dm_details_v1_simple(clear_data, user_token1, user_token2, user_token3, dm_1):
    """
    Testing whether dm_details_v1 returns the correct name and members
    """
    dm_details = dm_details_v1(user_token1['token'], dm_1['dm_id'])
    user_profile_dict1 = user_profile_v1(user_token1['token'], user_token1['auth_user_id'])
    handle1 = user_profile_dict1['handle_str']
    user_profile_dict2 = user_profile_v1(user_token2['token'], user_token2['auth_user_id'])
    handle2 = user_profile_dict2['handle_str']
    user_profile_dict3 = user_profile_v1(user_token3['token'], user_token3['auth_user_id'])
    handle3 = user_profile_dict3['handle_str']
    assert dm_details['name'] == f"{handle1}, {handle2}, {handle3}"
    assert dm_details['members'][0] == user_profile_dict1
    assert dm_details['members'][1] == user_profile_dict2
    assert dm_details['members'][2] == user_profile_dict3
    
def test_dm_details_v1_simple