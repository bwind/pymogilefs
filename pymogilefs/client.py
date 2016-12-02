from pymogilefs.backend import Backend
from pymogilefs.request import Request


class Client:
    def __init__(self, trackers):
        self._backend = Backend(trackers)

    def get_hosts(self):
        response = self._backend.do_request(Request(Hosts))
        return response.items

    def create_host(self):
        pass

    def update_host(self):
        pass

    def delete_host(self):
        pass

    def get_domains(self):
        response = self._backend.do_request(Request(Domains))
        return response.items

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
        response = self._backend.do_request(Request(Devices))
        return response.items

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


class Hosts:
    COMMAND = 'get_hosts'
    PREFIX_RE = r'host[0-9]+_'


class Domains:
    COMMAND = 'get_domains'
    PREFIX_RE = r'domain[0-9]+'


class Devices:
    COMMAND = 'get_devices'
    PREFIX_RE = r'dev[0-9]+_'

