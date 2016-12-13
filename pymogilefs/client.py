from pymogilefs import backend
from pymogilefs.exceptions import FileNotFoundError
import requests


CHUNK_SIZE = 4096


class Client:
    def __init__(self, trackers, domain):
        self._backend = backend.Backend(trackers)
        self._domain = domain

    def _do_request(self, config, **kwargs):
        return self._backend.do_request(config, **kwargs)

    def _create_open(self, **kwargs):
        return self._do_request(backend.CreateOpenConfig, **kwargs)

    def _create_close(self, **kwargs):
        return self._do_request(backend.CreateCloseConfig, **kwargs)

    def get_file(self, key):
        paths = self.get_paths(key).data
        if not paths['paths']:
            raise FileNotFoundError(self._domain, key)
        for idx in sorted(paths['paths'].keys()):
            try:
                r = requests.get(paths['paths'][idx], stream=True)
                return r.raw
            except:
                pass
        # TODO: raise proper exception
        raise  # UnknownFileError

    def store_file(self, file_handle, key, _class=None):
        kwargs = {'domain': self._domain,
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
                requests.put(path, data=file_handle)
            except:  # TODO: catch specific exceptions
                pass
            else:
                # Call create_close to tell the tracker where we wrote the
                # file to and can start replicating it.
                length = file_handle.tell()
                kwargs = {
                    'fid': fid,
                    'domain': self._domain,
                    'key': key,
                    'path': path,
                    'devid': devid,
                    'size': length,
                }
                if _class is not None:
                    kwargs['class'] = _class
                self._create_close(**kwargs)
                return {'path': path, 'length': length}
        # TODO: raise proper exception
        raise  # FileNotStoredError

    def delete_file(self):
        raise NotImplementedError

    def rename_file(self):
        raise NotImplementedError

    def get_paths(self, key, noverify=True, zone='alt', pathcount=2):
        return self._do_request(backend.GetPathsConfig,
                                domain=self._domain,
                                key=key,
                                noverify=1 if noverify else 0,
                                zone=zone,
                                pathcount=pathcount)

    def list_keys(self, prefix=None, after=None, limit=None):
        kwargs = {'domain': self._domain}
        if prefix is not None:
            kwargs['prefix'] = prefix
        if after is not None:
            kwargs['after'] = after
        if limit is not None:
            kwargs['limit'] = limit
        return self._do_request(backend.ListKeysConfig, **kwargs)
