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
    - Assume that working tests for public channels will also cover most tests for private channels as long as
      one is copied over
