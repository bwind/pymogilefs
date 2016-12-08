from pymogilefs.connection import Connection
import io
import socket
import unittest
try:
    from unittest import mock
except ImportError:
    import mock


class ConnectionTest(unittest.TestCase):
    def test_do_request_requires_request_instance(self):
        connection = Connection('host', 1)
        with self.assertRaises(AssertionError):
            connection.do_request('test')

    def test_connect(self):
        connection = Connection('host', 1)
        with mock.patch('socket.socket'):
            connection._connect()
            connection._sock.connect.assert_called_with(('host', 1))

    def test_no_socket_on_instantiation(self):
        connection = Connection('host', 1)
        self.assertFalse(hasattr(connection, '_sock'))

    def test_connect_settimeout(self):
        connection = Connection('host', 1)
        with mock.patch('socket.socket'):
            connection._connect()
            connection._sock.settimeout.assert_called_with(10)

    def test_recv_all(self):
        connection = Connection('host', 1)
        connection._sock = mock.MagicMock()
        connection._sock.recv = lambda buf_size: b'foo\r\n'
        response = connection._recv_all()
        expected = 'foo\r\n'
        self.assertEqual(response, expected)

    def test_recv_all_large(self):
        connection = Connection('host', 1)
        connection._sock = mock.MagicMock()
        connection._sock.recv = lambda buf_size: (b'foo' * 1500) + b'\r\n'
        response = connection._recv_all()
        expected = ('foo' * 1500) + '\r\n'
        self.assertEqual(response, expected)

    def test_recv_all_no_newline(self):
        connection = Connection('host', 1)
        connection._sock = mock.MagicMock()
        buf = io.BytesIO(b'foo')
        connection._sock.recv = lambda buf_size: buf.read()
        response = connection._recv_all()
        expected = 'foo'
        self.assertEqual(response, expected)
