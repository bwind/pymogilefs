from pymogilefs.backend import Backend
from pymogilefs.client import (
    Client,
    GetHostsConfig,
    CreateHostConfig,
    GetDomainsConfig,
    GetDevicesConfig,
)
from pymogilefs.response import Response
from unittest.mock import MagicMock
from unittest import TestCase


class HostTestCase(TestCase):
    def test_get_hosts(self):
        return_value = Response('OK host6_hostip=10.0.0.25&host6_http_port=7500&host8_hostname=\r\n',
                                GetHostsConfig)
        Backend.do_request = MagicMock(return_value=return_value)
        hosts = Client([]).get_hosts()
        expected = [{'hostip': '10.0.0.25', 'http_port': '7500'},
                    {'hostname': ''}]
        self.assertIn(expected[0], hosts)
        self.assertIn(expected[1], hosts)

    def test_create_host(self):
        return_value = Response('OK hostid=4&hostname=localhost\r\n',
                                CreateHostConfig)
        Backend.do_request = MagicMock(return_value=return_value)
        response = Client([]).create_host(host='localhost',
                                          ip='0.0.0.0',
                                          port=7001)
        expected = [{'id': '4', 'name': 'localhost'}]
        self.assertEqual(response, expected)


class DomainTestCase(TestCase):
    def test_get_domains(self):
        return_value = Response('OK domain15class1name=default&domain25class1name=default&domain41class1mindevcount=2\r\n',
                                GetDomainsConfig)
        Backend.do_request = MagicMock(return_value=return_value)
        domains = Client([]).get_domains()
        expected = [{'class1name': 'default'},
                    {'class1name': 'default'},
                    {'class1mindevcount': '2'}]
        self.assertIn(expected[0], domains)
        self.assertIn(expected[1], domains)
        self.assertIn(expected[2], domains)


class DeviceTestCase(TestCase):
    def test_get_devices(self):
        return_value = Response('OK dev27_mb_asof=&dev27_mb_total=1870562&dev26_mb_used=76672\r\n',
                                GetDevicesConfig)
        Backend.do_request = MagicMock(return_value=return_value)
        devices = Client([]).get_devices()
        expected = [{'mb_asof': '', 'mb_total': '1870562'},
                    {'mb_used': '76672'}]
        self.assertIn(expected[0], devices)
        self.assertIn(expected[1], devices)
