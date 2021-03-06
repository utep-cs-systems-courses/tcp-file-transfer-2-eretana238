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
    command = os.read(0, 1024).decode()
    if command == 'exit' or command == 'quit':
        sys.exit(1)

    args = re.match('(.*) (.*) (.*)', command)

    if not args:
        print('Incorrect number of arguments.\nUsage: put [local_name] [remote_name]')
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
        with open(args[1], 'rb') as f:
            data = f.read()
            framedSend(s,args[2],data,debug)