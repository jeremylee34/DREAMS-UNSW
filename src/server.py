import sys
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from src.error import InputError
from src import config
from src import auth
from src import user
from src import other
from src.data import data

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

APP = Flask(__name__)
CORS(APP)

APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(Exception, defaultHandler)


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
    r = auth.auth_register_v1(inputs['email'], inputs['password'], inputs['name_first'], inputs['name_last'])
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
    return dumps(r)

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
    return dumps(r)

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
    return dumps(r)

if __name__ == "__main__":
    APP.run(port=config.port) # Do not edit this port
