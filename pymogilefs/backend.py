from pymogilefs.connection import Connection
from pymogilefs.exceptions import NoTrackersAvailableError
import random

"""
Backend manages a pool of trackers and balances load between them.
"""

# TODO: mark tracker as dead


MAX_RETRIES = 5


class Backend:
    def __init__(self, trackers):
        self._trackers = [tracker.split(':') for tracker in trackers]

    def _get_connection(self):
        # TODO: Try random trackers, implement retries
        host, port = self._trackers[0]
        connection = Connection(host, port)
        connection._connect()
        return connection

    def do_request(self, request):
        return self._get_connection().do_request(request)
