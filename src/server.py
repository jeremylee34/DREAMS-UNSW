import sys
from json import dumps
from flask import Flask, request
from flask_cors import CORS

from src.error import InputError
from src import config
from src.channels import channels_list_v1
from src.channels import channels_create_v1
from src.channels import channels_listall_v1
from src.message import message_remove_v1
from src.message import message_edit_v1
from src.message import message_send_v1
from src.message import message_senddm_v1
from src.message import message_share_v1

from src import auth
from src import user
from src import other
from src import admin
from src import message
from src import channel
from src import channels
from src import dm

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
'''
Channels server routes
'''
@APP.route("channels/list/v2", methods=['GET'])
def get_list():
    token = request.args.get('token')
    channels = channels_list_v1(token)
    return dumps({channels})
@APP.route("channels/listall/v2", methods=['GET'])
def get_listall():
    token = request.args.get('token')
    channels = channels_listall_v1(token)
    return dumps({channels})
@APP.route("channels/create/v2", methods=['POST'])
def create_channel():
    data = request.get_json()
    channel_id = channels_create_v1(data['token'], data['name'], data['is_public'])
    return dumps({channel_id})
@APP.route("message/send/v2", methods=['POST'])
def message_send():
    data = request.get_json()
    message_id = message_send_v1(data['token'], data['channel_id'], data['message'])
    return dumps({message_id})
@APP.route("message/edit/v2", methods=['PUT'])
def message_edit():
    data = request.get_json()
    message_edit_v1(data['token'], data['message_id'], data['message'])
    return dumps({})
@APP.route("message/remove/v1", methods=['DELETE'])
def message_remove():
    data = request.get_json()
    message_remove_v1(data['token'], data['message_id'])
    return dumps({})
@APP.route("message/share/v1", methods=['POST'])
def message_share():
    data = request.get_json()
    shared_message_id = message_share_v1(data['token'], data['og_message_id'], data['message'], data['channel_id'], data['dm_id'])
    return dumps({shared_message_id})
@APP.route("message/senddm/v1", methods=['POST'])
def message_senddm():
    data = request.get_json()
    message_id = message_senddm_v1(data['token'], data['dm_id'], data['message'])
    return dumps({message_id})
if __name__ == "__main__":
    APP.run(port=config.port) # Do not edit this port
