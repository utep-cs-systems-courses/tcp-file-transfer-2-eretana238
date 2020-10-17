#! /usr/bin/env python3

import params
from framed_sock import EncapFramedSock
import socket
import sys
from threading import Thread
from threading import Lock
sys.path.append("../lib")       # for params


switchesVarDefaults = (
    (('-l', '--listenPort'), 'listenPort', 50001),
    (('-d', '--debug'), "debug", False),  # boolean (set if present)
    (('-?', '--usage'), "usage", False),  # boolean (set if present)
)

paramMap = params.parseParams(switchesVarDefaults)

debug, listenPort = paramMap['debug'], paramMap['listenPort']

if paramMap['usage']:
    params.usage()

lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # listener socket
bindAddr = ("127.0.0.1", listenPort)
lsock.bind(bindAddr)
lsock.listen(5)
print("listening on:", bindAddr)


class Server(Thread):
    def __init__(self, sockAddr) -> None:
        Thread.__init__(self)
        self.sock, self.addr = sockAddr
        self.fsock = EncapFramedSock(sockAddr)

    def run(self) -> None:
        print("new thread handling connection from", self.addr)
        while True:
            remote_name, payload = self.fsock.framed_receive(debug)
            if debug:
                print("rec'd: ", payload)
            if not payload or not remote_name:     # done
                if debug:
                    print(f"thread connected to {self.addr} done")
                self.fsock.close()
                return          # exit
            binary_format = bytearray(payload)

            data_lock = Lock()
            with data_lock:
                with open(remote_name.decode(), 'w+b') as nf:
                    nf.write(binary_format)


while True:
    sockAddr = lsock.accept()
    server = Server(sockAddr)
    server.start()
