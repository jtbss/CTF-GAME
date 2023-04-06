# CTF-GAME
This is a simple CTF game. The basic idea is to simulate the process of SSL.
## Simple description of SSL
1. The client initiates an SSL connection request to the server, which includes information such as the encryption algorithm and protocol version supported by the client.

2. The server sends a certificate to the client, which contains information such as the server's public key, the certificate's issuer, and validity period.

3. The client verifies the certificate's authenticity, including checking if the certificate is expired, if the issuing authority is trustworthy, and if the server's hostname matches the one in the certificate.

4. If the certificate is valid, the client uses the public key in the certificate to encrypt a random number, and sends the encrypted random number to the server.

5. The server decrypts the random number sent by the client using its private key, and generates a symmetric key with the decrypted random number. This symmetric key is used for subsequent communication encryption and decryption.

6. The client and server negotiate an encryption algorithm and protocol version, and determine how to use the symmetric key to encrypt and decrypt communication data.

7. Both parties start using the symmetric key to encrypt and decrypt communication data, and data transmission takes place.

8. At the end of the SSL connection, the client and server negotiate how to close the connection and perform the connection closing operation. 

## How to play this game
### Generate key pairs
At first, you need to generate a pair of public and private key by using RSA. Below is an example.

Let's first generate RSA private key.
```shell
openssl genrsa -out private.pem 2048
```
Then, generate public key
```shell
openssl rsa -in private.pem -pubout -out public.pem
```
The format of the public and private key should like this
```plain text
-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA43GuI2kHsY9IWtMbO5vU
+opOH6LaBdhixPxuMkSZ2eqMmHEuJhiDX2VhyZZLdu5SKLLYCH0Nyg9i65otw63s
yNRWggpNVxtUEAPORkuKQnZ+D8HufMwT+68/z9yRrKCD4nm1C8r18GkPq2cx3zJA
MMBvPO4+q6tt3nY7ppCqT/lugdvGQ1b3q1dX7N7Ao/1QsJ4b6aQVIiLyuFjMvyL4
tZmf3ZMs5ZkSrXVblEkq43SLxr9lklEWTN/R2D12g/XauDYpXUam5IOap+TQpb5j
/2MJV6W/vl9CuGvrtrGkcPRIQptYMpkpqUps6gnnR83iNjHEXj6a1Vr4+C0/fL/M
MQIDAQAB
-----END PUBLIC KEY-----
```
### Exchange secret key and decryption
First send the content of the public key by clicking the `send to user` button. If successful, two ciphers can be seen above the input box.

The upper cipher is a nonce that is encrypted by the public key. The lower cipher is the message that is encrypted by the nonce.

What you need to do is decrypting the the first cipher by using the `private key` to get the nonce value.

Once you obtain the nonce value, you can decrypt the second cipher by this nonce value. Finally, the plaintext can be decrypted.
## Useful commands
### Transfer a Base64 string to binary file.
Any base64 sting needs to transfer to binary format before using OpenSSL to decrypt.
Assume the file `enc.txt` contains the content of base64 string.
```bash
base64 -d enc.txt > enc.bin
```
### Decrypt the file `enc.bin` using OpenSSL
`key` is the key that is decrypted from the first cipher
```shell
openssl rsautl -decrypt -inkey private_key.pem -in enc.bin -out dec.txt
```
If it is successful, the file `dec.txt` will contain the nonce value. You need to use this nonce value to decrypt the second cipher.
```shell
openssl enc -d -aes-256-ecb -in enc.bin -out dec.txt -K 40b8c1ab995d1f8030cf23e58e9aa3e1db77f1b746020ee9a35abb3c9d92bc10
```
`40b8c1ab995d1f8030cf23e58e9aa3e1db77f1b746020ee9a35abb3c9d92bc10` is the key in this example. Of course, you need to modify it to the real one.

By doing this steps, the plaintext can be found!

