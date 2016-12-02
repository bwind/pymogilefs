import urllib


class Request:
    def __init__(self, command, args=None):
        self._command = command
        self._args = args or {}

    def __bytes__(self):
        args = urllib.parse.urlencode(self._args)
        return ('%s %s\r\n' % (self._command, args)).encode('utf-8')
