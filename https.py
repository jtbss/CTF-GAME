import base64
import secrets
from time import time
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_v1_5
from Crypto.Util.Padding import pad

block_size = 16

class Https:
    def __init__(self, key, time=time()) -> None:
        self.time = time
        self.public_key = key
        self.message = None
        self.nonce = None

    def get_public_key(self):
        return self.public_key
    
    def validate_message(self, str):
        return str == self.message

    # encrypt the nonce with RSA
    def encrypt_random_number(self):
        try:
            # creates 32 bytes (256 bits) random number
            random_number = secrets.token_hex(32)

            # store the nonce
            self.nonce = random_number

            # encrypt the nonce with the public key
            cipher = PKCS1_v1_5.new(RSA.importKey(self.public_key))
            cipher_text = base64.b64encode(cipher.encrypt(random_number.encode())).decode()

            return cipher_text
        except:
            return None
    
    # encrypt the message with AES (Mode: ECB)
    def encrypt_message(self):
        try:
            print('key:', self.nonce)
            
            key = bytes.fromhex(self.nonce)
            random_number = secrets.token_hex(4)

            message = 'I love comp7170' + ' ' + random_number
            self.message = message
            print('message:', message)
            
            cipher = AES.new(key, AES.MODE_ECB)
            padded_message = pad(message.encode('utf-8'), AES.block_size)
            encrypted_bytes = cipher.encrypt(padded_message)

            encrypted_message = base64.b64encode(encrypted_bytes).decode('utf-8')
            print(encrypted_message)

            return encrypted_message
        except:
            return None     
