pymogilefs
==========

[![Build Status](https://travis-ci.org/bwind/pymogilefs.svg?branch=master)](https://travis-ci.org/bwind/pymogilefs) [![codecov](https://codecov.io/gh/bwind/pymogilefs/branch/master/graph/badge.svg)](https://codecov.io/gh/bwind/pymogilefs)

Python client for MogileFS, based on https://github.com/AloneRoad/pymogile.

There are a few Python client projects for MogileFS around (pymogile,
python-mogilefs-client), however these projects seem to be outdated and
abandoned. This client was written from scratch, uses the excellent
[requests](https://github.com/kennethreitz/requests) library to handle all HTTP
requests and is compatible with Python versions 2.7 and 3.3-3.5.

A handfull of management commands haven't been implemented (yet). These include
slave, rebalance, and fsck related commands.

To install pymogilefs, simply:

    $ pip install pymogilefs

Usage:

    >>> from pymogilefs.client import Client
    >>> client = Client(trackers=['0.0.0.0:7001'], domain='testdomain')
    >>> response = client.list_keys(prefix='test', limit=5)
    >>> print(response.data)
    {'key_count': 5,
     'keys': {1: 'testkey',
              2: 'test_file2_0.115351657953_1480606271.65',
              3: 'test_file2_0.380149553659_1480606080.71',
              4: 'test_file_0.0129341319339_1480606080.74',
              5: 'test_file_0.0397767495074_1480606080.8'},
     'next_after': 'testkey'}
    >>> buf = client.get_file('testkey')
    >>> len(buf.read())
    4

Backend usage:

    >>> from pymogilefs.backend import Backend
    >>> backend = Backend(trackers=['0.0.0.0:7001'])
    >>> devices = backend.get_devices()
    >>> print(devices.data['devices']['9'])
    {'devid': '16',
     'hostid': '5',
     'mb_asof': '',
     'mb_free': '45181',
     'mb_total': '59640',
     'mb_used': '14459',
     'observed_state': '',
     'reject_bad_md5': '',
     'status': 'dead',
     'utilization': '',
     'weight': '100'}

Forks and pull requests are highly appreciated.
