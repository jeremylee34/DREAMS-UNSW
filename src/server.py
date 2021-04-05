import sys
from json import dumps
from flask import Flask, request
from flask_cors import CORS

from src.error import InputError
from src import config

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

@APP.route('/search/v2', methods=['GET'])
def search():
    inputs = request.get_json()
    r = other.search_v1(inputs['token'], inputs['query_str'])
    return dumps(r)

@APP.route('/admin/user/remove/v1', methods=['DELETE'])
def admin_user_remove():
    inputs = request.get_json()
    r = admin.admin_user_remove_v1(inputs['token'], inputs['u_id'])
    return dumps(r)

@APP.route('/admin/userpermission/change/v1', methods=['POST'])
def admin_userpermission_change():
    inputs = request.get_json()
    r = admin.admin_userpermission_change_v1(inputs['token'], inputs['u_id'], inputs['permission_id'])
    return dumps(r)

@APP.route('/notifications/get/v1', methods=['GET'])
def notifications_get():
    token = request.get_json()
    r = other.notifications_get_v1(token['token'])
    print(r)
    return dumps(r)

if __name__ == "__main__":
    APP.run(port=config.port) # Do not edit this port
