import requests


CHUNK_SIZE = 5


class HttpConnection:
    def __init__(self, domain, backend):
        self._domain = domain
        self._backend = backend

    def get_file(self):
        raise NotImplementedError

    def put_file(self, file_handle, uri):
        r = requests.put(uri,
                         data=self._generator_from_file_handle(file_handle))
        raise NotImplementedError

    # If provided with a generator, the `requests` module takes care of
    # Chunk-Encoded requests.
    def _generator_from_file_handle(self, file_handle):
        while True:
            chunk = file_handle.read(CHUNK_SIZE)
            if not chunk:
                break
            yield chunk
