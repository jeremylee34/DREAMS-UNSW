
For channel_join_v1:
- Assume nothing will occur after AccessError is raised
- Assume nothing will occur after InputError is raised
- Assume function will end if either error is raised
- Assume function will end if user_in_channel is True (user already added)

For channel_messages_v1:
- Assume nothing will occur after AccessError is raised
- Assume nothing will occur after InputError1 is raised
- Assume nothing will occur after InputError2 is raised
- Assume function will end if either error is raised
- Assumes 'start' argument is a valid index

For channel_test:
- Assume adding two users to channel will account for multiple (more than two) in invite tesing 
- Assume either AccessError or InputError would be raised, not both
- Assume that there is only one owner member in details testing
- Assume that a working test after two invites for details accounts for multiple invites 
- Assume that working tests for public channels will also cover most tests for private channels as long as one is copied over

For auth.py:
- Assumed that the auth_user_id is the placement of that particular user in the users list upon registration, ie. the first registered user has the user id of 1 as it is the first element in the list.
- Assumed that the inputed lastname and firstname can contain any character and doesn't necessarily have to be letters, eg. the firstname can be $%^^&&* and the lastname can be (tommy)*** as long as it satisfies the length requirements.
- Assumed that the password can contain any character and it can be of any length as long as it's greater than or equal to 6 characters, eg. the password can be 50 characters long and can contain special characters in it as well.

For channels.py:
- Assume that channels_create_v1 will produce an InputError when no channel name is given
- Assume that is_public will always be True or False