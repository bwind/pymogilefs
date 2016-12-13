from pymogilefs.request import Request
from pymogilefs.connection import Connection
import re

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

    def do_request(self, config, **kwargs):
        return self._get_connection().do_request(Request(config, **kwargs))

    def get_hosts(self):
        return self.do_request(GetHostsConfig)

    def create_host(self, host, ip, port):
        return self.do_request(CreateHostConfig, host=host, ip=ip, port=port)

    def update_host(self, host, ip, port):
        return self.do_request(UpdateHostConfig, host=host, ip=ip, port=port)

    def delete_host(self, host):
        return self.do_request(DeleteHostConfig, host=host)

    def get_domains(self):
        return self.do_request(GetDomainsConfig)

    def create_domain(self, domain):
        return self.do_request(CreateDomainConfig, domain=domain)

    def delete_domain(self, domain):
        return self.do_request(DeleteDomainConfig, domain=domain)

    def get_classes(self):
        raise NotImplementedError

    def create_class(self, domain, _class, mindevcount):
        kwargs = {'domain': domain,
                  'class': _class,
                  'mindevcount': mindevcount}
        return self.do_request(CreateClassConfig, **kwargs)

    def update_class(self, domain, _class, mindevcount):
        kwargs = {'domain': domain,
                  'class': _class,
                  'mindevcount': mindevcount}
        return self.do_request(UpdateClassConfig, **kwargs)

    def delete_class(self, domain, _class):
        kwargs = {'domain': domain,
                  'class': _class}
        return self.do_request(DeleteClassConfig, **kwargs)

    def get_devices(self):
        return self.do_request(GetDevicesConfig)

    def create_device(self, hostname, devid, hostip, state):
        return self.do_request(CreateDeviceConfig,
                               hostname=hostname,
                               devid=devid,
                               hostip=hostip,
                               state=state)

    def set_state(self, host, device, state):
        return self.do_request(SetStateConfig,
                               host=host,
                               device=device,
                               state=state)

    def set_weight(self, host, device, weight):
        return self.do_request(SetWeightConfig,
                               host=host,
                               device=device,
                               weight=weight)


class RequestConfig:
    @classmethod
    def parse_response_text(cls, response_text):
        if not response_text:
            return {}
        return dict([pair.split('=') for pair in response_text.split('&')])


class GetHostsConfig(RequestConfig):
    COMMAND = 'get_hosts'

    @classmethod
    def parse_response_text(cls, response_text):
        pairs = dict([pair.split('=') for pair in response_text.split('&')])
        if 'hosts' in pairs:
            del pairs['hosts']
        hosts = {}
        for key, value in pairs.items():
            idx, unprefixed_key = key[4:].split('_', 1)
            idx = int(idx)
            if idx not in hosts:
                hosts[idx] = {}
            hosts[idx][unprefixed_key] = value
        return {'hosts': hosts}


class CreateHostConfig(RequestConfig):
    COMMAND = 'create_host'

    @classmethod
    def parse_response_text(cls, response_text):
        pairs = dict([pair.split('=') for pair in response_text.split('&')])
        return {key.split('host', 1)[1]: value for key, value in pairs.items()}


class UpdateHostConfig(RequestConfig):
    COMMAND = 'update_host'

    @classmethod
    def parse_response_text(cls, response_text):
        pairs = dict([pair.split('=') for pair in response_text.split('&')])
        return {key.split('host', 1)[1]: value for key, value in pairs.items()}


class DeleteHostConfig(RequestConfig):
    COMMAND = 'delete_host'


class GetDomainsConfig(RequestConfig):
    COMMAND = 'get_domains'

    @classmethod
    def parse_response_text(cls, response_text):
        pairs = dict([pair.split('=') for pair in response_text.split('&')])
        if 'domains' in pairs:
            del pairs['domains']
        domains = {}
        pattern = r'^domain([0-9]+)class([0-9]+)([a-z]+)$'
        for key, value in pairs.items():
            domain_id, class_id, unprefixed_key = re.match(pattern,
                                                           key).groups()
            domain_id = int(domain_id)
            class_id = int(class_id)
            if domain_id not in domains:
                domains[domain_id] = {'classes': {}}
            if class_id not in domains[domain_id]['classes']:
                domains[domain_id]['classes'][class_id] = {}
            domains[domain_id]['classes'][class_id][unprefixed_key] = value
        return {'domains': domains}


class CreateDomainConfig(RequestConfig):
    COMMAND = 'create_domain'


class DeleteDomainConfig(RequestConfig):
    COMMAND = 'delete_domain'


class CreateClassConfig(RequestConfig):
    COMMAND = 'create_class'


class UpdateClassConfig(RequestConfig):
    COMMAND = 'update_class'


class DeleteClassConfig(RequestConfig):
    COMMAND = 'delete_class'


class GetDevicesConfig(RequestConfig):
    COMMAND = 'get_devices'

    @classmethod
    def parse_response_text(cls, response_text):
        pairs = dict([pair.split('=') for pair in response_text.split('&')])
        if 'devices' in pairs:
            del pairs['devices']
        devices = {}
        for key, value in pairs.items():
            idx, unprefixed_key = key[3:].split('_', 1)
            if idx not in devices:
                devices[idx] = {}
            devices[idx][unprefixed_key] = value
        return {'devices': devices}


class CreateDeviceConfig(RequestConfig):
    COMMAND = 'create_device'


class SetStateConfig(RequestConfig):
    COMMAND = 'set_state'


class SetWeightConfig(RequestConfig):
    COMMAND = 'set_weight'


class CreateOpenConfig(RequestConfig):
    COMMAND = 'create_open'

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


class CreateCloseConfig(RequestConfig):
    COMMAND = 'create_close'

    @classmethod
    def parse_response_text(cls, response_text):
        return {}


class ListKeysConfig(RequestConfig):
    COMMAND = 'list_keys'

    @classmethod
    def parse_response_text(cls, response_text):
        pairs = dict([pair.split('=') for pair in response_text.split('&')])
        key_count = pairs.pop('key_count')
        next_after = pairs.pop('next_after')
        data = {
            'key_count': int(key_count),
            'next_after': next_after,
            'keys': {int(key.split('_')[1]): file_key for key, file_key in
                     pairs.items()},
        }
        return data


class GetPathsConfig(RequestConfig):
    COMMAND = 'get_paths'

    @classmethod
    def parse_response_text(cls, response_text):
        pairs = dict([pair.split('=') for pair in response_text.split('&')])
        data = {
            'path_count': int(pairs['paths']),
            'paths': {int(key.replace('path', '')): path for key, path in
                      pairs.items() if re.match(r'^path[0-9]+$', key)},
        }
        return data
