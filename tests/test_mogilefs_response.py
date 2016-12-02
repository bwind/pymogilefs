from pymogilefs.client import Hosts
from pymogilefs.exceptions import RequestError
from pymogilefs.mogilefs_response import MogilefsResponse
import unittest


class MogilefsResponseTest(unittest.TestCase):
    def test_instantiate_with_bytes(self):
        buf = b'OK host1_hostip=10.0.0.25'
        with self.assertRaises(AssertionError):
            MogilefsResponse(buf)

    def test_instantiate_with_str(self):
        buf = 'OK host1_hostip=10.0.0.25'
        MogilefsResponse(buf)

    def test_instantiate_with_error(self):
        buf = 'ERR unknown_command Unknown+server+command\r\n'
        with self.assertRaises(RequestError):
            MogilefsResponse(buf)

    def test_parse_response_text(self):
        response = MogilefsResponse('OK host6_hostip=10.0.0.25&'
                                    'host6_http_port=7500&host8_hostname=\r\n',
                                    Hosts.PREFIX_RE)
        expected = [{'hostip': '10.0.0.25', 'http_port': '7500'},
                    {'hostname': ''}]
        self.assertIn(expected[0], response.items)
        self.assertIn(expected[1], response.items)
