import pytest
import re
from src.other import search_v1
from src.other import notifications_get_v1
from src.auth import auth_register_v1
from src.channels import channels_create_v1
from src.message import message_send_v1
from src.other import clear_v1
from src.error import InputError, AccessError
from src.data import data

@pytest.fixture
def clear_data():
    clear_v1()

#test search
def test_search_v1(clear_data):
    user = auth_register_v1('gordon@gmail.com', '12345678', 'Gordon', 'Liang')
    channel_info = channels_create_v1(user['token'], 'Channel1', True)
    message_send_v1(user['token'], channel_info['channel_id'], 'Hello')
    assert search_v1(user['token'], 'Hello')
    
def test_search_v1_input_error(clear_data):
    user = auth_register_v1('gordon@gmail.com', '12345678', 'Gordon', 'Liang')
    channel_info = channels_create_v1(user['token'], 'Channel1', True)
    message_send_v1(user['token'], channel_info['channel_id'], 'Hello')
    with pytest.raises(InputError):
        assert search_v1(user['token'], 'Hello' * 1000)

#test notifications
def test_notifications_get(clear_data):
    user = auth_register_v1('gordon@gmail.com', '12345678', 'Gordon', 'Liang')
    notification = notifications_get_v1(user['token'])
    assert len(notification['notifications']) < 20


