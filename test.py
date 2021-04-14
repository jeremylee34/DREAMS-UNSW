from flask import Flask, request, send_from_directory
from json import dumps
from src.auth import auth_register_v1
from src.data import data
from src.config import port
from src.user import user_profile_uploadphoto_v1

app = Flask(__name__, static_url_path='/static/')

@app.route('/static/<path:path>')
def send_js(path):
    return send_from_directory('', path)

@app.route('/auth/register/v2', methods=['POST'])
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

@app.route('/user/profile/uploadphoto/v1', methods=['POST'])
def image():
    info = request.get_json()
    r = user_profile_uploadphoto_v1(info['token'], info['img_url'], int(info['x_start']), int(info['y_start']), int(info['x_end']), int(info['y_end']))  
    return dumps(r)      

if __name__ == "__main__":
    app.run(port=port)
