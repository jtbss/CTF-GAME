# import secrets
import base64
import secrets
import binascii
from time import time
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5

block_size = 16

class Https:
    def __init__(self, key, time=time()) -> None:
        self.time = time
        self.public_key = key
        self.message = None
        self.nonce = None
        self.init_message = 'COMP7170 is the best course in the universe'
    
    def encrypt_random_number(self):
        # creates 32 bytes (256 bits) random number
        random_number = secrets.token_hex(32)

        # store the nonce
        self.nonce = random_number

        # encrypt the nonce with the public key
        cipher = Cipher_pkcs1_v1_5.new(RSA.importKey(self.public_key))
        cipher_text = base64.b64encode(cipher.encrypt(random_number.encode())).decode()

        return cipher_text
    
    def encrypt_message(self):
        print('key:', self.nonce)
        
        key = bytes.fromhex(self.nonce)
        random_number = secrets.token_hex(4)

        message = 'I love comp7170' + ' ' + random_number
        print('message:', message)
        
        cipher = AES.new(key, AES.MODE_ECB)
        padded_message = pad(message.encode('utf-8'), AES.block_size)
        encrypted_bytes = cipher.encrypt(padded_message)

        encrypted_message = base64.b64encode(encrypted_bytes).decode('utf-8')

        return encrypted_message        
