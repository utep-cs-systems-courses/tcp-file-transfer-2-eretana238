#! /usr/bin/env python3

# directory location may depend on machine

from framed_sock import EncapFramedSock
from os import sendfile
import socket
import sys
import re
import os
sys.path.append("../lib")       # for params
import params


class Client():
    """
    Represents the client that connects to the server and makes a file transfer

    Args:
        server(str): server connection, address and port
    """

    def __init__(self, server) -> None:
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

    def send_file(self, local_file, remote_file, debug=False) -> None:
        """
        Sends a message composed of the file bytes and the name of the (new) transfered file

        Args:
            local_file(str): the location of the file to be read and transferred to the server
            remote_file(str): the location of the file to be created in the server
        """
        with open(local_file, 'rb') as f:
            data = f.read()
            self.fsock.framed_send(data, remote_file, debug)


if __name__ == "__main__":
    switchesVarDefaults = (
        (("-s", "--server"), "server", "127.0.0.1:50001"),
        (("-d", "--debug"), "debug", False),  # boolean (set if present)
        (("-?", "--usage"), "usage", False),  # boolean (set if present)
    )

    paramMap = params.parseParams(switchesVarDefaults)
    server, usage, debug = paramMap["server"], paramMap["usage"], paramMap["debug"]

    if usage:
        params.usage()

    client = Client(server)

    while True:
        command = os.read(0, 1024).decode()
        if command.startswith('exit') or command.startswith('quit'):
            sys.exit(1)

        args = re.match('(.*) (.*) (.*)', command)

        if not args:
            print(
                'Incorrect number of arguments.\nUsage: put [local_name] [remote_name]')
            continue
        else:
            args = args.groups()

        if args[0].lower() != 'put':
            print('Incorrect args[0].\nUsage: put [local_name] [remote_name]')
            continue

        elif not os.path.exists(args[1]):
            print('Incorrect args[1].\nFile not found in specified path.')
            continue

        else:
            if os.path.getsize(args[1]) == 0:
                print('Zero byte file blah.\nNo point on transferring')
                continue
            client.send_file(args[1], args[2], debug)
