import sys
from flask import Flask, request, send_from_directory
from flask_cors import CORS
from json import dumps, loads, dump
from src import auth
from src import config
from src import other
from src import user
from src.admin import admin_user_remove_v1
from src.admin import admin_userpermission_change_v1
from src.auth import auth_register_v1
from src.channel import channel_addowner_v1
from src.channel import channel_details_v1
from src.channel import channel_invite_v1
from src.channel import channel_join_v1
from src.channel import channel_leave_v1
from src.channel import channel_messages_v1
from src.channel import channel_removeowner_v1
from src.channels import channels_create_v1
from src.channels import channels_list_v1
from src.channels import channels_listall_v1
from src.data import data
from src.dm import dm_create_v1
from src.dm import dm_details_v1
from src.dm import dm_invite_v1
from src.dm import dm_leave_v1
from src.dm import dm_list_v1
from src.dm import dm_messages_v1
from src.dm import dm_remove_v1
from src.error import InputError
from src.message import message_edit_v1
from src.message import message_remove_v1
from src.message import message_send_v1
from src.message import message_senddm_v1
from src.message import message_share_v1
from src.other import clear_v1
from src.other import notifications_get_v1
from src.other import search_v1

# with open('store.json', 'r') as fp:
#    global data
#    data = loads(fp.read())

def defaultHandler(err):
    response = err.get_response()
    print('response', err, err.get_response())
    response.data = dumps({
        "code": err.code,
        "name": "System Error",
        "message": err.get_description(),
    })
    response.content_type = 'APPlication/json'
    return response

APP = Flask(__name__, static_url_path='/static/')
CORS(APP)

APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(Exception, defaultHandler)

@APP.route('/static/<path:path>')
def send__js(path):
    return send_from_directory('', path)



# Example
@APP.route("/echo", methods=['GET'])
def echo():
    data = request.args.get('data')
    if data == 'echo':
   	    raise InputError(description='Cannot echo "echo"')
    return dumps({
        'data': data
    })

@APP.route('/user/profile/uploadphoto/v1', methods=['POST'])
def image():
    info = request.get_json()
    r = user.user_profile_uploadphoto_v1(info['token'], info['img_url'], int(info['x_start']), int(info['y_start']), int(info['x_end']), int(info['y_end']))  
    return dumps(r)

@APP.route('/search/v2', methods=['GET'])
def search():
    token = request.args.get('token')
    query_str = request.args.get('query_str')
    r = search_v1(token, query_str)
    return dumps(r)

@APP.route('/admin/user/remove/v1', methods=['DELETE'])
def admin_user_remove():
    inputs = request.get_json()
    r = admin_user_remove_v1(inputs['token'], inputs['u_id'])
    return dumps(r)

@APP.route('/admin/userpermission/change/v1', methods=['POST'])
def admin_userpermission_change():
    inputs = request.get_json()
    r = admin_userpermission_change_v1(inputs['token'], inputs['u_id'], inputs['permission_id'])
    return dumps(r)

@APP.route('/notifications/get/v1', methods=['GET'])
def notifications_get():
    token = request.args.get('token')
    r = notifications_get_v1(token)
    return dumps(r)

################################################################################
#####################           AUTH ROUTES            #########################
################################################################################

@APP.route('/auth/login/v2', methods=['POST'])
def login():
    """
    Description of function:
        Gets the user inputs and calls the auth_login_v1 function
    Parameters:
        None
    Exceptions:
        None
    Returns:
        Returns the result of the auth_login_v1 function in json
    """   
    inputs = request.get_json()
    r = auth.auth_login_v1(inputs['email'], inputs['password'])
    with open('store.json', 'w') as fp:
        fp.write(dumps(data))
    return dumps(r)

@APP.route('/auth/register/v2', methods=['POST'])
def register():
    """
    Description of function:
        Gets the user inputs and calls the auth_register_v1 function
    Parameters:
        None
    Exceptions:
        None
    Returns:
        Returns the result of the auth_register_v1 function in json
    """       
    inputs = request.get_json()
    r = auth_register_v1(inputs['email'], inputs['password'], inputs['name_first'], inputs['name_last'])
    with open('store.json', 'w') as fp:
        fp.write(dumps(data))
    return dumps(r)

@APP.route('/auth/logout/v1', methods=['POST'])
def logout():
    """
    Description of function:
        Gets the user inputs and calls the auth_logout_v1 function
    Parameters:
        None
    Exceptions:
        None
    Returns:
        Returns the result of the auth_logout_v1 function in json
    """       
    inputs = request.get_json()
    r = auth.auth_logout_v1(inputs['token'])
    with open('store.json', 'w') as fp:
        fp.write(dumps(data))    
    return dumps(r)

################################################################################
#####################           USER ROUTES            #########################
################################################################################

@APP.route('/user/profile/v2', methods=['GET'])
def user_profile():
    """
    Description of function:
        Gets the user inputs from the query string and calls the user_profile_v1 function
    Parameters:
        None
    Exceptions:
        None
    Returns:
        Returns the result of the user_profile_v1 function in json
    """       
    token = request.args.get('token')
    u_id = int(request.args.get('u_id'))
    r = user.user_profile_v1(token, u_id)
    return dumps(r)

@APP.route('/user/profile/setname/v2', methods=['PUT'])
def profile_setname():
    """
    Description of function:
        Gets the user inputs and calls the user_profile_setname_v1 function
    Parameters:
        None
    Exceptions:
        None
    Returns:
        Returns the result of the user_profile_setname_v1 function in json
    """       
    inputs = request.get_json()
    r = user.user_profile_setname_v1(inputs['token'], inputs['name_first'], inputs['name_last'])
    return dumps(r)

@APP.route('/user/profile/setemail/v2', methods=['PUT'])
def profile_setemail():
    """
    Description of function:
        Gets the user inputs and calls the user_profile_setemail_v1 function
    Parameters:
        None
    Exceptions:
        None
    Returns:
        Returns the result of the user_profile_setemail_v1 function in json
    """       
    inputs = request.get_json()
    r = user.user_profile_setemail_v1(inputs['token'], inputs['email'])
    return dumps(r)

@APP.route('/user/profile/sethandle/v1', methods=['PUT'])
def profile_sethandle():
    """
    Description of function:
        Gets the user inputs and calls the user_profile_sethandle_v1 function
    Parameters:
        None
    Exceptions:
        None
    Returns:
        Returns the result of the user_profile_sethandle_v1 function in json
    """        
    inputs = request.get_json()
    r = user.user_profile_sethandle_v1(inputs['token'], inputs['handle_str']) 
    return dumps(r)

@APP.route('/users/all/v1', methods=['GET'])
def users_all():
    """
    Description of function:
        Gets the user inputs and calls the users_all_v1 function
    Parameters:
        None
    Exceptions:
        None
    Returns:
        Returns the result of the users_all_v1 function in json
    """        
    token = request.args.get('token')
    r = user.users_all_v1(token)
    with open('store.json', 'w') as fp:
        fp.write(dumps(data))    
    return dumps(r)

################################################################################
#####################          OTHER ROUTES            #########################
################################################################################

@APP.route('/clear/v1', methods=['DELETE'])
def clear():
    """
    Description of function:
        Gets the user inputs and calls the clear_v1 function
    Parameters:
        None
    Exceptions:
        None
    Returns:
        Returns the result of the clear_v1 function in json
    """        
    r = other.clear_v1()
    with open('store.json', 'w') as fp:
        fp.write(dumps(data))    
    return dumps(r)


################################################################################
#####################         CHANNELS ROUTES          #########################
################################################################################

@APP.route("/channels/list/v2", methods=['GET'])
def get_list():
    token = request.args.get('token')
    channels = channels_list_v1(token)
    return dumps(channels)

@APP.route("/channels/listall/v2", methods=['GET'])
def get_listall():
    token = request.args.get('token')
    channels = channels_listall_v1(token)
    return dumps(channels)

@APP.route("/channels/create/v2", methods=['POST'])
def create_channel():
    data = request.get_json()
    channel_id = channels_create_v1(data['token'], data['name'], data['is_public'])
    return dumps(channel_id)

################################################################################
#####################         CHANNEL ROUTES           #########################
################################################################################

@APP.route("/channel/invite/v2", methods=['POST'])
def invite_channel():
    data = request.get_json()
    channel_invite_v1(data['token'], data['channel_id'], data['u_id'])
    return dumps({})
    
@APP.route("/channel/details/v2", methods=['GET'])
def details_channel():
    token = request.args.get('token')
    channel_id = int(request.args.get('channel_id'))
    details = channel_details_v1(token, channel_id)
    return dumps(details)
    
@APP.route("/channel/messages/v2", methods=['GET'])
def messages_channel():
    token = request.args.get('token')
    channel_id = int(request.args.get('channel_id'))
    start = start(request.args.get('start'))
    msg = channel_messages_v1(token, channel_id, start)
    return dumps(msg)

@APP.route("/channel/join/v2", methods=['POST'])
def join_channel():
    data = request.get_json()
    channel_join_v1(data['token'], data['channel_id'])
    return dumps({})

@APP.route("/channel/addowner/v1", methods=['POST'])
def addowner_channel():
    data = request.get_json()
    channel_addowner_v1(data['token'], data['channel_id'], data['u_id'])
    return dumps({})
    
@APP.route("/channel/removeowner/v1", methods=['POST'])
def removeowner_channel():
    data = request.get_json()
    channel_removeowner_v1(data['token'], data['channel_id'], data['u_id'])
    return dumps({})

@APP.route("/channel/leave/v1", methods=['POST'])
def leave_channel():
    data = request.get_json()
    channel_leave_v1(data['token'], data['channel_id'])
    return dumps({})

################################################################################
#####################           DM ROUTES              #########################
################################################################################

@APP.route("/dm/details/v1", methods=['GET'])
def details_dm():
    token = request.args.get('token')
    dm_id = int(request.args.get('dm_id'))
    details = dm_details_v1(token, dm_id)
    return dumps(details)

@APP.route("/dm/list/v1", methods=['GET'])
def list_dm():
    data = request.args.get('token')
    dm_list = dm_list_v1(data)
    return dumps(dm_list)

@APP.route("/dm/create/v1", methods=['POST'])
def create_dm():
    data = request.get_json()
    dm_info = dm_create_v1(data['token'], data['u_ids'])
    return dumps(dm_info)

@APP.route("/dm/remove/v1", methods=['DELETE'])
def remove_dm():
    data = request.get_json()
    dm_remove_v1(data['token'], data['dm_id'])
    return dumps({})

@APP.route("/dm/invite/v1", methods=['POST'])
def invite_dm():
    data = request.get_json()
    dm_invite_v1(data['token'], data['dm_id'], data['u_id'])
    return dumps({})
    
@APP.route("/dm/leave/v1", methods=['POST'])
def leave_dm():
    data = request.get_json()
    dm_leave_v1(data['token'], data['dm_id'])
    return dumps({})
    
@APP.route("/dm/messages/v1", methods=['GET'])
def messages_dm():
    token = request.args.get('token')
    dm_id = int(request.args.get('dm_id'))
    start = int(request.args.get('start'))
    msg = dm_messages_v1(token, dm_id, start)
    return dumps(msg)

################################################################################
#####################         MESSAGE ROUTES           #########################
################################################################################

@APP.route("/message/send/v2", methods=['POST'])
def message_send():
    data = request.get_json()
    message_id = message_send_v1(data['token'], data['channel_id'], data['message'])
    return dumps(message_id)

@APP.route("/message/edit/v2", methods=['PUT'])
def message_edit():
    data = request.get_json()
    message_edit_v1(data['token'], data['message_id'], data['message'])
    return dumps({})

@APP.route("/message/remove/v1", methods=['DELETE'])
def message_remove():
    data = request.get_json()
    message_remove_v1(data['token'], data['message_id'])
    return dumps({})

@APP.route("/message/share/v1", methods=['POST'])
def message_share():
    data = request.get_json()
    shared_message_id = message_share_v1(data['token'], data['og_message_id'], data['message'], data['channel_id'], data['dm_id'])
    return dumps(shared_message_id)

@APP.route("/message/senddm/v1", methods=['POST'])
def message_senddm():
    data = request.get_json()
    message_id = message_senddm_v1(data['token'], data['dm_id'], data['message'])
    return dumps(message_id)

################################################################################
#####################           MAIN APP.RUN           #########################
################################################################################

if __name__ == "__main__":
    APP.run(port=config.port) # Do not edit this port

