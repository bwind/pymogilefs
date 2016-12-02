from pymogilefs.backend import Backend
from pymogilefs.request import Request


class Client:
    def __init__(self, trackers):
        self._backend = Backend(trackers)

    def _do_request(self, config, **kwargs):
        return self._backend.do_request(Request(config, **kwargs)).items

    def get_hosts(self):
        return self._do_request(GetHostsConfig)

    def create_host(self, **kwargs):
        return self._do_request(CreateHostConfig, **kwargs)

    def update_host(self, **kwargs):
        return self._do_request(UpdateHostConfig, **kwargs)

    def delete_host(self):
        pass

    def get_domains(self):
        return self._do_request(GetDomainsConfig)

    def create_domain(self):
        pass

    def delete_domain(self):
        pass

    def get_classes(self):
        pass

    def create_class(self):
        pass

    def update_class(self):
        pass

    def delete_class(self):
        pass

    def get_devices(self):
        return self._do_request(GetDevicesConfig)

    def create_device(self):
        pass

    def update_device(self):
        pass

    def set_state(self):
        pass

    def set_weight(self):
        pass

    def clear_cache(self):
        pass


class GetHostsConfig:
    COMMAND = 'get_hosts'
    PREFIX_RE = r'^host[0-9]+_'


class CreateHostConfig:
    COMMAND = 'create_host'
    PREFIX_RE = r'^host'


class UpdateHostConfig:
    COMMAND = 'update_host'
    PREFIX_RE = r'^host'


class GetDomainsConfig:
    COMMAND = 'get_domains'
    PREFIX_RE = r'^domain[0-9]+'


class GetDevicesConfig:
    COMMAND = 'get_devices'
    PREFIX_RE = r'^dev[0-9]+_'

