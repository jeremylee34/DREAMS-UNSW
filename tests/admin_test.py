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
from src.dm import dm_messages_v1
from src.message import message_send_v1
from src.message import message_senddm_v1
from src.data import data
from src.other import clear_v1
from src.error import InputError, AccessError

@pytest.fixture
def clear_data():
    '''
    Clears all user data
    '''
    clear_v1()

@pytest.fixture
def user_token1():
    '''
    Registers first user
    '''
    user_token1 = auth_register_v1("firstUser@gmail.com", "password", "Paras", "Mins")
    return user_token1

@pytest.fixture
def user_token2():
    '''
    Registers second user
    '''
    user_token2 = auth_register_v1("secondUser@gmail.com", "password", "Goyas", "Lsiwe")
    return user_token2

@pytest.fixture
def user_token3():
    '''
    Registers third user
    '''
    user_token3 = auth_register_v1("thirdUser@gmail.com", "password", "Taraa", "safba")
    return user_token3

########## test admin_user_remove_v1 ##########

def test_admin_remove(clear_data, user_token1, user_token2):
    '''
    Basic test for functionality of admin_userpermission_change_v1
    and admin_user_remove_v1
    '''
    admin_userpermission_change_v1(user_token1['token'], user_token2['auth_user_id'], 1)
    admin_user_remove_v1(user_token1['token'], user_token2['auth_user_id'])
    users = users_all_v1(user_token1['token'])
    assert len(users['users']) == 1
    assert users['users'][0]['u_id'] == user_token1['auth_user_id']

def test_admin_remove_input_error(clear_data, user_token1):
    '''
    Test if admin_remove_input has invalid input
    '''
    with pytest.raises(InputError):
        assert admin_user_remove_v1(user_token1['token'], 6)

def test_admin_remove_access_error(clear_data, user_token1, user_token2):
    '''
    Test if admin_remove_input has invalid access
    '''
    with pytest.raises(AccessError):
        assert admin_user_remove_v1(user_token2['token'], user_token1['auth_user_id'])

def test_admin_remove_invalid_token(clear_data, user_token1):
    '''
    Test if admin_remove_input has invalid token
    '''
    with pytest.raises(AccessError):
        assert admin_user_remove_v1('asdf', user_token1['auth_user_id'])

def test_admin_remove_user_is_the_only_owner(clear_data, user_token1):
    '''
    Test if admin_remove_input raise InputError("User is the only owner") 
    '''
    with pytest.raises(InputError):
        assert admin_user_remove_v1(user_token1['token'], user_token1['auth_user_id'])

def test_admin_remove_channel(clear_data, user_token1, user_token2, user_token3):
    '''
    Test if deleted user message in channel become 'Removed User'
    '''
    new_channel = channels_create_v1(user_token1['token'], "Public channel", True)
    channel_id = new_channel['channel_id']
    channel_join_v1(user_token1['token'], channel_id)
    channel_join_v1(user_token2['token'], channel_id)
    admin_userpermission_change_v1(user_token1['token'], user_token2['auth_user_id'], 1)
    admin_userpermission_change_v1(user_token1['token'], user_token3['auth_user_id'], 1)

    message_send_v1(user_token1['token'], channel_id, "Hello")
    message_send_v1(user_token2['token'], channel_id, "Bye byee")
    admin_user_remove_v1(user_token1['token'], user_token2['auth_user_id'])
    channel_msg = channel_messages_v1(user_token1['token'], channel_id, 0)

    assert channel_msg['messages'][0]['message'] == 'Removed user'

def test_admin_remove_invalid_uid(clear_data, user_token1):
    '''
    Test if input u_id is invalid
    '''
    with pytest.raises(InputError):
        admin_user_remove_v1(user_token1['token'], 78673456)
      
def test_admin_remove_dm(clear_data, user_token1, user_token2, user_token3):
    '''
    Test if deleted user message in dm become 'Removed User'
    '''
    u_ids = [ user_token2['auth_user_id'], user_token3['auth_user_id'] ]
    new_dm = dm_create_v1(user_token1['token'], u_ids)
    dm_id = new_dm['dm_id']

    admin_userpermission_change_v1(user_token1['token'], user_token2['auth_user_id'], 1)
    admin_userpermission_change_v1(user_token1['token'], user_token3['auth_user_id'], 1)
    message_senddm_v1(user_token2['token'], dm_id, "Hello")
    message_senddm_v1(user_token3['token'], dm_id, "Bye byee")

    dm_detail = dm_messages_v1(user_token2['token'], dm_id, 0)
    admin_user_remove_v1(user_token1['token'], user_token2['auth_user_id'])
    dm_detail = dm_messages_v1(user_token3['token'], dm_id, 0)

    assert dm_detail['messages'][1]['message'] == 'Removed user'

########## test admin_userpermission_change_v1 ##########

def test_admin_userpermission_permission_id(clear_data, user_token1, user_token2):
    '''
    Test if function raises AccessError('Permission_id is not valid') 
    '''
    with pytest.raises(AccessError):
        assert admin_userpermission_change_v1(user_token1['token'], user_token2['auth_user_id'], 3)

def test_admin_userpermission_invalid_token(clear_data, user_token1):
    '''
    Test if function raises AccessError('Invalid token') 
    '''
    with pytest.raises(AccessError):
        assert admin_userpermission_change_v1('asdf', user_token1['auth_user_id'], 1)

def test_admin_userpermission_error(clear_data, user_token1, user_token2):
    '''
    Test if admin_userpermission_change works
    '''
    admin_userpermission_change_v1(user_token1['token'], user_token2['auth_user_id'], 1)
    users = users_all_v1(user_token1['token'])
    assert users['users'][user_token2['auth_user_id']]['permission_id'] == 1

def test_admin_userpermission_input_error(clear_data, user_token1):
    '''
    Test if admin_userpermission_change has invalid input
    '''
    with pytest.raises(InputError):
        assert admin_userpermission_change_v1(user_token1['token'], 7, 1)

def test_admin_userpermission_access_error(clear_data, user_token1, user_token2):
    '''
    Test if admin_userpermission_change has invalid access
    '''
    with pytest.raises(AccessError):
        assert admin_userpermission_change_v1(user_token2['token'], user_token1['auth_user_id'], 2)
