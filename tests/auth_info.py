#dictionary in dictionary
users = {
    "user1" : {"password" : "1234", "firstname": "Tim", "Lastname": "John", "email": "tim@gmail.com"},
    "user2" : {"password" : "4#6@aA", "firstname": "Roland", "Lastname": "gordon", "email": "12345abc@yahoo.com"},
}
print(users)

def rego(password, firstname, Lastname, email):
    users["user1"]["password"] = password
    users["user1"]["firstname"] = firstname
    users["user1"]["Lastname"] = Lastname
    users["user1"]["email"] = email
    return users

rego("3844", "jane", "smith", "jane@gmail.com")
print(users["user1"])