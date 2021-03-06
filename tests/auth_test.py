import pytest
import re
from src.auth import auth_login_v1
from src.auth import auth_register_v1
from src.error import InputError
from src.other import clear_v1
from src.data import data

@pytest.fixture
def clear_data():
    clear_v1()
    
def test_login_incorrect_password(clear_data):
    auth_register_v1("hiheee@gmail.com", "1234566", "K","S")
    with pytest.raises(InputError):
        assert auth_login_v1("hiheee@gmail.com", "1234666")


def test_login_correct_password(clear_data):
    auth_user_id1 = auth_register_v1("hiheee@gmail.com", "1234455", "K","S")
    auth_user_id2 = auth_login_v1("hiheee@gmail.com", "1234455")
    assert auth_user_id1 == auth_user_id2


#test for auth_register
def test_register_valid_email(clear_data):
    auth_user_id1 = auth_register_v1("asdf@gmail.com", "12344545", "K","S")
    auth_user_id2 = auth_login_v1("asdf@gmail.com", "12344545")
    assert auth_user_id1 == auth_user_id2
    
def test_register_invalid_email(clear_data):
    with pytest.raises(InputError):
        assert auth_register_v1("asdfgmail.com", "12344545", "K","S")
    
def test_register_email_unshared(clear_data):
    auth_user_id1 = auth_register_v1("same@gmail.com", "12344545", "Me", "Me")
    auth_user_id2 = auth_register_v1("Notsame@gmail.com", "12344545", "NotMe", "NotMe")
    assert(auth_user_id1 != auth_user_id2)

#repeated
def test_register_email_shared(clear_data):
    auth_register_v1("same@gmail.com", "12344545", "Me", "Me")
    with pytest.raises(InputError):
        assert auth_register_v1("same@gmail.com", "12344545", "NotMe", "NotMe") is None


def check_password_test(clear_data): #less than 6 characters is a fail
    with pytest.raises(InputError):
        assert auth_register_v1("honey@outlook.com", "hi", "Tim", "Oreo")

def firstname_length_test(clear_data): # if firstname < 1 or >50 is a fail
    with pytest.raises(InputError):
        assert auth_register_v1("honey@outlook.com", "hi", "", "Oreo")   

def lastname_length_test(clear_data): #if lastname < 1 or >50 is a fail
    with pytest.raises(InputError):
        assert auth_register_v1("honey@outlook.com", "hi", "Tim", "")
    
#register handle
def test_handle_taken(clear_data):
    auth_register_v1("roland@gmail.com", "1234567", "Roland", "Lin")
    auth_register_v1("roland1@gmail.com", "1234567", "Roland", "Lin")
    assert data['users'][0]['handle'] == 'rolandlin'
    assert data['users'][1]['handle'] == 'rolandlin0'
    
def test_handle_too_long(clear_data):
    auth_register_v1("roland@gmail.com", "1234567", "Roland", "Linisverycool123")
    assert data['users'][0]['handle'] == 'rolandlinisverycool1'
def test_handle_same(clear_data):
    pass
def test_handle_nospace(clear_data):
    pass

def test_handle_concatenate(clear_data):
    auth_register_v1("roland1@gmail.com", "1234567", "Roland", "Linisverycoolasd") #22lettershandle    
    auth_register_v1("roland2@gmail.com", "1234567", "Roland", "Linisverycoolasd")    
    auth_register_v1("roland3@gmail.com", "1234567", "Roland", "Linisverycoolasd")    
    auth_register_v1("roland4@gmail.com", "1234567", "Roland", "Linisverycoolasd")    
    auth_register_v1("roland5@gmail.com", "1234567", "Roland", "Linisverycoolasd")    
    auth_register_v1("roland6@gmail.com", "1234567", "Roland", "Linisverycoolasd")    
    auth_register_v1("roland7@gmail.com", "1234567", "Roland", "Linisverycoolasd")    
    auth_register_v1("roland8@gmail.com", "1234567", "Roland", "Linisverycoolasd")    
    auth_register_v1("roland9@gmail.com", "1234567", "Roland", "Linisverycoolasd")    
    auth_register_v1("roland0@gmail.com", "1234567", "Roland", "Linisverycoolasd")    
    auth_register_v1("roland12a@gmail.com", "1234567", "Roland","Linisverycoolasd")
    auth_register_v1("roland1s@gmail.com", "1234567", "Roland", "Linisverycoolasd") #22lettershandle    
    auth_register_v1("roland2d@gmail.com", "1234567", "Roland", "Linisverycoolasd")    
    auth_register_v1("roland3f@gmail.com", "1234567", "Roland", "Linisverycoolasd")    
    auth_register_v1("roland4aa@gmail.com", "1234567", "Roland", "Linisverycoolasd")    
    auth_register_v1("roland5ss@gmail.com", "1234567", "Roland", "Linisverycoolasd")    
    auth_register_v1("roland6dd@gmail.com", "1234567", "Roland", "Linisverycoolasd")    
    auth_register_v1("roland7ff@gmail.com", "1234567", "Roland", "Linisverycoolasd")    
    auth_register_v1("roland8aaa@gmail.com", "1234567", "Roland", "Linisverycoolasd")    
    auth_register_v1("roland9sss@gmail.com", "1234567", "Roland", "Linisverycoolasd")    
    
    assert data['users'][0]['handle'] == 'rolandlinisverycoola'
    assert data['users'][1]['handle'] == 'rolandlinisverycool0'
    assert data['users'][2]['handle'] == 'rolandlinisverycool1'
    assert data['users'][3]['handle'] == 'rolandlinisverycool2' 
    assert data['users'][4]['handle'] == 'rolandlinisverycool3'
    assert data['users'][5]['handle'] == 'rolandlinisverycool4' 
    assert data['users'][6]['handle'] == 'rolandlinisverycool5'
    assert data['users'][7]['handle'] == 'rolandlinisverycool6' 
    assert data['users'][8]['handle'] == 'rolandlinisverycool7' 
    assert data['users'][9]['handle'] == 'rolandlinisverycool8' 
    assert data['users'][10]['handle'] =='rolandlinisverycool9' 
    assert data['users'][11]['handle'] =='rolandlinisverycoo10' 
    assert data['users'][12]['handle'] =='rolandlinisverycoo11' 
    assert data['users'][13]['handle'] =='rolandlinisverycoo12' 
    assert data['users'][14]['handle'] =='rolandlinisverycoo13' 
    assert data['users'][15]['handle'] =='rolandlinisverycoo14' 
    assert data['users'][16]['handle'] =='rolandlinisverycoo15' 
    assert data['users'][17]['handle'] =='rolandlinisverycoo16' 
    assert data['users'][18]['handle'] =='rolandlinisverycoo17' 
    assert data['users'][19]['handle'] =='rolandlinisverycoo18' 
