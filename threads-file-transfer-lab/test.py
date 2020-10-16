import time
import os

# start server
exec(open('./file_server.py').read())

# start clients
files = ['image1.png', 'image2.png', 'image3.jpg', 'image4.jpg', 'test.txt', 'video1.mp4', 'zero-byte-file']

for file in files:
    os.system('./file_client.py client/' + file + ' server/' + file)

# wait for files to be created
time.sleep(10)

flag = False

# verify that server files have been created
for file in files:
    if not os.path.exists('server/'+file):
        flag = True
        print('server/' + file + ' has not been created successfully')

if not flag:
    print('Successfully created all server files.\nNow testing')
