from pymogilefs.response import Response
from pymogilefs.request import Request
import socket


BUFSIZE = 4096
TIMEOUT = 10


class Connection:
    def __init__(self, host, port):
        self._host = host
        self._port = int(port)

    def _connect(self):
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.connect((self._host, self._port))
        self._sock.settimeout(TIMEOUT)

    def _recv_all(self):
        response_text = b''
        while True:
            received = self._sock.recv(BUFSIZE)
            if received == b'':
                break
            response_text += received
            if response_text[-2:] == b'\r\n':
                break
        return response_text.decode()

    def do_request(self, request):
        assert isinstance(request, Request)
        self._sock.send(bytes(request))
        response_text = self._recv_all()
        self._sock.close()
        return Response(response_text, request.config)
