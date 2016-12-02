import urllib


class Request:
    def __init__(self, config, args=None):
        self._config = config
        self._args = args or {}

    def __bytes__(self):
        args = urllib.parse.urlencode(self._args)
        return ('%s %s\r\n' % (self._config.COMMAND, args)).encode('utf-8')
