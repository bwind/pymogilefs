from pymogilefs.client import Client
from unittest import TestCase


#class FileTestCase(TestCase):
#    @skip(reason='WIP')
#    def test_store_file(self):
#        client = Client(['mogtrack0.acc.telegraaf.net:7001'])
#        #client = Client(['0.0.0.0:7001'])
#        file_handle = io.BytesIO(b'asdf')
#        response = client.store_file(file_handle=file_handle,
#                                     key='testkey',
#                                     domain='testdomain')
#        self.assertEqual(response, 4)
