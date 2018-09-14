import logging

from pymogilefs import backend
from pymogilefs.exceptions import FileNotFoundError, MogilefsError
from pymogilefs.response import Response
import requests
from requests import RequestException

CHUNK_SIZE = 4096

log = logging.getLogger(__name__)

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

    def get_file(self, key, timeout=None, zone='alt'):
        """
        Make sure to consume all the data so the connection could be closed.

        :param key:
        :param timeout:
        :return:
        """
        paths = self.get_paths(key, zone=zone).data
        if not paths['paths']:
            raise FileNotFoundError(self._domain, key)
        for idx in sorted(paths['paths'].keys()):
            try:
                r = requests.get(paths['paths'][idx], stream=True, timeout=timeout)
                r.raise_for_status()
                return r.raw
            except RequestException as e:
                log.warning('Get file from the url in idx "%s" failed. Try another one.', idx, exc_info=e)
                r.close()
        # TODO: raise proper exception
        #raise  # UnknownFileError
            raise Exception('No usable location to get file.')

    def store_file(self, file_handle, key, _class=None, timeout=None):
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
                r = requests.put(path, data=file_handle, timeout=timeout)
                r.raise_for_status()
            except RequestException as e:
                log.warning('Put file to the url in idx "%s" failed. Try another one.', idx, exc_info=e)
                file_handle.seek(0)
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
        #raise  # UnknownFileError
        raise Exception('No usable location to put file.')

    def delete_file(self, key):
        return self._do_request(backend.DeleteFileConfig,
                                domain=self._domain,
                                key=key)

    def rename_file(self):
        raise NotImplementedError

    def get_paths(self, key, noverify=True, zone='alt', pathcount=2):
        # TODO: timeout?
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
        try:
            return self._do_request(backend.ListKeysConfig, **kwargs)
        except Exception as exception:
            if exception.code == 'none_match':
                # Empty result set from this list call should not result
                # in an exception. Return a mocked Mogile response instead.
                response = Response('OK \r\n', backend.ListKeysConfig)
                response.data = {
                    'key_count': 0,
                    'next_after': None,
                    'keys': {},
                }
                return response
            raise exception
