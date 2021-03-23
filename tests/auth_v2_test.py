import pytest
import json
import requests
from src import config

#for auth/login/v2
"""
    InputError - Invalid email
    InputError - Email entered doesn't belong to user
    InputError - Password is incorrect
"""

#for auth/register/v2
"""
    InputError - Invalid email
    InputError - Email is already used by someone else
    InputError - Password is less than 6 characters
    InputError - firstname is <1 or >50
    InputError - lastname is <1 or >50
"""

#auth/login/v1
"""
    tests for successful logout
"""