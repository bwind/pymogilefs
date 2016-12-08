from pymogilefs.exceptions import MogilefsError


class Response:
    def __init__(self, response_text, config):
        if isinstance(response_text, bytes):
            response_text = response_text.decode()
        status, response_text = response_text.split(' ', 1)
        if status == 'ERR':
            code, message = response_text.split(' ', 1)
            raise MogilefsError(code, message)
        self.config = config
        self.text = response_text.strip()
        self.data = self.config.parse_response_text(self.text)
