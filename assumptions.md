For auth.py:
- Assumed that the auth_user_id is the placement of that particular user in the users list upon registration, ie. the first registered user has the user id of 1 as it is the first element in the list.
- Assumed that the inputed lastname and firstname can contain any character and doesn't necessarily have to be letters, eg. the firstname can be $%^^&&* and the lastname can be (tommy)*** as long as it satisfies the length requirements.
- Assumed that the password can contain any character and it can be of any length as long as it's greater than or equal to 6 characters, eg. the password can be 50 characters long and can contain special characters in it as well.

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

For channel_add_owners:
- Owner can be added even if not already in the channel

For channel_leave_v1:
- Assume that an owner may not leave if they are the only owner left

For channels.py:
- Assume that channels_create_v1 will produce an InputError when no channel name is given
- Assume that is_public will always be True or False

For dm_invite_v1:
- Assume that if u_id is already in the dm, attempting to invite again will result
in an InputError and will not add u_id again.
- Assume that inviting a user will update the name based on the new list of members

From dm_leave_v1:
- Assume that a user leaving will update the name bsed on the new list of members

For message.py:
- Optional message is appended to the shared message 
- We cannot share a deleted message
- Optional message cannot exceed 1000 characters
- Cannot send no message
- When deleting a string, the contents of the message becomes nothing
- Time_ variables are rounded to 1 decimal place

For admin.py:
- Assume that either InputError will be raised when Input isn't valid
- Assume that either AccessError will be raised when user doesn't have permission

For other.py
- Assume that either InputError will be raised when Input isn't valid
- Assume that either AccessError will be raised when user doesn't have permission
- Assume that given query_str is always string
