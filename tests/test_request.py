from pymogilefs.client import Hosts
from pymogilefs.request import Request
import unittest


class RequestTest(unittest.TestCase):
    def test_request_returns_bytes(self):
        request = Request(Hosts)
        self.assertIsInstance(bytes(request), bytes)

    def test_request_returns_newline_terminated_command(self):
        request = Request(Hosts)
        self.assertEqual(bytes(request), b'get_hosts \r\n')

    def test_request_with_args(self):
        request = Request(Hosts, {'test': 'foo'})
        self.assertIn(b'test=foo', bytes(request))
