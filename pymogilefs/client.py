from pymogilefs import backend
from pymogilefs.exceptions import FileNotFoundError
from pymogilefs.request import Request
import requests
import io


CHUNK_SIZE = 4096


class Client:
    def __init__(self, backend):
        self._backend = backend

    def _do_request(self, config, **kwargs):
        return self._backend.do_request(config, **kwargs)

    def _create_open(self, **kwargs):
        return self._do_request(backend.CreateOpenConfig, **kwargs)

    def _create_close(self, **kwargs):
        return self._do_request(backend.CreateCloseConfig, **kwargs)

    def get_file(self, domain, key):
        paths = self.get_paths(domain, key).data
        if not paths['paths']:
            raise FileNotFoundError(domain, key)
        for idx in sorted(paths['paths'].keys()):
            try:
                r = requests.get(paths['paths'][idx], stream=True)
                return r.raw
            except:
                pass
        # TODO: raise proper exception
        raise #UnknownFileError

    def store_file(self, file_handle, key, domain, _class=None):
        kwargs = {'domain': domain,
                  'key': key,
                  'fid': 0,
                  'multi_dest': 1}
        if _class is not None:
            kwargs['class'] = _class
        paths = self._create_open(**kwargs).data
        fid = paths['fid']
        for idx in sorted(paths['paths'].keys()):
            path = paths['paths'][idx]
            devid = paths['devids'][idx]
            try:
                r = requests.put(path, data=file_handle)
            except: # TODO: catch specific exceptions
                pass
            else:
                # Call close_open to tell the tracker where we wrote the file
                # to and can start replicating it.
                length = file_handle.tell()
                kwargs = {
                    'fid': fid,
                    'domain': domain,
                    'key': key,
                    'path': path,
                    'devid': devid,
                    'size': length,
                }
                if _class is not None:
                    kwargs['class'] = _class
                response = self._create_close(**kwargs)
                return length
        # TODO: raise proper exception
        raise #FileNotStoredError

    def delete_file(self):
        raise NotImplementedError

    def rename_file(self):
        raise NotImplementedError

    def get_paths(self, domain, key, noverify=True, zone='alt', pathcount=2):
        return self._do_request(backend.GetPathsConfig,
                                domain=domain,
                                key=key,
                                noverify=1 if noverify else 0,
                                zone=zone,
                                pathcount=pathcount)

    def list_keys(self, domain, prefix, after, limit):
        return self._do_request(backend.ListKeysConfig,
                                domain=domain,
                                prefix=prefix,
                                after=after,
                                limit=limit)
