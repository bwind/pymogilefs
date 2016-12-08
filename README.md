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
    >>> client = Client(['0.0.0.0:7001'])
    >>> response = client.list_keys(domain='testdomain', prefix='test', after='test', limit=10)
    >>> print(response.data)
    {'key_count': 10,
     'keys': {1: 'testkey',
              2: 'test_file2_0.115351657953_1480606271.65',
              3: 'test_file2_0.380149553659_1480606080.71',
              4: 'test_file_0.0129341319339_1480606080.74',
              5: 'test_file_0.0397767495074_1480606080.8',
              6: 'test_file_0.0865504817808_1480606081.94',
              7: 'test_file_0.1086473832_1480606271.69',
              8: 'test_file_0.215045162336_1480606271.45_9',
              9: 'test_file_0.217320516944_1480606270.9',
              10: 'test_file_0.277959960379_1480606271.23_1'},
     'next_after': 'testkey'}

Forks and pull requests are highly appreciated.
