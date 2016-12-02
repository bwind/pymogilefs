import urllib


class Request:
    def __init__(self, config, **kwargs):
        self.config = config
        self._kwargs = kwargs or {}

    def __bytes__(self):
        try:
            kwargs = urllib.parse.urlencode(self._kwargs)
        except:
            print(self._kwargs)
        return ('%s %s\r\n' % (self.config.COMMAND, kwargs)).encode('utf-8')
