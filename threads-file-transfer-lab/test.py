#! /usr/bin/env python3

import time
import os

dirname = 'client/'
files = []

if os.path.exists(dirname):
    count = 0
    for root, dirs, file_names in os.walk(dirname):
        files = [f for f in file_names]
print(files)
# start server
# os.('./file_server.py')
# './file_server.py'

# start clients
# files = ['image1.png', 'image2.png', 'image3.jpg', 'image4.jpg', 'test.txt', 'video1.mp4', 'zero-byte-file']

# for file in files:
#     os.system('./file_client.py client/' + file + ' server/' + file)

# wait for files to be created
# time.sleep(10)

# flag = False

# verify that server files have been created
# for file in files:
#     if not os.path.exists('server/'+file):
#         flag = True
#         print('server/' + file + ' has not been created successfully')

# if not flag:
#     for file in files:
#         os.remove('sever/' + file)
#     print('Successfully created all server files.\nNow testing same file.')
exit(0)