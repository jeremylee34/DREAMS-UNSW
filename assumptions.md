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