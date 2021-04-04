from src.data import data
def clear_v1():
    data['users'].clear()
    data['channels'].clear()
    data['messages'].clear()

def search_v2(token, query_str):
    input_token = request.args.get('token')
    input_query_str = request.args.get('query_str')
    return {
       'messages': [
            {
                'message_id': 1,
                'u_id': 1,
                'message': 'Hello world',
                'time_created': 1582426789,
            }
        ],
    } #when call if info blank make it removed suer

def notifications_get(token):
    valid = 0
    input_token = request.args.get('token')
    decoded_token = jwt.decode(input_token, 'HELLO', algorithms=['HS256'])
    get_notification = {"notification" : []}
    all_msg = []

    #find that person with token
    for x in data['users']:
        for y in x['session_ids']:
            if decoded_token["session_ids"] == y:
                #some actionsss
                #search all msg in channel/dm
                #collect, print20
                #change all funcs to other file and do apply func in server

    #collect all message
    for x in dict(reversed(list(noti_list.items()))): #newest noti first
        if len(all_msg <= 20)
            all_msg.append(x['notification_message'])

    return {
        get_notification["notification"]['notification_message']
    }
