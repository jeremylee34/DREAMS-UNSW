Assumption 1:
The auth_user_id that is returned in both functions of auth.py is assumed to be the placement of that particular user in the users list upon registration, ie. the first registered user has the user id of 1 as it is the first element in the list.

Assumption 2:
In auth.py, it is assumed that the inputed lastname and firstname can contain any character and doesn't necessarily have to be letters, eg. the firstname can be $%^^&&* and the lastname can be (tommy)*** as long as it satisfies the length requirements

Assumption 3:
In auth.py, it is assumed that the password can contain any character and it can be of any length as long as it's greater than or equal to 6 characters, eg. the password can be 50 characters long and can contain special characters in it as well.

