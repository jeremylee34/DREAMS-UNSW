import pytest
import re
from src.user import admin_user_remove
from src.user import admin_userpermission_change_v1
from src.other import clear_v1
from src.other import search_v2
from src.other import notifications_get

from src.error import InputError, AccessError
from src.data import data

@pytest.fixture
def clear_data():
    clear_v1()

