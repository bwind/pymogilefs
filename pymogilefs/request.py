try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode


class Request:
    def __init__(self, config, **kwargs):
        self.config = config
        self._kwargs = kwargs or {}

    def __bytes__(self):
        kwargs = urlencode(self._kwargs)
        return ('%s %s\r\n' % (self.config.COMMAND, kwargs)).encode('utf-8')
