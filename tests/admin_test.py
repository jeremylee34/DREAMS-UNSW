import pytest
import re
from src.admin import admin_user_remove_v1
from src.admin import admin_userpermission_change_v1
from src.auth import auth_register_v1
from src.user import users_all_v1

from src.other import clear_v1
from src.error import InputError, AccessError

@pytest.fixture
def clear_data():
    '''
    Clears data in data file
    '''
    clear_v1()

def test_admin_remove(clear_data):
    '''
    Basic test for functionality of admin_userpermission_change_v1
    and admin_user_remove_v1
    '''
    user = auth_register_v1('gordon@gmail.com', '12345678', 'Gordon', 'Liang')
    user2 = auth_register_v1('Kanit@gmail.com', '12345678', 'Kanit', 'Liang')
    admin_userpermission_change_v1(user['token'], user2['auth_user_id'], 1)
    admin_user_remove_v1(user['token'], user2['auth_user_id'])
    users = users_all_v1(user['token'])
    assert len(users['users']) == 1
    assert users['users'][0]['u_id'] == user['auth_user_id']

def test_admin_remove_input_error(clear_data):
    '''
    Test if admin_remove_input has invalid input
    '''
    user = auth_register_v1('gordon@gmail.com', '12345678', 'Gordon', 'Liang')
    with pytest.raises(InputError):
        assert admin_user_remove_v1(user['token'], 6)

def test_admin_remove_access_error(clear_data):
    '''
    Test if admin_remove_input has invalid access
    '''
    user = auth_register_v1('gordon@gmail.com', '12345678', 'Gordon', 'Liang')
    user2 = auth_register_v1('Kanit@gmail.com', '12345678', 'Kanit', 'Liang')
    with pytest.raises(AccessError):
        assert admin_user_remove_v1(user2['token'], user['auth_user_id'])

def test_admin_userpermission_error(clear_data):
    '''
    Test if admin_userpermission_change works
    '''
    user = auth_register_v1('gordon@gmail.com', '12345678', 'Gordon', 'Liang')
    user2 = auth_register_v1('Kanit@gmail.com', '12345678', 'Kanit', 'Liang')
    admin_userpermission_change_v1(user['token'], user2['auth_user_id'], 1)
    users = users_all_v1(user['token'])
    assert users['users'][user2['auth_user_id']]['permission_id'] == 1

def test_admin_userpermission_input_error(clear_data):
    '''
    Test if admin_userpermission_change has invalid input
    '''
    user = auth_register_v1('gordon@gmail.com', '12345678', 'Gordon', 'Liang')
    with pytest.raises(InputError):
        assert admin_userpermission_change_v1(user['token'], 7, 1)

def test_admin_userpermission_access_error(clear_data):
    '''
    Test if admin_userpermission_change has invalid access
    '''
    user = auth_register_v1('gordon@gmail.com', '12345678', 'Gordon', 'Liang')
    user2 = auth_register_v1('Kanit@gmail.com', '12345678', 'Kanit', 'Liang')
    with pytest.raises(AccessError):
        assert admin_userpermission_change_v1(user2['token'], user['auth_user_id'], 2)
