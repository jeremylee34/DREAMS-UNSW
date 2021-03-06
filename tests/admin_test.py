import pytest
import re
from src.admin import admin_user_remove_v1
from src.admin import admin_userpermission_change_v1
from src.auth import auth_register_v1
from src.user import users_all_v1
from src.channel import channel_messages_v1
from src.channel import channel_join_v1
from src.channels import channels_create_v1
from src.dm import dm_create_v1
from src.message import message_send_v1
from src.message import message_senddm_v1

from src.other import clear_v1
from src.error import InputError, AccessError
from src.data import data

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

def test_admin_remove_invalid_token(clear_data):
    '''
    Test if admin_remove_input has invalid token
    '''
    user2 = auth_register_v1('Kanit@gmail.com', '12345678', 'Kanit', 'Liang')
    with pytest.raises(AccessError):
        assert admin_user_remove_v1('asdf', user2['auth_user_id'])

def test_admin_remove_user_is_the_only_owner(clear_data):
    '''
    Test if admin_remove_input raise InputError("User is the only owner") 
    '''
    user = auth_register_v1('gordon@gmail.com', '12345678', 'Gordon', 'Liang')
    with pytest.raises(InputError):
        assert admin_user_remove_v1(user['token'], user['auth_user_id'])

def test_admin_remove_channel(clear_data):
    '''
    Test if deleted user message in channel become 'Removed User'
    '''
    user = auth_register_v1('gordon@gmail.com', '12345678', 'Gordon', 'Liang')
    user2 = auth_register_v1('Kanit@gmail.com', '12345678', 'Kanit', 'Liang')
    user3 = auth_register_v1('asdf@gmail.com', '12345678', 'Lop', 'Ang')
    new_channel = channels_create_v1(user['token'], "Public channel", True)
    channel_id = new_channel['channel_id']

    channel_join_v1(user['token'], channel_id)
    channel_join_v1(user2['token'], channel_id)
    channel_join_v1(user3['token'], channel_id)

    admin_userpermission_change_v1(user['token'], user2['auth_user_id'], 1)
    admin_userpermission_change_v1(user['token'], user3['auth_user_id'], 1)
    message_send_v1(user2['token'], channel_id, "Hello")
    message_send_v1(user3['token'], channel_id, "Bye byee")

    admin_user_remove_v1(user['token'], user2['auth_user_id'])
    
    assert data['channels'][channel_id]['messages'][1]['u_id'] == user2['auth_user_id'] 
    assert data['channels'][channel_id]['messages'][1]['message'] == 'Removed user'
    assert data['channels'][channel_id]['messages'][0]['message'] == 'Bye byee'

def test_admin_remove_dm(clear_data):
    '''
    Test if deleted user message in dm become 'Removed User'
    '''
    user = auth_register_v1('gordon@gmail.com', '12345678', 'Gordon', 'Liang')
    user2 = auth_register_v1('Kanit@gmail.com', '12345678', 'Kanit', 'Liang')
    user3 = auth_register_v1('asdf@gmail.com', '12345678', 'Lop', 'Ang')
    u_ids = [ user2['auth_user_id'], user3['auth_user_id'] ]
    new_dm = dm_create_v1(user['token'], u_ids)
    dm_id = new_dm['dm_id']

    admin_userpermission_change_v1(user['token'], user2['auth_user_id'], 1)
    admin_userpermission_change_v1(user['token'], user3['auth_user_id'], 1)
    message_senddm_v1(user2['token'], dm_id, "Hello")
    message_senddm_v1(user3['token'], dm_id, "Bye byee")

    admin_user_remove_v1(user['token'], user2['auth_user_id'])
    
    assert data['dms'][dm_id]['messages'][1]['u_id'] == user2['auth_user_id'] 
    assert data['dms'][dm_id]['messages'][1]['message'] == 'Removed user'
    assert data['dms'][dm_id]['messages'][0]['message'] == 'Bye byee'

def test_admin_userpermission_permission_id(clear_data):
    '''
    Test if function raises AccessError('Permission_id is not valid') 
    '''
    user = auth_register_v1('gordon@gmail.com', '12345678', 'Gordon', 'Liang')
    user2 = auth_register_v1('Kanit@gmail.com', '12345678', 'Kanit', 'Liang')
    with pytest.raises(AccessError):
        assert admin_userpermission_change_v1(user['token'], user2['auth_user_id'], 3)

def test_admin_userpermission_invalid_token(clear_data):
    '''
    Test if function raises AccessError('Invalid token') 
    '''
    user2 = auth_register_v1('Kanit@gmail.com', '12345678', 'Kanit', 'Liang')
    with pytest.raises(AccessError):
        assert admin_userpermission_change_v1('asdf', user2['auth_user_id'], 1)

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
