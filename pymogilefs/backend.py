from pymogilefs.connection import Connection

"""
Backend manages a pool of trackers and balances load between them.
"""

# TODO: mark tracker as dead


MAX_RETRIES = 5


class Backend:
    def __init__(self, trackers):
        self._trackers = [tracker.split(':') for tracker in trackers]

    def _get_connection(self):
        # TODO: Try random trackers, implement retries
        host, port = self._trackers[0]
        connection = Connection(host, port)
        connection._connect()
        return connection

    def _do_request(self, request):
        return self._get_connection().do_request(request)

    def get_hosts(self):
        return self._do_request(GetHostsConfig)

    def create_host(self, host, ip, port):
        return self._do_request(CreateHostConfig, host=host, ip=ip, port=port)

    def update_host(self, host, ip, port):
        return self._do_request(UpdateHostConfig, host=host, ip=ip, port=port)

    def delete_host(self, host):
        return self._do_request(DeleteHostConfig, host=host)

    def get_domains(self):
        return self._do_request(GetDomainsConfig)

    def create_domain(self, domain):
        return self._do_request(CreateDomainConfig, domain=domain)

    def delete_domain(self, domain):
        return self._do_request(DeleteDomainConfig, domain=domain)

    def get_classes(self):
        raise NotImplementedError

    def create_class(self, domain, _class, mindevcount):
        kwargs = {'domain': domain,
                  'class': _class,
                  'mindevcount': mindevcount}
        return self._do_request(CreateClassConfig, **kwargs)

    def update_class(self, domain, _class, mindevcount):
        kwargs = {'domain': domain,
                  'class': _class,
                  'mindevcount': mindevcount}
        return self._do_request(UpdateClassConfig, **kwargs)

    def delete_class(self, domain, _class):
        kwargs = {'domain': domain,
                  'class': _class}
        return self._do_request(DeleteClassConfig, **kwargs)

    def get_devices(self):
        return self._do_request(GetDevicesConfig)

    def create_device(self, hostname, devid, hostip, state):
        return self._do_request(CreateDeviceConfig,
                                hostname=hostname,
                                devid=devid,
                                hostip=hostip,
                                state=state)

    def set_state(self, host, device, state):
        return self._do_request(SetStateConfig,
                                host=host,
                                device=device,
                                state=state)

    def set_weight(self, host, device, weight):
        return self._do_request(SetWeightConfig,
                                host=host,
                                device=device,
                                weight=weight)


class GetHostsConfig:
    COMMAND = 'get_hosts'
    PREFIX_RE = r'^host[0-9]+_'


class CreateHostConfig:
    COMMAND = 'create_host'
    PREFIX_RE = r'^host'


class UpdateHostConfig:
    COMMAND = 'update_host'
    PREFIX_RE = r'^host'


class DeleteHostConfig:
    COMMAND = 'delete_host'
    PREFIX_RE = r'^host'


class GetDomainsConfig:
    COMMAND = 'get_domains'
    PREFIX_RE = r'^domain[0-9]+'


class CreateDomainConfig:
    COMMAND = 'create_domain'
    PREFIX_RE = r'^domain[0-9]+'


class DeleteDomainConfig:
    COMMAND = 'delete_domain'
    PREFIX_RE = r'^domain[0-9]+'


class CreateClassConfig:
    COMMAND = 'create_class'
    PREFIX_RE = r'^foo'


class UpdateClassConfig:
    COMMAND = 'update_class'
    PREFIX_RE = r'^foo'


class DeleteClassConfig:
    COMMAND = 'delete_class'
    PREFIX_RE = r'^foo'


class GetDevicesConfig:
    COMMAND = 'get_devices'
    PREFIX_RE = r'^dev[0-9]+_'


class CreateDeviceConfig:
    COMMAND = 'create_device'
    PREFIX_RE = r'^dev[0-9]+_'


class SetStateConfig:
    COMMAND = 'set_state'
    PREFIX_RE = r'^foo'


class SetWeightConfig:
    COMMAND = 'set_weight'
    PREFIX_RE = r'^foo'


class StoreFileConfig:
    COMMAND = 'create_open'
    PREFIX_RE = r'^'

    @classmethod
    def parse_response_text(cls, response_text):
        pairs = dict([pair.split('=') for pair in response_text.split('&')])
        data = {
            'fid': pairs['fid'],
            'dev_count': int(pairs['dev_count']),
            'paths': {int(key.split('_')[1]): path for key, path in
                      pairs.items() if key.startswith('path_')},
            'devids': {int(key.split('_')[1]): int(devid) for key, devid in
                       pairs.items() if key.startswith('devid_')},
        }
        return data
