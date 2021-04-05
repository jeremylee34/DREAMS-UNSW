import requests
import pytest
from src import config
import src.auth
import src.user
import src.other
import src.data
from src.error import InputError, AccessError

@pytest.fixture
def clear_data():
    requests.delete(config.url + 'clear/v1')

def test_search_v2(clear_data):
    user1 = requests.post(config.url + 'auth/register/v2', json = {
        'email': 'ska@gmail.com',
        'password': '1234aaaaaa',
        'name_first': 'Tom',
        'name_last': 'Diaaa',
    })
    #join server
    
    #send message

    payload = user1.json()
    requests.get(config.url + 'search/v1', json = {
        'token': 'skadi@gmail.com',
        'query_str': '1234aaaaaa',
    })

def test_notifications_get(clear_data):
    user1 = requests.post(config.url + 'auth/register/v2', json = {
        'email': 'ska@gmail.com',
        'password': '1234aaaaaa',
        'name_first': 'Tom',
        'name_last': 'Diaaa',
    })
    payload = user1.json()
    requests.get(config.url + 'search/v1', json = {
        'token': payload['token'],
    })