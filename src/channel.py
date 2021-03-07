def channel_invite_v1(auth_user_id, channel_id, u_id):
    return {
    }

def channel_details_v1(auth_user_id, channel_id):
    return {
        'name': 'Hayden',
        'owner_members': [
            {
                'u_id': 1,
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
            }
        ],
        'all_members': [
            {
                'u_id': 1,
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
            }
        ],
    }

def channel_messages_v1(auth_user_id, channel_id, start):
    return {
        'messages': [
            {
                'message_id': 1,
                'u_id': 1,
                'message': 'Hello world',
                'time_created': 1582426789,
            }
        ],
        'start': 0,
        'end': 50,
    }

def channel_leave_v1(auth_user_id, channel_id):
    return {
    }

def channel_join_v1(auth_user_id, channel_id):

    if data['channels'][channel_id]['is_public'] == False:
        raise AccessError
    
    user_in_channel = False
    ## search thru all members
    for i in range(len(data['channels'][channel_id]['all_members'])):
        ## if auth_user_id matches the member
        if data['channels'][channel_id]['all_members'][i]['u_id'] == auth_user_id:
            user_in_channel = True

    ## if user not added, 
    if user_in_channel is False:
        user = user_profile_v1(auth_user_id, auth_user_id)
        user_to_append = {
            'u_id' : auth_user_id,
            'name_first' : user['name_first'],
            'name_last' : user['name_last'],
        }
        data['channels'][channel_id]['all_members'].append(user)
    else:
        pass
    return {
    }

def channel_addowner_v1(auth_user_id, channel_id, u_id):
    return {
    }

def channel_removeowner_v1(auth_user_id, channel_id, u_id):
    return {
    }
