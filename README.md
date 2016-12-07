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

Forks and pull requests are highly appreciated.
