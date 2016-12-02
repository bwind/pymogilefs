from pymogilefs.exceptions import RequestError
import re


class Response:
    def __init__(self, response_text, config):
        assert isinstance(response_text, str)
        status, response_text = response_text.split(' ', 1)
        if status == 'ERR':
            code, message = response_text.split(' ', 1)
            raise RequestError(code, message)
        self.text = response_text.strip()
        self.config = config
        self.items = self._parse_response_text(self.text,
                                               self.config.PREFIX_RE)

    def _parse_response_text(self, response_text, prefix_re):
        if not response_text:
            return {}
        topics = {}
        pairs = [pair.split('=') for pair in response_text.split('&')]
        for key, value in pairs:
            unprefixed_key = re.sub(prefix_re, '', key)
            prefix = key[:-len(unprefixed_key)].strip('_')
            if prefix not in topics:
                topics[prefix] = {}
            topics[prefix][unprefixed_key] = value
        return list(topics.values())

