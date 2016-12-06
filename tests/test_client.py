from pymogilefs.backend import Backend, ListKeysConfig
from pymogilefs.client import Client
from pymogilefs.response import Response
from unittest import TestCase
try:
    from unittest.mock import patch
except ImportError:
    from mock import patch


class FileTestCase(TestCase):
#    @skip(reason='WIP')
#    def test_store_file(self):
#        client = Client(['mogtrack0.acc.telegraaf.net:7001'])
#        #client = Client(['0.0.0.0:7001'])
#        file_handle = io.BytesIO(b'asdf')
#        response = client.store_file(file_handle=file_handle,
#                                     key='testkey',
#                                     domain='testdomain')
#        self.assertEqual(response, 4)

    def test_list_keys(self):
        return_value = Response('OK key_3=test_file_0.0129341319339_1480606080.74&key_21=test_file_0.634434876753_1480606271.32_4&key_count=666&next_after=after\r\n',
                                ListKeysConfig)
        with patch.object(Backend, 'do_request', return_value=return_value):
            response = Client(Backend([])).list_keys(domain='testdomain',
                                                     prefix='test',
                                                     after='test',
                                                     limit=100).data
            self.assertEqual(response['key_count'], 666)
            self.assertEqual(response['next_after'], 'after')
            self.assertIn((3, 'test_file_0.0129341319339_1480606080.74'),
                          response['keys'].items())
            self.assertIn((21, 'test_file_0.634434876753_1480606271.32_4'),
                          response['keys'].items())
