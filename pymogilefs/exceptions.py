import urllib


class NoTrackersAvailableError(Exception):
    pass


class RequestError(Exception):
    def __init__(self, code, message):
        self.code = code
        self.message = urllib.parse.unquote_plus(message)

    def __str__(self):
        return '%s: %s' % (self.code, self.message)
