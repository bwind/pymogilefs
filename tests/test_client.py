from pymogilefs.backend import Backend
from pymogilefs.client import (
    Client,
    GetHostsConfig,
    CreateHostConfig,
    UpdateHostConfig,
    DeleteHostConfig,
    GetDomainsConfig,
    CreateDomainConfig,
    DeleteDomainConfig,
    CreateClassConfig,
    GetDevicesConfig,
)
from pymogilefs.response import Response
from unittest.mock import patch
from unittest import TestCase


class HostTestCase(TestCase):
    def test_get_hosts(self):
        return_value = Response('OK host6_hostip=10.0.0.25&host6_http_port=7500&host8_hostname=\r\n',
                                GetHostsConfig)
        with patch.object(Backend, 'do_request', return_value=return_value):
            hosts = Client([]).get_hosts()
            expected = [{'hostip': '10.0.0.25', 'http_port': '7500'},
                        {'hostname': ''}]
            self.assertIn(expected[0], hosts)
            self.assertIn(expected[1], hosts)

    def test_create_host(self):
        return_value = Response('OK hostid=4&hostname=localhost\r\n',
                                CreateHostConfig)
        with patch.object(Backend, 'do_request', return_value=return_value):
            response = Client([]).create_host(host='localhost',
                                              ip='0.0.0.0',
                                              port=7001)
            expected = [{'id': '4', 'name': 'localhost'}]
            self.assertEqual(response, expected)

    def test_update_host(self):
        return_value = Response('OK hostid=7&hostname=hostname\r\n',
                                UpdateHostConfig)
        with patch.object(Backend, 'do_request', return_value=return_value):
            response = Client([]).update_host(host='localhost',
                                              ip='0.0.0.0',
                                              port=7001)
            expected = [{'id': '7', 'name': 'hostname'}]
            self.assertEqual(response, expected)

    def test_delete_host(self):
        return_value = Response('OK \r\n',
                                DeleteHostConfig)
        with patch.object(Backend, 'do_request', return_value=return_value):
            response = Client([]).delete_host(host='localhost')
            self.assertEqual(response, {})


class DomainTestCase(TestCase):
    def test_get_domains(self):
        return_value = Response('OK domain15class1name=default&domain25class1name=default&domain41class1mindevcount=2\r\n',
                                GetDomainsConfig)
        with patch.object(Backend, 'do_request', return_value=return_value):
            domains = Client([]).get_domains()
            expected = [{'class1name': 'default'},
                        {'class1name': 'default'},
                        {'class1mindevcount': '2'}]
            self.assertIn(expected[0], domains)
            self.assertIn(expected[1], domains)
            self.assertIn(expected[2], domains)

    def test_create_domain(self):
        return_value = Response('OK domain=testdomain\r\n', CreateDomainConfig)
        with patch.object(Backend, 'do_request', return_value=return_value):
            domains = Client([]).create_domain('testdomain')
            expected = [{'domain': 'testdomain'}]
            self.assertEqual(domains, expected)

    def test_delete_domain(self):
        return_value = Response('OK domain=testdomain\r\n', DeleteDomainConfig)
        with patch.object(Backend, 'do_request', return_value=return_value):
            domains = Client([]).delete_domain('testdomain')
            expected = [{'domain': 'testdomain'}]
            self.assertEqual(domains, expected)


class ClassTestCase(TestCase):
    def test_create_class(self):
        return_value = Response('OK mindevcount=2&domain=testdomain&class=testclass\r\n', CreateClassConfig)
        with patch.object(Backend, 'do_request', return_value=return_value):
            classes = Client([]).create_class(domain='testdomain',
                                              _class='testclass',
                                               mindevcount=2)
            expected = {'mindevcount': '2',
                        'domain': 'testdomain',
                        'class': 'testclass'}
            self.assertEqual(expected, classes[0])

    def test_update_class(self):
        return_value = Response('OK mindevcount=3&domain=testdomain&class=testclass\r\n', CreateClassConfig)
        with patch.object(Backend, 'do_request', return_value=return_value):
            classes = Client([]).update_class(domain='testdomain',
                                              _class='testclass',
                                              mindevcount=3)
            expected = {'mindevcount': '3',
                        'domain': 'testdomain',
                        'class': 'testclass'}
            self.assertEqual(expected, classes[0])

    def test_delete_class(self):
        raise NotImplementedError


class DeviceTestCase(TestCase):
    def test_get_devices(self):
        return_value = Response('OK dev27_mb_asof=&dev27_mb_total=1870562&dev26_mb_used=76672\r\n',
                                GetDevicesConfig)
        with patch.object(Backend, 'do_request', return_value=return_value):
            devices = Client([]).get_devices()
            expected = [{'mb_asof': '', 'mb_total': '1870562'},
                        {'mb_used': '76672'}]
            self.assertIn(expected[0], devices)
            self.assertIn(expected[1], devices)

    def test_create_device(self):
        raise NotImplementedError


class SetStateTestCase(TestCase):
    def test_set_state(self):
        raise NotImplementedError


class SetWeightTestCase(TestCase):
    def test_set_weight(self):
        raise NotImplementedError
