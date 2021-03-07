For channel_test:
    - Assume adding two users to channel will account for multiple (more than two) in invite tesing 
    - Assume either AccessError or InputError would be raised, not both
    - Assume that there is only one owner member in details testing
    - Assume that a working test after two invites for details accounts for multiple invites 
    - Assume that working tests for public channels will also cover most tests for private channels as long as
      one is copied over
