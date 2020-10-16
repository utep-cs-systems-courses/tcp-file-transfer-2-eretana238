#! /usr/bin/env python3
from file_client import Client
import sys
sys.path.append("../lib")       # for params
import params

# check number of arguments
if len(sys.argv) < 3:
    print('Invalid number of args. Must be at least 3.')
    exit(1)

# switchesVarDefaults = (
#     (("-s", "--server"), "server", "127.0.0.1:50001"),
#     (("-d", "--debug"), "debug", False),  # boolean (set if present)
#     (("-?", "--usage"), "usage", False),  # boolean (set if present)
# )

# paramMap = params.parseParams(switchesVarDefaults)
# server, usage, debug = paramMap["server"], paramMap["usage"], paramMap["debug"]

# if usage:
#     params.usage()

client = Client(debug=0)
client.send_file(sys.argv[3], sys.argv[4])
