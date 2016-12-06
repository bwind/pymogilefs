try:
    from urllib.parse import unquote_plus
except ImportError:
    from urllib import unquote_plus


class MogilefsError(Exception):
    def __init__(self, code, message):
        self.code = code
        self.message = unquote_plus(message)

    def __str__(self):
        return '%s: %s' % (self.code, self.message)


class FileNotFoundError(Exception):
    def __init__(self, domain, key):
        self.domain = domain
        self.key = key

    def __str__(self):
        return 'File "%s" not found in domain "%s"' % (self.key, self.domain)
