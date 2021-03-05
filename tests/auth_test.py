import pytest
from src.auth import auth_login_v1
from src.auth import auth_register_v1
from src.error import InputError
from src.other import clear_v1

#tests for auth_login
def test_login_valid_email():
    with pytest.raises(Exception):
        auth_login_v1("fafasf@gmail.com", "asdf1234@") == "user1"
    with pytest.raises(Exception):
        auth_login_v1("asd@gmail.com", "asdfasf1234@") == "user2"
    with pytest.raises(Exception):
        auth_login_v1("2424ss@gmail.com", "asasfdf1234@") == "user3"
    with pytest.raises(Exception):
        auth_login_v1("42542552@gmail.com", "asdasff1234@") == "user4"

"""def test_login_invalid_email():
    assert (auth_login_v1("asdfg.com", "a2sdf") == "invalid mail")
    assert (auth_login_v1("asdfg@gmailcom", "as2df") == "invalid mail")    
    assert (auth_login_v1("asdfgcom", "asdssf") == "invalid mail")    
    assert (auth_login_v1("asdfg@com", "asaadf") == "invalid mail")   """     

# i dont get it
#def test_login_email_unshared():
#    pass 

#def test_login_email_shared():
#    pass

def test_login_incorrect_password():
    clear_v1()
    auth_user_id1 = auth_register_v1("hiheee@gmail.com", "1234", "K","S")
    auth_user_id2 = auth_login_v1("hiheee@gmail.com", "1234")
    assert(auth_user_id1 != auth_user_id2) 


def test_login_correct_password():
    clear_v1()
    auth_user_id1 = auth_register_v1("hiheee@gmail.com", "1234", "K","S")
    auth_user_id2 = auth_login_v1("hiheee@gmail.com", "1234")
    assert(auth_user_id1 == auth_user_id2)


#test for auth_register
def test_register_valid_email():
    clear_v1()
    auth_user_id1 = auth_register_v1("asdf@gmail.com", "1234", "K","S")
    auth_user_id2 = auth_login_v1("asdf@gmail.com", "1234")
    assert(auth_user_id1 == auth_user_id2)
    
def test_register_invalid_email():
    clear_v1()
    auth_user_id1 = auth_register_v1("asdf@gmail.com", "1234", "K","S")
    auth_user_id2 = auth_login_v1("asdf@gmail.com", "1234")
    assert(auth_user_id1 != auth_user_id2)
    
    
def test_register_email_unshared():
    clear_v1()
    auth_user_id1 = auth_register_v1("same@gmail.com", "1234", "Me", "Me")
    auth_user_id2 = auth_register_v1("Notsame@gmail.com", "1234", "NotMe", "NotMe")
    assert(auth_user_id1 != auth_user_id2)

#repeated
def test_register_email_shared():
    clear_v1()
    auth_user_id1 = auth_register_v1("same@gmail.com", "1234", "Me", "Me")
    auth_user_id2 = auth_register_v1("same@gmail.com", "1234", "NotMe", "NotMe")
    assert(auth_user_id2 == None)
    pass


def check_password_test(): #less than 6 characters is a fail
    clear_v1()
    with pytest.raises(InputError):
        assert auth_register_v1("honey@outlook.com", "hi", "Tim", "Oreo")

def firstname_length_test(): # if firstname < 1 or >50 is a fail
    clear_v1()
    with pytest.raises(InputError):
        assert auth_register_v1("honey@outlook.com", "hi", "", "Oreo")   

def lastname_length_test(): #if lastname < 1 or >50 is a fail
    clear_v1()
    with pytest.raises(InputError):
        assert auth_register_v1("honey@outlook.com", "hi", "Tim", "")
    
#register handle
def test_handle_taken():
    #clear()
    pass

def test_handle_nospace():
    #clear()
    pass

def test_handle_toolong():
    #clear()
    pass
def test_handle_same():
    #clear()
    pass
