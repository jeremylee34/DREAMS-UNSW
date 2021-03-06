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
    auth_register_v1("roland0dddd@gmail.com", "1234567", "Roland", "Linisverycoolasd")    
    auth_register_v1("roland12fff@gmail.com", "1234567", "Roland","Linisverycoolasd")
    auth_register_v1("roland1q@gmail.com", "1234567", "Roland", "Linisverycoolasd") #22lettershandle    
    auth_register_v1("roland2w@gmail.com", "1234567", "Roland", "Linisverycoolasd")    
    auth_register_v1("roland3e@gmail.com", "1234567", "Roland", "Linisverycoolasd")    
    auth_register_v1("roland4r@gmail.com", "1234567", "Roland", "Linisverycoolasd")    
    auth_register_v1("roland5qq@gmail.com", "1234567", "Roland", "Linisverycoolasd")    
    auth_register_v1("roland6ww@gmail.com", "1234567", "Roland", "Linisverycoolasd")    
    auth_register_v1("roland7ee@gmail.com", "1234567", "Roland", "Linisverycoolasd")    
    auth_register_v1("roland8rr@gmail.com", "1234567", "Roland", "Linisverycoolasd")    
    auth_register_v1("roland9qwer@gmail.com", "1234567", "Roland", "Linisverycoolasd")    
    auth_register_v1("roland0rewq@gmail.com", "1234567", "Roland", "Linisverycoolasd")    
    auth_register_v1("roland12zxcv@gmail.com", "1234567", "Roland","Linisverycoolasd")  
    auth_register_v1("roland1@g1mail.com", "1234567", "Roland", "Linisverycoolasd") #22lettershandle    
    auth_register_v1("roland2@g2mail.com", "1234567", "Roland", "Linisverycoolasd")    
    auth_register_v1("roland3@g3mail.com", "1234567", "Roland", "Linisverycoolasd")    
    auth_register_v1("roland4@g4mail.com", "1234567", "Roland", "Linisverycoolasd")    
    auth_register_v1("roland5@g5mail.com", "1234567", "Roland", "Linisverycoolasd")    
    auth_register_v1("roland6@g6mail.com", "1234567", "Roland", "Linisverycoolasd")    
    auth_register_v1("roland7@g7mail.com", "1234567", "Roland", "Linisverycoolasd")    
    auth_register_v1("roland8@g8mail.com", "1234567", "Roland", "Linisverycoolasd")    
    auth_register_v1("roland9@g9mail.com", "1234567", "Roland", "Linisverycoolasd")    
    auth_register_v1("roland0@g0mail.com", "1234567", "Roland", "Linisverycoolasd")    
    auth_register_v1("roland12a@11gmail.com", "1234567", "Roland","Linisverycoolasd")
    auth_register_v1("roland1s@22gmail.com", "1234567", "Roland", "Linisverycoolasd") #22lettershandle    
    auth_register_v1("roland2d@33gmail.com", "1234567", "Roland", "Linisverycoolasd")    
    auth_register_v1("roland3f@44gmail.com", "1234567", "Roland", "Linisverycoolasd")    
    auth_register_v1("roland4aa@55gmail.com", "1234567", "Roland", "Linisverycoolasd")    
    auth_register_v1("roland5ss@66gmail.com", "1234567", "Roland", "Linisverycoolasd")    
    auth_register_v1("roland6dd@77gmail.com", "1234567", "Roland", "Linisverycoolasd")    
    auth_register_v1("roland7ff@88gmail.com", "1234567", "Roland", "Linisverycoolasd")    
    auth_register_v1("roland8aaa@99gmail.com", "1234567", "Roland", "Linisverycoolasd")    
    auth_register_v1("roland9sss@00gmail.com", "1234567", "Roland", "Linisverycoolasd")    
    auth_register_v1("roland0dddd@111gmail.com", "1234567", "Roland", "Linisverycoolasd")    
    auth_register_v1("roland12fff@111gmail.com", "1234567", "Roland","Linisverycoolasd")
    auth_register_v1("roland1q@111gmail.com", "1234567", "Roland", "Linisverycoolasd") #22lettershandle    
    auth_register_v1("roland2w@111gmail.com", "1234567", "Roland", "Linisverycoolasd")    
    auth_register_v1("roland3e@111gmail.com", "1234567", "Roland", "Linisverycoolasd")    
    auth_register_v1("roland4r@gamail.com", "1234567", "Roland", "Linisverycoolasd")    
    auth_register_v1("roland5qq@gamail.com", "1234567", "Roland", "Linisverycoolasd")    
    auth_register_v1("roland6ww@gmaail.com", "1234567", "Roland", "Linisverycoolasd")    
    auth_register_v1("roland7ee@gmaail.com", "1234567", "Roland", "Linisverycoolasd")    
    auth_register_v1("roland8rr@gmaial.com", "1234567", "Roland", "Linisverycoolasd")    
    auth_register_v1("roland9qwer@gmaail.com", "1234567", "Roland", "Linisverycoolasd")    
    auth_register_v1("roland0rewq@gmafil.com", "1234567", "Roland", "Linisverycoolasd")    
    auth_register_v1("roland12zxcv@gmgail.com", "1234567", "Roland","Linisverycoolasd")  
    auth_register_v1("roland1@gmailg.com", "1234567", "Roland", "Linisverycoolasd") #22lettershandle    
    auth_register_v1("roland2@gmailg.com", "1234567", "Roland", "Linisverycoolasd")    
    auth_register_v1("roland3@gmailg.com", "1234567", "Roland", "Linisverycoolasd")    
    auth_register_v1("roland4@gmailg.com", "1234567", "Roland", "Linisverycoolasd")    
    auth_register_v1("roland5@gmailg.com", "1234567", "Roland", "Linisverycoolasd")    
    auth_register_v1("roland6@gmailg.com", "1234567", "Roland", "Linisverycoolasd")    
    auth_register_v1("roland7@gmailg.com", "1234567", "Roland", "Linisverycoolasd")    
    auth_register_v1("roland8@gmailg.com", "1234567", "Roland", "Linisverycoolasd")    
    auth_register_v1("roland9@gmailg.com", "1234567", "Roland", "Linisverycoolasd")    
    auth_register_v1("roland0@gmailg.com", "1234567", "Roland", "Linisverycoolasd")    
    auth_register_v1("roland12a@gmagil.com", "1234567", "Roland","Linisverycoolasd")
    auth_register_v1("roland1s@gmaigl.com", "1234567", "Roland", "Linisverycoolasd") #22lettershandle    
    auth_register_v1("roland2d@gmaigl.com", "1234567", "Roland", "Linisverycoolasd")    
    auth_register_v1("roland3f@gmailg.com", "1234567", "Roland", "Linisverycoolasd")    
    auth_register_v1("roland4aa@gmaigl.com", "1234567", "Roland", "Linisverycoolasd")    
    auth_register_v1("roland5ss@gmaigl.com", "1234567", "Roland", "Linisverycoolasd")    
    auth_register_v1("roland6dd@gmaigl.com", "1234567", "Roland", "Linisverycoolasd")    
    auth_register_v1("roland7ff@gmaigl.com", "1234567", "Roland", "Linisverycoolasd")    
    auth_register_v1("roland8aaa@gmaigl.com", "1234567", "Roland", "Linisverycoolasd")    
    auth_register_v1("roland9sss@gmaigl.com", "1234567", "Roland", "Linisverycoolasd")    
    auth_register_v1("roland0dddd@gmagil.com", "1234567", "Roland", "Linisverycoolasd")    
    auth_register_v1("roland12fff@gmagil.com", "1234567", "Roland","Linisverycoolasd")
    auth_register_v1("roland1q@agmail.com", "1234567", "Roland", "Linisverycoolasd") #22lettershandle    
    auth_register_v1("roland2w@gamail.com", "1234567", "Roland", "Linisverycoolasd")    
    auth_register_v1("roland3e@gmaail.com", "1234567", "Roland", "Linisverycoolasd")    
    auth_register_v1("roland4r@gmaail.com", "1234567", "Roland", "Linisverycoolasd")    
    auth_register_v1("roland5qq@gmaail.com", "1234567", "Roland", "Linisverycoolasd")    
    auth_register_v1("roland6ww@gasfmaail.com", "1234567", "Roland", "Linisverycoolasd")    
    auth_register_v1("rolanda7ee@gmaail.com", "1234567", "Roland", "Linisverycoolasd")    
    auth_register_v1("rosland8rr@gmaail.com", "1234567", "Roland", "Linisverycoolasd")    
    auth_register_v1("roldand9qwer@gamail.com", "1234567", "Roland", "Linisverycoolasd")    
    auth_register_v1("rofland0rewq@gamail.com", "1234567", "Roland", "Linisverycoolasd")    
    auth_register_v1("rolgand12zxcv@agmail.com", "1234567", "Roland","Linisverycoolasd")  
    auth_register_v1("rohland1@gmaail.com", "1234567", "Roland", "Linisverycoolasd") #22lettershandle    
    auth_register_v1("roljand2@gmaail.com", "1234567", "Roland", "Linisverycoolasd")    
    auth_register_v1("rolaknd3@gmaail.com", "1234567", "Roland", "Linisverycoolasd")    
    auth_register_v1("rolanld4@gmaail.com", "1234567", "Roland", "Linisverycoolasd")    
    auth_register_v1("rolandl5@gmaail.com", "1234567", "Roland", "Linisverycoolasd")    
    auth_register_v1("roldsaand6@gmaail.com", "1234567", "Roland", "Linisverycoolasd")    
    auth_register_v1("roland7@gmajil.com", "1234567", "Roland", "Linisverycoolasd")    
    auth_register_v1("roland8@gmajil.com", "1234567", "Roland", "Linisverycoolasd")    
    auth_register_v1("roland9@gmajil.com", "1234567", "Roland", "Linisverycoolasd")    
    auth_register_v1("roland0@gmajil.com", "1234567", "Roland", "Linisverycoolasd")    
    auth_register_v1("roland12a@gjmail.com", "1234567", "Roland","Linisverycoolasd")
    auth_register_v1("roland1s@gmjail.com", "1234567", "Roland", "Linisverycoolasd") #22lettershandle    
    auth_register_v1("roland2d@gmjail.com", "1234567", "Roland", "Linisverycoolasd")    
    auth_register_v1("roland3f@gmjail.com", "1234567", "Roland", "Linisverycoolasd")    
    auth_register_v1("roland4aa@gjmail.com", "1234567", "Roland", "Linisverycoolasd")    
    auth_register_v1("roland5ss@gjjmail.com", "1234567", "Roland", "Linisverycoolasd")    
    auth_register_v1("roland6dd@gmajil.com", "1234567", "Roland", "Linisverycoolasd")    
    auth_register_v1("roland7ff@gmaijl.com", "1234567", "Roland", "Linisverycoolasd")    
    auth_register_v1("roland8aaa@gmajil.com", "1234567", "Roland", "Linisverycoolasd")    
    auth_register_v1("roland9sss@gmajil.com", "1234567", "Roland", "Linisverycoolasd")    
    auth_register_v1("roland0dddd@gmjail.com", "1234567", "Roland", "Linisverycoolasd")    
    auth_register_v1("roland12fff@gmjail.com", "1234567", "Roland","Linisverycoolasd")
    auth_register_v1("roland1q@gmailj.com", "1234567", "Roland", "Linisverycoolasd") #22lettershandle    
    auth_register_v1("roland2w@gmfail.com", "1234567", "Roland", "Linisverycoolasd")    
    auth_register_v1("roland3e@gmafil.com", "1234567", "Roland", "Linisverycoolasd")    
    auth_register_v1("roland4r@gmaifl.com", "1234567", "Roland", "Linisverycoolasd")    
    auth_register_v1("roland5qq@gmafil.com", "1234567", "Roland", "Linisverycoolasd")    
    auth_register_v1("roland6ww@gmafil.com", "1234567", "Roland", "Linisverycoolasd")    
    auth_register_v1("roland7ee@gmafil.com", "1234567", "Roland", "Linisverycoolasd")    
    auth_register_v1("roland8rr@gmaiffl.com", "1234567", "Roland", "Linisverycoolasd")    
    auth_register_v1("rolaasdnd9qwer@gmail.com", "1234567", "Roland", "Linisverycoolasd")    
    auth_register_v1("rolanfdsd0rewq@gfmail.com", "1234567", "Roland", "Linisverycoolasd")    
    auth_register_v1("rolandasd12zxcv@fgmail.com", "1234567", "Roland","Linisverycoolasd") 

    assert data['users'][0]['handle'] == 'rolandlinisverycool0'
    assert data['users'][1]['handle'] == 'rolandlinisverycool0'
    assert data['users'][0]['handle'] == 'rolandlinisverycool0'
    assert data['users'][1]['handle'] == 'rolandlinisverycool0' 
    assert data['users'][0]['handle'] == 'rolandlinisverycool0'
    assert data['users'][1]['handle'] == 'rolandlinisverycool0' 
    assert data['users'][0]['handle'] == 'rolandlinisverycool0'
    assert data['users'][1]['handle'] == 'rolandlinisverycool0' 
    assert data['users'][1]['handle'] == 'rolandlinisverycool0' 
    assert data['users'][1]['handle'] == 'rolandlinisverycool0' 
    assert data['users'][1]['handle'] == 'rolandlinisverycool0' 
    assert data['users'][1]['handle'] == 'rolandlinisverycool0' 
    assert data['users'][1]['handle'] == 'rolandlinisverycool0' 
    assert data['users'][1]['handle'] == 'rolandlinisverycool0' 
    assert data['users'][1]['handle'] == 'rolandlinisverycool0' 
    assert data['users'][1]['handle'] == 'rolandlinisverycool0' 
    assert data['users'][1]['handle'] == 'rolandlinisverycool0' 
    assert data['users'][1]['handle'] == 'rolandlinisverycool0' 
    assert data['users'][1]['handle'] == 'rolandlinisverycool0' 
    assert data['users'][1]['handle'] == 'rolandlinisverycool0' 
    assert data['users'][1]['handle'] == 'rolandlinisverycool0' 
    assert data['users'][1]['handle'] == 'rolandlinisverycool0' 
    assert data['users'][1]['handle'] == 'rolandlinisverycool0' 
    assert data['users'][1]['handle'] == 'rolandlinisverycool0' 
    assert data['users'][1]['handle'] == 'rolandlinisverycool0' 
    assert data['users'][1]['handle'] == 'rolandlinisverycool0' 
    assert data['users'][1]['handle'] == 'rolandlinisverycool0' 
    assert data['users'][1]['handle'] == 'rolandlinisverycool0' 
    assert data['users'][1]['handle'] == 'rolandlinisverycool0' 
    assert data['users'][1]['handle'] == 'rolandlinisverycool0' 
    assert data['users'][1]['handle'] == 'rolandlinisverycool0' 
    assert data['users'][1]['handle'] == 'rolandlinisverycool0' 
    assert data['users'][1]['handle'] == 'rolandlinisverycool0' 
    assert data['users'][1]['handle'] == 'rolandlinisverycool0' 
    assert data['users'][1]['handle'] == 'rolandlinisverycool0' 
    assert data['users'][1]['handle'] == 'rolandlinisverycool0' 
    assert data['users'][1]['handle'] == 'rolandlinisverycool0' 
    assert data['users'][1]['handle'] == 'rolandlinisverycool0' 
    assert data['users'][1]['handle'] == 'rolandlinisverycool0' 
    assert data['users'][1]['handle'] == 'rolandlinisverycool0' 
    assert data['users'][1]['handle'] == 'rolandlinisverycool0' 
    assert data['users'][1]['handle'] == 'rolandlinisverycool0' 
    assert data['users'][1]['handle'] == 'rolandlinisverycool0' 
    assert data['users'][1]['handle'] == 'rolandlinisverycool0' 
    assert data['users'][1]['handle'] == 'rolandlinisverycool0' 
    assert data['users'][1]['handle'] == 'rolandlinisverycool0' 
    assert data['users'][1]['handle'] == 'rolandlinisverycool0' 
    assert data['users'][1]['handle'] == 'rolandlinisverycool0' 
    assert data['users'][1]['handle'] == 'rolandlinisverycool0' 
    assert data['users'][1]['handle'] == 'rolandlinisverycool0' 
    assert data['users'][1]['handle'] == 'rolandlinisverycool0' 
    assert data['users'][1]['handle'] == 'rolandlinisverycool0' 
    assert data['users'][1]['handle'] == 'rolandlinisverycool0' 
    assert data['users'][1]['handle'] == 'rolandlinisverycool0' 
    assert data['users'][1]['handle'] == 'rolandlinisverycool0' 
    assert data['users'][1]['handle'] == 'rolandlinisverycool0' 
    assert data['users'][1]['handle'] == 'rolandlinisverycool0' 
    assert data['users'][1]['handle'] == 'rolandlinisverycool0' 
    assert data['users'][1]['handle'] == 'rolandlinisverycool0' 
    assert data['users'][1]['handle'] == 'rolandlinisverycool0' 
    assert data['users'][1]['handle'] == 'rolandlinisverycool0' 
    assert data['users'][1]['handle'] == 'rolandlinisverycool0' 
    assert data['users'][1]['handle'] == 'rolandlinisverycool0' 
    assert data['users'][1]['handle'] == 'rolandlinisverycool0' 
    assert data['users'][1]['handle'] == 'rolandlinisverycool0' 
    assert data['users'][1]['handle'] == 'rolandlinisverycool0' 
    assert data['users'][1]['handle'] == 'rolandlinisverycool0' 
    assert data['users'][1]['handle'] == 'rolandlinisverycool0' 
    assert data['users'][1]['handle'] == 'rolandlinisverycool0' 
    assert data['users'][1]['handle'] == 'rolandlinisverycool0' 
    assert data['users'][1]['handle'] == 'rolandlinisverycool0' 
    assert data['users'][1]['handle'] == 'rolandlinisverycool0' 
    assert data['users'][1]['handle'] == 'rolandlinisverycool0' 
    assert data['users'][1]['handle'] == 'rolandlinisverycool0' 
    assert data['users'][1]['handle'] == 'rolandlinisverycool0' 
    assert data['users'][1]['handle'] == 'rolandlinisverycool0' 
    assert data['users'][1]['handle'] == 'rolandlinisverycool0' 
    assert data['users'][1]['handle'] == 'rolandlinisverycool0' 
    assert data['users'][1]['handle'] == 'rolandlinisverycool0' 
    assert data['users'][1]['handle'] == 'rolandlinisverycool0' 
    assert data['users'][1]['handle'] == 'rolandlinisverycool0' 
    assert data['users'][1]['handle'] == 'rolandlinisverycool0' 
    assert data['users'][1]['handle'] == 'rolandlinisverycool0' 
    assert data['users'][1]['handle'] == 'rolandlinisverycool0' 
    assert data['users'][1]['handle'] == 'rolandlinisverycool0' 
    assert data['users'][1]['handle'] == 'rolandlinisverycool0' 
    assert data['users'][1]['handle'] == 'rolandlinisverycool0' 
    assert data['users'][1]['handle'] == 'rolandlinisverycool0' 
    assert data['users'][1]['handle'] == 'rolandlinisverycool0' 
    assert data['users'][1]['handle'] == 'rolandlinisverycool0' 
    assert data['users'][1]['handle'] == 'rolandlinisverycool0' 
    assert data['users'][1]['handle'] == 'rolandlinisverycool0' 
    assert data['users'][1]['handle'] == 'rolandlinisverycool0' 
    assert data['users'][1]['handle'] == 'rolandlinisverycool0' 
    assert data['users'][1]['handle'] == 'rolandlinisverycool0' 
    assert data['users'][1]['handle'] == 'rolandlinisverycool0' 
    assert data['users'][1]['handle'] == 'rolandlinisverycool0' 
    assert data['users'][1]['handle'] == 'rolandlinisverycool0' 
    assert data['users'][1]['handle'] == 'rolandlinisverycool0' 
    assert data['users'][1]['handle'] == 'rolandlinisverycool0' 
    assert data['users'][1]['handle'] == 'rolandlinisverycool0' 
    assert data['users'][1]['handle'] == 'rolandlinisverycool0' 
    assert data['users'][1]['handle'] == 'rolandlinisverycool0' 
    assert data['users'][1]['handle'] == 'rolandlinisverycool0' 
    assert data['users'][1]['handle'] == 'rolandlinisverycool0' 
    assert data['users'][1]['handle'] == 'rolandlinisverycool0' 
    assert data['users'][1]['handle'] == 'rolandlinisverycool0' 
    assert data['users'][1]['handle'] == 'rolandlinisverycool0' 
    assert data['users'][1]['handle'] == 'rolandlinisverycool0' 
    assert data['users'][1]['handle'] == 'rolandlinisverycool0' 
    assert data['users'][1]['handle'] == 'rolandlinisverycool0' 
    assert data['users'][1]['handle'] == 'rolandlinisverycool0' 
    assert data['users'][1]['handle'] == 'rolandlinisverycool0' 
    assert data['users'][1]['handle'] == 'rolandlinisverycool0' 
    assert data['users'][1]['handle'] == 'rolandlinisverycool0' 
    assert data['users'][1]['handle'] == 'rolandlinisverycool0' 
    assert data['users'][1]['handle'] == 'rolandlinisverycool0' 
    assert data['users'][1]['handle'] == 'rolandlinisverycool0' 
    assert data['users'][1]['handle'] == 'rolandlinisverycool0' 
    assert data['users'][1]['handle'] == 'rolandlinisverycool0' 
    assert data['users'][1]['handle'] == 'rolandlinisverycool0' 
    assert data['users'][1]['handle'] == 'rolandlinisverycool0' 
    assert data['users'][1]['handle'] == 'rolandlinisverycool0' 
    assert data['users'][1]['handle'] == 'rolandlinisverycool0' 
    assert data['users'][1]['handle'] == 'rolandlinisverycool0' 
    assert data['users'][1]['handle'] == 'rolandlinisverycool0' 
    assert data['users'][1]['handle'] == 'rolandlinisverycool0' 
    assert data['users'][1]['handle'] == 'rolandlinisverycool0' 
    assert data['users'][1]['handle'] == 'rolandlinisverycool0' 
    assert data['users'][1]['handle'] == 'rolandlinisverycool0' 
    assert data['users'][1]['handle'] == 'rolandlinisverycool0' 
    assert data['users'][1]['handle'] == 'rolandlinisverycool0' 
    assert data['users'][1]['handle'] == 'rolandlinisverycool0' 
    