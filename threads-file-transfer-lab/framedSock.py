import re

class EncapFramedSock:               # a facade
    def __init__(self, sockAddr) -> None:
        self.sock, self.addr = sockAddr
        self.rbuf = b''         # receive buffer

    def close(self) -> int:
        return self.sock.close()

    def send(self, payload, remote_name = 'None', debug=0) -> None:
        if debug:
            print('framedSend: sending %d byte message' % len(payload))
        msg = str(len(payload)).encode() + b':' + \
            remote_name.encode() + b':' + payload
        while len(msg):
            nsent = self.sock.send(msg)
            msg = msg[nsent:]

    def receive(self, debug=0) -> None:
        state = 'getLength'
        msgLength = -1
        remote_name = ''
        while True:
            if state == 'getLength':
                match = re.match(b'([^:]+):(.*):(.*)', self.rbuf,
                                re.DOTALL | re.MULTILINE)  # look for header
                if match:
                    lengthStr, remote_name, rbuf = match.groups()
                    try:
                        msgLength = int(lengthStr)
                    except:
                        if len(rbuf):
                            print('badly formed message length:', lengthStr)
                            return None, None
                    state = 'getPayload'
            if state == 'getPayload':
                if len(self.rbuf) >= msgLength:
                    payload = self.rbuf[0:msgLength]
                    rbuf = self.rbuf[msgLength:]
                    return remote_name, payload
            r = self.sock.recv(100)
            self.rbuf += r
            if len(r) == 0:
                if len(self.rbuf) != 0:
                    print('FramedReceive: incomplete message.\n state=%s, length=%d' % (
                        state, msgLength))
                return None, None
            if debug:
                print('FramedReceive: state=%s, length=%d, rbuf=%s' %
                    (state, msgLength, self.rbuf))

    
