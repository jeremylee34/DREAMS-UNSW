import pytest
import json
import requests
from src import config

#for user/profile/v2
"""
    InputError - user with u_id is not valid user
"""

#for user/profile/setname/v2
"""
    InputError - firstname is <1 or >50
    InputError - lastname is <1 or >50
"""

#for user/profile/setemail/v2
"""
    InputError - Invalid email
    InputError - Email is already used by someone else    
"""

#for user/profile/sethandle/v1
"""
    InputError - handle_str < 3 or > 20
    InputError - handle is already used by another user
"""

#users/all/v1
"""
    test by returning all users
"""

#search/v2
"""
    InputError - query_str is > 1000
"""

#admin/user/remove/v1
"""
    InputError - u_id does not refer to a valid user
    InputError - user is currently the only owner
    AccessError - authorised user is not an owner
"""

#admin/userpermission/change/v1
"""
    InputError - u_id does not refer to a valid user
    InputError - permission_id does not refer to a value permission
    AccessError - authorised user is not an owner
"""

