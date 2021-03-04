import pytest
from src.auth import auth_login_v1
from src.auth import auth_register_v1
from src.error import InputError
from src.auth_info import users

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

def test_login_invalid_email():
    assert (auth_login_v1("asdfg.com", "a2sdf") == "invalid mail")
    assert (auth_login_v1("asdfg@gmailcom", "as2df") == "invalid mail")    
    assert (auth_login_v1("asdfgcom", "asdssf") == "invalid mail")    
    assert (auth_login_v1("asdfg@com", "asaadf") == "invalid mail")        

def test_login_email_unshared():
    pass 

def test_login_email_shared():
    pass

def test_login_incorrect_password():
    with pytest.raises(InputError):
        assert auth_login_v1("tim@gmail.com", "1234")    

def test_login_correct_password():
    auth_register_v1("tim@gmail.com", "1234hello!", "Tim", "Brown")
    auth_login_v1("tim@gmail.com", "1234hello!")
    auth_register_v1("tom@yahoo.com", "asdfgasdg123", "Tom", "Blue")
    assert users["user1"]["password"] == "1234hello!"
    auth_login_v1("tom@yahoo.com", "asdfgasdg123")
    assert users["user2"]["password"] == "asdfgasdg123"


#test for auth_register
def test_register_invalid_email():
    with pytest.raises(InputError):
        assert auth_register_v1("12345678", "hello!!!1", "Tim", "Oreo")
    
def test_register_valid_email():
    pass
    
def test_register_email_unshared():
    pass

def test_register_email_shared():
    with pytest.raises(InputError):
        auth_register_v1("tim@gmail.com", "1234hello!", "Tim", "Brown")
        assert auth_register_v1("tim@gmail.com", "1cooooool!!!", "Tim", "Blue")

def check_password_test(): #less than 6 characters is a fail
    with pytest.raises(InputError):
        assert auth_register_v1("honey@outlook.com", "hi", "Tim", "Oreo")

def firstname_length_test(): # if firstname < 1 or >50 is a fail
    with pytest.raises(InputError):
        assert auth_register_v1("honey@outlook.com", "hi", "", "Oreo")   

def lastname_length_test(): #if lastname < 1 or >50 is a fail
    with pytest.raises(InputError):
        assert auth_register_v1("honey@outlook.com", "hi", "Tim", "")

#register handle
def test_handle_taken():
    #clear()
    user_1 = auth_register_v1("asdf@gmail.com","1234", "Tom", "Holyy")
    user_1["handle"] = "tomholyy"
    user_1 = auth_register_v1("fdsa@gmail.com","12345", "Tom", "Holyy")
    assert (user_1["handle"] == "tomholyy0")

def test_handle_nospace():
    #clear()
    user_1 = auth_register_v1("asdf@gmail.com","1234", "Tom", "Holyy@")
    assert (user_1["handle"] == "tomholyy")

def test_handle_toolong():
    #clear()
    user_1 = auth_register_v1("asdf@gmail.com","1234", "asdfasdfasdf", "asdfasdfasdf")
    assert (user_1["handle"] == "asdfasdfasdfasdfasdf")

def test_handle_same():
    #clear()
    user_1 = auth_register_v1("asdf@gmail.com","1234", "hellomynameis", "garythekingpingyo")
    assert (user_1["handle"] == "hellomynameisgarythe")
    user_2 = auth_register_v1("fdsadasd@gmail.com","1234444", "hellomynameis", "garythekingpingyo")
    assert (user_2["handle"] == "hellomynameisgaryth0")
    user_3 = auth_register_v1("fdsadasd@gmail.com","1234444", "hellomynameis", "garythekingpingyo")
    assert (user_3["handle"] == "hellomynameisgaryth1")