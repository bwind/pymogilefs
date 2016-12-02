from pymogilefs.backend import Backend
from pymogilefs.request import Request


class Client:
    def __init__(self, trackers):
        self._backend = Backend(trackers)

    def get_hosts(self):
        response = self._backend.do_request(Request('get_hosts'))
        pairs = [pair.split('=') for pair in response.text.split('&')]
        hosts = {}
        for key, value in pairs:
            index = key[4:5]
            if index not in hosts:
                hosts[index] = {}
            hosts[index][key[6:]] = value
        return list(hosts.values())

    def create_host(self):
        pass

    def update_host(self):
        pass

    def delete_host(self):
        pass

    def get_domains(self):
        pass

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
        pass

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
