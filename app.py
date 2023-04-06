from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

from https import Https

app = Flask(__name__, template_folder='web', static_folder='web', static_url_path='/web')
CORS(app)

@app.route("/")
def get_web():
    return send_from_directory('web', 'index.html')


@app.route("/send_key", methods=['POST'])
def send_key():
    values = request.get_json() if request.data else None
    if not values:
        response = { 'message': 'Required data in missing.' }
        return jsonify(response), 400
    
    key_str = values['key']

    global huser
    huser = Https(key_str)
    encrypt_nonce = huser.encrypt_random_number()
    encrypt_message = huser.encrypt_message()
    print(encrypt_message)
    response = {
        'message': 'Send successfully',
        'data1': encrypt_nonce,
        'data2': encrypt_message
    }
    return jsonify(response), 200


if __name__ == "__main__":
    huser = Https('')
    app.run()
