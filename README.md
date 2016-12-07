pymogilefs
==========

Python client for MogileFS, based on https://github.com/AloneRoad/pymogile.

There are a few Python client projects for MogileFS around (pymogile,
python-mogilefs-client), however these projects seem to be outdated and
abandoned. This client was written from scratch, uses the excellent `requests`
library to handle all HTTP requests and is compatible with Python versions 2.7,
3.4, and 3.5.

A handfull of management commands haven't been implemented (yet). These include
slave, rebalance, and fsck related commands.

To install pymogilefs, simply:

    $ pip install pymogilefs

Forks and pull requests are highly appreciated.
