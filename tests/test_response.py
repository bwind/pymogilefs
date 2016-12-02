from pymogilefs.client import GetHostsConfig
from pymogilefs.exceptions import RequestError
from pymogilefs.response import Response
import unittest


class ResponseTest(unittest.TestCase):
    def test_instantiate_with_bytes(self):
        response_text = b'OK host1_hostip=10.0.0.25'
        with self.assertRaises(AssertionError):
            Response(response_text, GetHostsConfig)

    def test_instantiate_with_str(self):
        response_text = 'OK host1_hostip=10.0.0.25'
        Response(response_text, GetHostsConfig)

    def test_instantiate_with_error(self):
        response_text = 'ERR unknown_command Unknown+server+command\r\n'
        with self.assertRaises(RequestError):
            Response(response_text, GetHostsConfig)

    def test_parse_response_text(self):
        response = Response('OK host6_hostip=10.0.0.25&'
                            'host6_http_port=7500&host8_hostname=\r\n',
                            GetHostsConfig)
        expected = [{'hostip': '10.0.0.25', 'http_port': '7500'},
                    {'hostname': ''}]
        self.assertIn(expected[0], response.items)
        self.assertIn(expected[1], response.items)
