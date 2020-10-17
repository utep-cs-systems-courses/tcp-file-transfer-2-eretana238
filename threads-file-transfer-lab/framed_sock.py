import re

class EncapFramedSock:               # a facade
    def __init__(self, sockAddr) -> None:
        self.sock, self.addr = sockAddr
        self.rbuf = b''         # receive buffer

    def close(self) -> int:
        return self.sock.close()

    def framed_send(self, payload, remote_name = 'None', debug=0) -> None:
        msg = str(len(payload)).encode() + b':' + \
            remote_name.encode() + b':' + payload
        while len(msg):
            nsent = self.sock.send(msg)
            msg = msg[nsent:]
        if debug:
            print('Sent {:.2f}kb'.format(len(payload)/1000))

    def framed_receive(self, debug=0) -> None:
        state = 'getLength'
        self.msgLength = -1
        remote_name = ''
        counter = -1
        while True:
            if state == 'getLength':
                match = re.match(b'([^:]+):(.*):(.*)', self.rbuf,
                                re.DOTALL | re.MULTILINE)  # look for header
                if match:
                    lengthStr, remote_name, self.rbuf = match.groups()
                    counter = len(self.rbuf)
                    try:
                        self.msgLength = int(lengthStr)
                    except:
                        if len(self.rbuf):
                            print('badly formed message length:', lengthStr)
                            return None, None
                    state = 'getPayload'
            if state == 'getPayload':
                if len(self.rbuf) >= self.msgLength:
                    payload = self.rbuf[0:self.msgLength]
                    self.rbuf = self.rbuf[self.msgLength:]
                    return remote_name, payload
            r = self.sock.recv(100)
            self.rbuf += r
            if len(r) == 0:
                if len(self.rbuf) != 0:
                    print('FramedReceive: incomplete message.\n state=%s, length=%d' % (
                        state, self.msgLength))
                return None, None
            if debug:
                if counter != -1 and counter % 1000 == 0:
                    print('{} of {}'.format(len(self.rbuf), self.msgLength))
                counter += 1

