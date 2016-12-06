from pymogilefs import backend
from pymogilefs.request import Request


class Client:
    def __init__(self, backend):
        self._backend = backend

    def _do_request(self, config, **kwargs):
        return self._backend.do_request(Request(config, **kwargs))

    def store_file(self, file_handle, key, domain, _class=None):
        kwargs = {'domain': domain,
                  'key': key,
                  'fid': 0,
                  'multi_dest': 1}
        if _class is not None:
            kwargs['class'] = _class
        response = self._do_request(backend.StoreFileConfig, **kwargs).items
        http_connection = HttpConnection(domain=self._domain,
                                         backend=self._backend)
        http_connection.put_file(file_handle=file_handle,
                                 uri=uri)

    def delete_file(self):
        raise NotImplementedError

    def rename_file(self):
        raise NotImplementedError

    def get_paths(self):
        raise NotImplementedError

    def list_keys(self, domain, prefix, after, limit):
        return self._do_request(backend.ListKeysConfig,
                                domain=domain,
                                prefix=prefix,
                                after=after,
                                limit=limit)
