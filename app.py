import re
import time

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from https import Https

app = Flask(__name__, template_folder='web', static_folder='web', static_url_path='/web')
CORS(app)

public_key_pattern = re.compile(
    r'^-----BEGIN PUBLIC KEY-----\n'
    r'[A-Za-z0-9+/=\n]+\n'
    r'-----END PUBLIC KEY-----$'
)

def is_x509_public_key(data):
    return bool(public_key_pattern.match(data))


@app.route("/")
def get_web():
    return send_from_directory('web', 'index.html')


@app.route("/send_key", methods=['POST'])
def send_key():
    time.sleep(.5)

    values = request.get_json() if request.data else None
    if not values:
        response = { 'message': 'Required data in missing.' }
        return jsonify(response), 400
    
    key_str = values['key']
    # validate the public key format.
    if not is_x509_public_key(key_str):
        response = { 'message': 'Invalid public key format' }
        return jsonify(response), 400

    global huser
    huser = Https(key_str)
    encrypted_nonce = huser.encrypt_random_number()
    encrypted_message = huser.encrypt_message()

    if not encrypted_nonce or not encrypted_message:
        response = {'message': 'Encryption failed. Please check the public key format'}
        return jsonify(response), 400

    response = {
        'message': 'Send successfully',
        'data1': encrypted_nonce,
        'data2': encrypted_message
    }
    return jsonify(response), 200


@app.route('/validate', methods=['POST'])
def validate_message():
    time.sleep(.5)

    values = request.get_json() if request.data else None
    if not values:
        response = { 'message': 'Required data in missing.' }
        return jsonify(response), 400
    
    message = values['message']

    if not huser or not huser.get_public_key():
        response = { 'message': "It seems you haven't given me the public key yet." }
        return jsonify(response), 400

    feedback = huser.validate_message(message)
    if feedback:
        response = {
            'message': 'OK',
            'ctf': 'CTF_{$ THE PERSON WHO SEES THIS SENTENCE WILL BECOME RICH $}'
        }
        return jsonify(response), 200
    else:
        response = { 'message': 'Wrong message.' }
        return jsonify(response), 400

if __name__ == "__main__":
    huser = Https('')
    app.run()
