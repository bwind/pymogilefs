from pymogilefs.backend import Backend
from pymogilefs.client import Client
from pymogilefs.mogilefs_response import MogilefsResponse
from unittest.mock import MagicMock
from unittest import TestCase


class ClientTest(TestCase):
    def test_get_hosts_dict(self):
        return_value = MogilefsResponse('OK host6_hostip=10.0.0.25&host6_http_port=7500&host8_hostname=\r\n')
        Backend.do_request = MagicMock(return_value=return_value)
        hosts = Client([]).get_hosts()
        expected = [
            {
                'hostip': '10.0.0.25',
                'http_port': '7500',
            },
            {
                'hostname': '',
            },
        ]
        self.assertEqual(hosts, expected)
