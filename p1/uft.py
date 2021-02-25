#!/usr/bin/python3
import sys
import socket
import os
from socketserver import TCPServer, BaseRequestHandler


f=sys.argv[1]
if f =="-l" :
    port = int(sys.argv[2])
    class handler(BaseRequestHandler):
        def handle(self):
            msg = self.request.recv(1024*1024)
            sys.stdout.buffer.write(msg)
            self.request.send(msg)
            """print( repr(msg) )"""
            serv.server_close()
            exit(0)
    serv = TCPServer(('localhost', port), handler)
    serv.serve_forever()
else:
    host = sys.argv[1] 
    port = int(sys.argv[2]) 
    sock =socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    print("connect succeed!")
    msg=sys.stdin.read()
    sock.sendall(msg.encode('UTF-8'))
    response = sock.recv(1024*1024)
    """print( repr(response) )"""
    sock.close()
     
