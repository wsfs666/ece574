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
import io


server_port= int(sys.argv[4])
proxy_port= int(sys.argv[2])
host=sys.argv[3]
g=2
p=0x00cc81ea8157352a9e9a318aac4e33ffba80fc8da3373fb44895109e4c3ff6cedcc55c02228fccbd551a504feb4346d2aef47053311ceaba95f6c540b967b9409e9f0502e598cfc71327c5a455e2e807bede1e0b7d23fbea054b951ca964eaecae7ba842ba1fc6818c453bf19eb9c5c86e723e69a210d4b72561cab97b3fb3060b
p=int(str(p),16)

##receive data from client
class handler(BaseRequestHandler):
    def handle(self):
        print("start proxy....")
        x_b=get_random_bytes(5)# bob random value
        x_b=int.from_bytes(x_b,byteorder='little')
        b=pow(g,x_b,p)
        self.request.send(b.to_bytes(200, 'little')) #send B to client
        msg= self.request.recv(1024*1024)
        #print(msg)
        k=msg.split(b'/n')
        a=k[0]
            
        nonce=k[1]
            
        tag=k[2]
            
        cipher_text=k[3]
            
        salt=k[4]
            
        a=int.from_bytes(a,byteorder='little')
            
            
        password=pow(a,x_b,p) #private key
        password=password.to_bytes(200, 'little')
        key = PBKDF2(password, salt, 16, count=1000000, hmac_hash_module=SHA512)
        decipher = AES.new(key, AES.MODE_GCM, nonce = nonce)
        data = decipher.decrypt_and_verify(cipher_text, tag)
        
        print("decrept data from client.....")
        print(data.decode('utf-8'))

        #encreption
#send data to server
        sock2 =socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock2.connect((host, server_port))#connect to server
        msg = sock2.recv(1024*1024)
        b=int.from_bytes(msg,byteorder='little')#receive b from bob
        x_a=get_random_bytes(5)# alice random value
        x_a=int.from_bytes(x_a,byteorder='little')
        a=pow(g,x_a,p)
        password=pow(b,x_a,p)#private pass
        salt =get_random_bytes(16)
        password=password.to_bytes(200,'little')
        key = PBKDF2(password, salt, 16, count=1000000, hmac_hash_module=SHA512)
        cipher = AES.new(key, AES.MODE_GCM)
        nonce = cipher.nonce
        print("re_encrept data to server.....")
        
        #data="hukhvolh"
        
        cipher_text, tag = cipher.encrypt_and_digest(data)
    
        en_data=b'/n'+nonce+b'/n'+tag+b'/n'+cipher_text+b'/n'+salt
        sock2.send(a.to_bytes(200,'little')) #send A
        sock2.sendall(en_data) #send other values
        sock2.close()
        
        serv.server_close()
        exit(0)


serv = TCPServer(('localhost', proxy_port), handler)#create proxy as server


serv.serve_forever()








   




