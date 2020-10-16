#! /home/silverlycan/os/tcp-file-transfer-2-eretana238/threads-file-transfer-lab/interpreter.py

# directory location may depend on machine

import socket
import sys
import re
import os
from framed_sock import EncapFramedSock
sys.path.append("../lib")       # for params
import params

class Client():
    """
    Represents the client that connects to the server and makes a file transfer
    """
    def __init__(self, server = "127.0.0.1:50001", debug = 0) -> None:
        self.debug = debug
        try:
            server_host, server_port = re.split(":", server)
            server_port = int(server_port)
        except:
            print("Can't parse server:port from '%s'" % server)
            sys.exit(1)

        addr_port = (server_host, server_port)
        addr_family = socket.AF_INET
        sock_type = socket.SOCK_STREAM
        
        sock = socket.socket(addr_family, sock_type)
        sock.connect(addr_port)
        
        self.fsock = EncapFramedSock((sock, addr_port))

    def send_file(self,local_file, remote_file) -> None:
        """
        docstring
        """
        if os.path.getsize(local_file) == 0:
            print('Zero byte file blah.\nNo point on transferring')
        with open(local_file, 'rb') as f:
            data = f.read()
            self.fsock.framed_send(data, remote_file, self.debug)