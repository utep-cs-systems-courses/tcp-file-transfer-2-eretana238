#! /usr/bin/env python3

import sys
sys.path.append("../lib")       # for params
import re, socket, params, os

switchesVarDefaults = (
    (('-l', '--listenPort') ,'listenPort', 50001),
    (('-d', '--debug'), "debug", False), # boolean (set if present)
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )

progname = "echoserver"
paramMap = params.parseParams(switchesVarDefaults)

debug, listenPort = paramMap['debug'], paramMap['listenPort']

if paramMap['usage']:
    params.usage()

lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # listener socket
bindAddr = ("127.0.0.1", listenPort)
lsock.bind(bindAddr)
lsock.listen(5)
print("listening on:", bindAddr)

while True:
    sock, addr = lsock.accept()
    print("connection rec'd from", addr)
    from framedSock import framedSend, framedReceive
    if not os.fork():
        remote_name, payload = framedReceive(sock, debug)
        if debug: print("rec'd: ", payload)
        if not payload or not remote_name:
            break
        binary_format = bytearray(payload)
        with open(remote_name, 'w+b') as nf:
            print('File data in buffer. Now creating file.')
            nf.write(binary_format)
            nf.close()
