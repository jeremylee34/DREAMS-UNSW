import pytest
import json
import requests
from src import config

"""
    STATUS_CODE
    200 = successful
    403 = AccessError
    400 = InputError
"""
def test_system():

#for user/profile/v2
"""
    InputError - user with u_id is not valid user
"""

#for user/profile/setname/v2
    #InputError - firstname is <1 or >50
    assert requests.put(config.url + 'user/profile/setname/v2', json = {
        'token': ''
        'name_first': '',
        'name_last': 'harry'
    }).status_code == 400     
    
    #InputError - lastname is <1 or >50
    assert requests.put(config.url + 'user/profile/setname/v2', json = {
        'token': ''
        'name_first': 'tom',
        'name_last': ''
    }).status_code == 400 
    

#for user/profile/setemail/v2
"""
    InputError - Email is already used by someone else    
"""
    #InputError - Invalid email
    assert requests.put(config.url + 'user/profile/setemail/v2', json = {
        'token': ''
        'email': 'tom_harry.com'
    }).status_code == 400 

#for user/profile/sethandle/v1
"""
    InputError - handle is already used by another user
"""
    #InputError - handle_str < 3 or > 20
    assert requests.put(config.url + 'user/profile/sethandle/v2', json = {
        'token': ''
        'handle': 'to'
    }).status_code == 400 

#users/all/v1
"""
    test by returning all users
"""
    r = requests.get(config.url + 'users/all/v1', json = {
        'token':''
    })
    payload = r.json()
    assert payload['users'] != ''
    assert requests.get(config.url + 'users/all/v1', json = {
        'token':''
    }).status_code == 400

#search/v2
"""
    return collection of messages
    InputError - query_str is > 1000
"""
    r = requests.get(config.url + 'search/v2', json = {
        'token':''
        'query_str':''
    })
    payload = r.json()
    assert payload['messages'] != ''
    assert requests.get(config.url + 'search/v2', json = {
        'token': ''
        'query_str': ''
    }).status_code == 400     

#admin/user/remove/v1
"""
    InputError - u_id does not refer to a valid user
    InputError - user is currently the only owner
    AccessError - authorised user is not an owner
"""
    r = requests.delete(config.url + 'admin/user/remove/v1', json = {
        'token':''
        'u_id':''
    })
    payload = r.json()
    assert payload == {}
    assert requests.get(config.url + 'admin/user/remove/v1', json = {
        'token':''
        'u_id':''
    }).status_code == 400     

#admin/userpermission/change/v1
"""
    InputError - u_id does not refer to a valid user
    InputError - permission_id does not refer to a value permission
    AccessError - authorised user is not an owner
"""
    r = requests.post(config.url + 'admin/userpermission/change/v1', json = {
            'token':''
            'u_id':''
            'permission_id':''
        })
        payload = r.json()
        assert payload == {}
        assert requests.get(config.url + 'admin/userpermission/change/v1', json = {
            'token':''
            'u_id':''
            'permission_id':''
        }).status_code == 400   


#notifications/get/v1
"""
    test for successful notifications
"""
    r = requests.get(config.url + 'admin/userpermission/change/v1', json = {
            'token':''
        })
        payload = r.json()
        assert payload != {}
        assert requests.get(config.url + 'admin/userpermission/change/v1', json = {
            'token':''
        }).status_code == 400   

#clear/v1
"""
    test for successful delete
"""
    assert requests.delete(config.url + '/clear/v1').status_code == 400
