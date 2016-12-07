from pymogilefs.connection import Connection
import unittest


class ConnectionTest(unittest.TestCase):
    def test_do_request_requires_request_instance(self):
        connection = Connection('host', 1)
        with self.assertRaises(AssertionError):
            connection.do_request('test')
