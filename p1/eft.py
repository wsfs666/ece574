#!/usr/bin/env python3
import sys
import socket
import os
from socketserver import TCPServer, BaseRequestHandler
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Hash import SHA512
from Crypto.Protocol.KDF import PBKDF2
import hashlib


f=sys.argv[3]
if f =="-l" :
    port = int(sys.argv[4])
    class handler(BaseRequestHandler):
        def handle(self):
            password=sys.argv[2]
            msg= self.request.recv(1024*1024)
            k=msg.split(b'/n')
            salt=bytes(k[0])
            nonce=bytes(k[1])
            tag=bytes(k[2])
            cipher_text=bytes(k[3])
            key = PBKDF2(password, salt, 16, count=1000000, hmac_hash_module=SHA512)
            decipher = AES.new(key, AES.MODE_GCM, nonce = nonce)
            try:
                data=decipher.decrypt_and_verify(cipher_text, tag)
                sys.stdout.buffer.write(data)
                self.request.send(msg)
            except ValueError:
                sys.stderr.write("Error: integrity check failed.\n")
            """print( repr(msg) )"""
            serv.server_close()
            exit(0)
    serv = TCPServer(('localhost', port), handler)
    serv.serve_forever()
else:
    host = sys.argv[3] 
    port = int(sys.argv[4])
    password=sys.argv[2]
    salt =get_random_bytes(16)
    key = PBKDF2(password, salt, 16, count=1000000, hmac_hash_module=SHA512)
    cipher = AES.new(key, AES.MODE_GCM)
    nonce = cipher.nonce
    sock =socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    print("connect succeed!")
    data=sys.stdin.read()
    cipher_text, tag = cipher.encrypt_and_digest(data.encode('UTF-8'))
    msg=salt+b'/n'+nonce+b'/n'+tag+b'/n'+cipher_text
    #print(msg)
    #print(msg.split(b'/n'))
    sock.sendall(msg)
    response = sock.recv(1024*1024)
    sock.close()
    
