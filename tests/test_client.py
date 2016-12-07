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
        create_open = Response('OK paths=1&path1=http://10.0.0.1:7500/dev1/0/1/2/0000000001.fid&fid=56320928&dev_count=1\r\n',
                               GetPathsConfig)
        with patch.object(Client, '_create_open', return_value=create_open), \
            patch('requests.put', new=fake_put):
            client = Client(Backend([]))
            file_handle = io.BytesIO(b'asdf')
            response = client.store_file(file_handle=file_handle,
                                         key='testkey',
                                         domain='testdomain')
            self.assertEqual(response, 4)

    def test_list_keys(self):
        return_value = Response('OK key_3=test_file_0.0129341319339_1480606080.74&key_21=test_file_0.634434876753_1480606271.32_4&key_count=666&next_after=after\r\n',
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
        return_value = Response('OK path1=http://10.0.0.2:7500/dev38/0/056/254/0056254995.fid&paths=2&path2=http://10.0.0.1:7500/dev54/0/056/254/0056254995.fid\r\n',
                                GetPathsConfig)
        with patch.object(Backend, 'do_request', return_value=return_value):
            client = Client(Backend([]))
            response = client.get_paths(domain='testdomain',
                                        key='test_file_0.634434876753_1480606271.32_4').data
            self.assertEqual(response['path_count'], 2)
            self.assertIn((1, 'http://10.0.0.2:7500/dev38/0/056/254/0056254995.fid'),
                          response['paths'].items())
            self.assertIn((2, 'http://10.0.0.1:7500/dev54/0/056/254/0056254995.fid'),
                          response['paths'].items())

    def test_get_file(self):
        class FakeResponse:
            raw = io.BytesIO(b'foo\r\n')
        return_value = Response('OK path1=http://10.0.0.2:7500/dev38/0/056/254/0056254995.fid&paths=2&path2=http://10.0.0.1:7500/dev54/0/056/254/0056254995.fid\r\n',
                                GetPathsConfig)
        with patch.object(requests, 'get', return_value=FakeResponse):
            with patch.object(Client, 'get_paths', return_value=return_value):
                client = Client(Backend([]))
                buf = client.get_file(domain='testdomain',
                                      key='test_file_0.634434876753_1480606271.32_4')
                self.assertEqual(buf.read(), b'foo\r\n')

    def test_get_file_no_paths(self):
        return_value = Response('OK paths=0\r\n', GetPathsConfig)
        with patch.object(Backend, 'do_request', return_value=return_value):
            with self.assertRaises(FileNotFoundError):
                Client(Backend([])).get_file(domain='testdomain',
                                             key='doesnotexist')
