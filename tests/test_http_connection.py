from pymogilefs import http_connection
import unittest
import io
try:
    from unittest.mock import patch
except ImportError:
    from mock import patch


class HttpConnectionTest(unittest.TestCase):
    def test_chunked_encoding(self):
        body = io.BytesIO(b'asdf_test_foo_hi')
        with patch.object(http_connection, 'CHUNK_SIZE', 5):
            conn = http_connection.HttpConnection(None, None)
            chunks = [chunk for chunk in
                      conn._generator_from_file_handle(body)]
            self.assertEqual(chunks, [b'asdf_', b'test_', b'foo_h', b'i'])
