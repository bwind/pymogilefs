from pymogilefs.connection import Connection


class Backend:
    def __init__(self, trackers):
        self._trackers = [tracker.split(':') for tracker in trackers]

    def get_connection(self):
        host, port, = self._trackers[0]
        connection = Connection(host, port)
        connection._connect()
        return connection
