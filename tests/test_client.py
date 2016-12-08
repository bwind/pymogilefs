from pymogilefs.backend import (
    Backend,
    ListKeysConfig,
    GetPathsConfig,
    CreateOpenConfig,
    CreateCloseConfig,
)
from pymogilefs.client import Client
from pymogilefs.exceptions import FileNotFoundError
from pymogilefs.response import Response
from unittest import TestCase
import io
import requests
try:
    from unittest.mock import patch
except ImportError:
    from mock import patch


class FileTestCase(TestCase):
    def test_store_file(self):
        # fake_put is used to read the full contents of `data`, in order for
        # Client.store_file to return the correct position in the file_handle
        # through seek().
        def fake_put(path, data):
            data.read()
        create_open = Response('OK paths=1&path_1=http://10.0.0.1:7500/dev1/0'
                               '/1/2/0000000001.fid&fid=56320928&dev_count=1&'
                               'devid_1=57\r\n',
                               CreateOpenConfig)
        create_close = Response('OK \r\n', CreateCloseConfig)
        with patch.object(Client, '_create_open', return_value=create_open), \
            patch.object(Client, '_create_close', return_value=create_close), \
                patch('requests.put', new=fake_put):
            client = Client(Backend([]))
            file_handle = io.BytesIO(b'asdf')
            response = client.store_file(file_handle=file_handle,
                                         key='testkey',
                                         domain='testdomain',
                                         _class='testclass')
            self.assertEqual(response, 4)

    def test_list_keys(self):
        return_value = Response('OK key_3=test_file_0.0129341319339_148060608'
                                '0.74&key_21=test_file_0.634434876753_1480606'
                                '271.32_4&key_count=666&next_after=after\r\n',
                                ListKeysConfig)
        with patch.object(Backend, 'do_request', return_value=return_value):
            client = Client(Backend([]))
            response = client.list_keys(domain='testdomain',
                                        prefix='test',
                                        after='test',
                                        limit=100).data
            self.assertEqual(response['key_count'], 666)
            self.assertEqual(response['next_after'], 'after')
            self.assertIn((3, 'test_file_0.0129341319339_1480606080.74'),
                          response['keys'].items())
            self.assertIn((21, 'test_file_0.634434876753_1480606271.32_4'),
                          response['keys'].items())

    def test_get_paths(self):
        return_value = Response('OK path1=http://10.0.0.2:7500/dev38/0/056/25'
                                '4/0056254995.fid&paths=2&path2=http://10.0.0'
                                '.1:7500/dev54/0/056/254/0056254995.fid\r\n',
                                GetPathsConfig)
        with patch.object(Backend, 'do_request', return_value=return_value):
            client = Client(Backend([]))
            key = 'test_file_0.634434876753_1480606271.32_4'
            response = client.get_paths(domain='testdomain', key=key).data
            self.assertEqual(response['path_count'], 2)
            path_1 = 'http://10.0.0.2:7500/dev38/0/056/254/0056254995.fid'
            self.assertIn((1, path_1), response['paths'].items())
            path_2 = 'http://10.0.0.1:7500/dev54/0/056/254/0056254995.fid'
            self.assertIn((2, path_2), response['paths'].items())

    def test_get_file(self):
        class FakeResponse:
            raw = io.BytesIO(b'foo\r\n')
        return_value = Response('OK path1=http://10.0.0.2:7500/dev38/0/056/25'
                                '4/0056254995.fid&paths=2&path2=http://10.0.0'
                                '.1:7500/dev54/0/056/254/0056254995.fid\r\n',
                                GetPathsConfig)
        with patch.object(requests, 'get', return_value=FakeResponse):
            with patch.object(Client, 'get_paths', return_value=return_value):
                client = Client(Backend([]))
                key = 'test_file_0.634434876753_1480606271.32_4'
                buf = client.get_file(domain='testdomain', key=key)
                self.assertEqual(buf.read(), b'foo\r\n')

    def test_get_file_no_paths(self):
        return_value = Response('OK paths=0\r\n', GetPathsConfig)
        with patch.object(Backend, 'do_request', return_value=return_value):
            with self.assertRaises(FileNotFoundError):
                Client(Backend([])).get_file(domain='testdomain',
                                             key='doesnotexist')
