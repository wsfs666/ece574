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

g=2
p=0x00cc81ea8157352a9e9a318aac4e33ffba80fc8da3373fb44895109e4c3ff6cedcc55c02228fccbd551a504feb4346d2aef47053311ceaba95f6c540b967b9409e9f0502e598cfc71327c5a455e2e807bede1e0b7d23fbea054b951ca964eaecae7ba842ba1fc6818c453bf19eb9c5c86e723e69a210d4b72561cab97b3fb3060b
p=int(str(p),16)
f=sys.argv[1]
if f =="-l" :
    
    port = int(sys.argv[2])
    class handler(BaseRequestHandler):
        def handle(self):
            x_b=get_random_bytes(5)# bob random value
            x_b=int.from_bytes(x_b,byteorder='little')
            b=pow(g,x_b,p)
            """print("int b")
            print(b)
            print("byte b")
            print(b.to_bytes(200, 'little'))"""
            self.request.send(b.to_bytes(200, 'little')) #send B
            msg= self.request.recv(1024*1024)
            #print(msg)
            k=msg.split(b'/n')
            a=k[0]
            """print("byte a")
            print(a)"""
            nonce=k[1]
            #print(nonce)
            tag=k[2]
            #print(tag)
            cipher_text=k[3]
            #print(cipher_text)
            salt=k[4]
            #print(salt)
            a=int.from_bytes(a,byteorder='little')
            #print("int a ")
            #print(a)
            password=pow(a,x_b,p) #private key
            password=password.to_bytes(200, 'little')
            key = PBKDF2(password, salt, 16, count=1000000, hmac_hash_module=SHA512)
            decipher = AES.new(key, AES.MODE_GCM, nonce = nonce)
            data = decipher.decrypt_and_verify(cipher_text, tag)
            sys.stdout.buffer.write(data)
            serv.server_close()
            exit(0)
    serv = TCPServer(('localhost', port), handler)
    serv.serve_forever()
else:
    host = sys.argv[1] 
    port = int(sys.argv[2])
    sock =socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    #print("connect succeed!")
    msg = sock.recv(1024*1024)
    b=int.from_bytes(msg,byteorder='little')#receive b from bob
    #print("int b")
    #print(b)
    #print("byte b ")
    #print(msg)
    x_a=get_random_bytes(5)# alice random value
    x_a=int.from_bytes(x_a,byteorder='little')
    a=pow(g,x_a,p)
    #print("int a")
    #print(a)
    #print("byte a ")
    #print(a.to_bytes(200,'little'))
    password=pow(b,x_a,p)#private pass
    salt =get_random_bytes(16)
    password=password.to_bytes(200,'little')
    key = PBKDF2(password, salt, 16, count=1000000, hmac_hash_module=SHA512)
    cipher = AES.new(key, AES.MODE_GCM)
    nonce = cipher.nonce
    data=sys.stdin.read()
    cipher_text, tag = cipher.encrypt_and_digest(data.encode('UTF-8'))
    #print("tag")
    #print(tag)
    en_data=b'/n'+nonce+b'/n'+tag+b'/n'+cipher_text+b'/n'+salt
    sock.send(a.to_bytes(200,'little')) #send A
    sock.sendall(en_data) #send other values
    #print(en_data)
    #print(nonce)
    #print(tag)
    #print(cipher_text)
    #print(salt)
    #print(msg)
    #print(msg.split(b'/n'))
    sock.close()