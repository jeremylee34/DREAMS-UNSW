import sys
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from src.error import InputError
from src import config
from src.channel import channel_invite_v1
from src.channel import channel_details_v1
from src.channel import channel_addowner_v1
from src.channel import channel_removeowner_v1
from src.dm import dm_invite_v1
from src.dm import dm_leave_v1
from src.dm import dm_messages_v1

def defaultHandler(err):
    response = err.get_response()
    print('response', err, err.get_response())
    response.data = dumps({
        "code": err.code,
        "name": "System Error",
        "message": err.get_description(),
    })
    response.content_type = 'application/json'
    return response

APP = Flask(__name__)
CORS(APP)

APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(Exception, defaultHandler)

# Example
@APP.route("/echo", methods=['GET'])
def echo():
    data = request.args.get('data')
    if data == 'echo':
   	    raise InputError(description='Cannot echo "echo"')
    return dumps({
        'data': data
    })
"""
Channel server routes
"""
@APP.route("channel/invite/v2", methods=['POST'])
def invite_channel():
    data = request.get_json()
    channel_invite_v1(data['token'], data['channel_id'], data['u_id'])
    return dumps({})
    
@APP.route("channel/details/v2", methods=['GET'])
def details_channel():
    data = request.get_json()
    channel_details_v1(data['token'], data['channel_id'])
    return dumps({name, is_public, owner_members, all_members})
    
@APP.route("channel/addowner/v1", methods=['POST'])
def addowner_channel():
    data = request.get_json()
    channel_addowner_v1(data['token'], data['channel_id'], data['u_id'])
    return dumps({})
    
@APP.route("channel/removeowner/v1", methods=['POST'])
def removeowner_channel():
    data = request.get_json()
    channel_removeowner_v1(data['token'], data['channel_id'], data['u_id'])
    return dumps({})

"""
Dm server routes
"""

@APP.route("dm/invite/v1", methods=['POST'])
def invite_dm():
    data = request.get_json()
    dm_invite_v1(data['token'], data['dm_id'], data['u_id'])
    return dumps({})
    
@APP.route("dm/leave/v1", methods=['POST'])
def leave_dm():
    data = request.get_json()
    dm_leave_v1(data['token'], data['dm_id'])
    return dumps({})
    
@APP.route("dm/messages/v1", methods=['GET'])
def messages_dm():
    data = request.get_json()
    dm_messages_v1(data['token'], data['dm_id'], data['start'])
    return dumps({messages, start, end})

if __name__ == "__main__":
    APP.run(port=config.port) # Do not edit this port
