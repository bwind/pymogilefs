from pymogilefs.exceptions import RequestError


class MogilefsResponse:
    def __init__(self, buf):
        assert isinstance(buf, str)
        status, response_text = buf.strip().split(' ', 1)
        if status == 'ERR':
            code, message = response_text.split(' ', 1)
            raise RequestError(code, message)
        self.text = response_text
