from pymogilefs.backend import (
    Backend,
    GetHostsConfig,
    CreateHostConfig,
    UpdateHostConfig,
    DeleteHostConfig,
    GetDomainsConfig,
    CreateDomainConfig,
    DeleteDomainConfig,
    CreateClassConfig,
    DeleteClassConfig,
    GetDevicesConfig,
    CreateDeviceConfig,
    SetStateConfig,
    SetWeightConfig,
)
from pymogilefs.response import Response
try:
    from unittest.mock import patch
except ImportError:
    from mock import patch
from unittest import TestCase


class HostTestCase(TestCase):
    def test_get_hosts(self):
        return_value = Response('OK host6_hostip=10.0.0.25&host6_http_port=75'
                                '00&host8_hostname=\r\n',
                                GetHostsConfig)
        with patch.object(Backend, 'do_request', return_value=return_value):
            hosts = Backend([]).get_hosts().data
            expected = [{'hostip': '10.0.0.25', 'http_port': '7500'},
                        {'hostname': ''}]
            self.assertIn(expected[0], hosts['hosts'].values())
            self.assertIn(expected[1], hosts['hosts'].values())

    def test_create_host(self):
        return_value = Response('OK hostid=4&hostname=localhost\r\n',
                                CreateHostConfig)
        with patch.object(Backend, 'do_request', return_value=return_value):
            response = Backend([]).create_host(host='localhost',
                                               ip='0.0.0.0',
                                               port=7001).data
            expected = {'id': '4', 'name': 'localhost'}
            self.assertEqual(response, expected)

    def test_update_host(self):
        return_value = Response('OK hostid=7&hostname=hostname\r\n',
                                UpdateHostConfig)
        with patch.object(Backend, 'do_request', return_value=return_value):
            response = Backend([]).update_host(host='localhost',
                                               ip='0.0.0.0',
                                               port=7001).data
            expected = {'id': '7', 'name': 'hostname'}
            self.assertEqual(response, expected)

    def test_delete_host(self):
        return_value = Response('OK \r\n', DeleteHostConfig)
        with patch.object(Backend, 'do_request', return_value=return_value):
            response = Backend([]).delete_host(host='localhost').data
            self.assertEqual(response, {})


class DomainTestCase(TestCase):
    def test_get_domains(self):
        return_value = Response('OK domain15class1name=default&domain25class1'
                                'name=default&domain41class1mindevcount=2\r\n',
                                GetDomainsConfig)
        with patch.object(Backend, 'do_request', return_value=return_value):
            domains = Backend([]).get_domains().data['domains']
            self.assertEqual(domains[15]['classes'][1]['name'], 'default')
            self.assertEqual(domains[25]['classes'][1]['name'], 'default')
            self.assertEqual(domains[41]['classes'][1]['mindevcount'], '2')

    def test_create_domain(self):
        return_value = Response('OK domain=testdomain\r\n', CreateDomainConfig)
        with patch.object(Backend, 'do_request', return_value=return_value):
            domains = Backend([]).create_domain('testdomain').data
            expected = {'domain': 'testdomain'}
            self.assertEqual(domains, expected)

    def test_delete_domain(self):
        return_value = Response('OK domain=testdomain\r\n', DeleteDomainConfig)
        with patch.object(Backend, 'do_request', return_value=return_value):
            domains = Backend([]).delete_domain('testdomain').data
            expected = {'domain': 'testdomain'}
            self.assertEqual(domains, expected)


class ClassTestCase(TestCase):
    def test_create_class(self):
        return_value = Response('OK mindevcount=2&domain=testdomain&class=tes'
                                'tclass\r\n',
                                CreateClassConfig)
        with patch.object(Backend, 'do_request', return_value=return_value):
            classes = Backend([]).create_class(domain='testdomain',
                                               _class='testclass',
                                               mindevcount=2).data
            expected = {'mindevcount': '2',
                        'domain': 'testdomain',
                        'class': 'testclass'}
            self.assertEqual(expected, classes)

    def test_update_class(self):
        return_value = Response('OK mindevcount=3&domain=testdomain&class=tes'
                                'tclass\r\n',
                                CreateClassConfig)
        with patch.object(Backend, 'do_request', return_value=return_value):
            classes = Backend([]).update_class(domain='testdomain',
                                               _class='testclass',
                                               mindevcount=3).data
            expected = {'mindevcount': '3',
                        'domain': 'testdomain',
                        'class': 'testclass'}
            self.assertEqual(expected, classes)

    def test_delete_class(self):
        return_value = Response('OK domain=testdomain&class=testclass\r\n',
                                DeleteClassConfig)
        with patch.object(Backend, 'do_request', return_value=return_value):
            classes = Backend([]).delete_class('testdomain', 'testclass').data
            expected = {'domain': 'testdomain', 'class': 'testclass'}
            self.assertEqual(classes, expected)


class DeviceTestCase(TestCase):
    def test_get_devices(self):
        return_value = Response('OK dev27_mb_asof=&dev27_mb_total=1870562&dev'
                                '26_mb_used=76672\r\n',
                                GetDevicesConfig)
        with patch.object(Backend, 'do_request', return_value=return_value):
            devices = Backend([]).get_devices().data
            expected = [{'mb_asof': '', 'mb_total': '1870562'},
                        {'mb_used': '76672'}]
            self.assertIn(expected[0], devices['devices'].values())
            self.assertIn(expected[1], devices['devices'].values())

    def test_create_device(self):
        return_value = Response('OK \r\n', CreateDeviceConfig)
        with patch.object(Backend, 'do_request', return_value=return_value):
            response = Backend([]).create_device(hostname='testhost10',
                                                 devid=6,
                                                 hostip='0.0.0.0',
                                                 state='alive').data
            self.assertEqual(response, {})


class SetStateTestCase(TestCase):
    def test_set_state(self):
        return_value = Response('OK \r\n', SetStateConfig)
        with patch.object(Backend, 'do_request', return_value=return_value):
            response = Backend([]).set_state(host='localhost',
                                             device=7,
                                             state='down').data
            self.assertEqual(response, {})


class SetWeightTestCase(TestCase):
    def test_set_weight(self):
        return_value = Response('OK \r\n', SetWeightConfig)
        with patch.object(Backend, 'do_request', return_value=return_value):
            response = Backend([]).set_weight(host='testhost10',
                                              device=6,
                                              weight=8).data
            self.assertEqual(response, {})
