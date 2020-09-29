#! /usr/bin/env python3

# Echo client program
import socket, sys, re, os

sys.path.append("../lib")       # for params
import params

from framedSock import framedSend, framedReceive

switchesVarDefaults = (
    (('-s', '--server'), 'server', "127.0.0.1:50001"),
    (('-d', '--debug'), "debug", False), # boolean (set if present)
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )


progname = "framedClient"
paramMap = params.parseParams(switchesVarDefaults)

server, usage, debug  = paramMap["server"], paramMap["usage"], paramMap["debug"]

if usage:
    params.usage()

try:
    serverHost, serverPort = re.split(":", server)
    serverPort = int(serverPort)
except:
    print("Can't parse server:port from '%s'" % server)
    sys.exit(1)

addrFamily = socket.AF_INET
socktype = socket.SOCK_STREAM
addrPort = (serverHost, serverPort)

s = socket.socket(addrFamily, socktype)

if s is None:
    print('could not open socket')
    sys.exit(1)

s.connect(addrPort)

while True:
    fd = None
    commands = os.read(0, 1024).decode()
    args = re.split('\s', commands)

    if args[0].lower() != 'put':
        os.write(2, "Incorrect args[0].\nUsage: put [file_path]\n".encode())

    elif os.path.exists(args[1]):
        with open(args[1], 'rb') as f:
            packet = f.read()
            framedSend(s,packet,debug)
    else:
        os.write(2, "Incorrect args[1].\nFile not found in specified path.\n".encode())