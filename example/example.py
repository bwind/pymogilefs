# -*- coding: utf-8 -*-
import logging

import requests

from pymogilefs.client import Client
from pymogilefs.exceptions import MogilefsError


logger = logging.getLogger('pymogilefs')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setFormatter(
    logging.Formatter('[%(asctime)s] p%(process)s {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s',
                      '%m-%d %H:%M:%S'))
logger.addHandler(handler)


key = 'qoo'
timeout = 15

file = open("/tmp/qqq", "w")
file.write("qqqqq")
file.close()

file = open("/tmp/qqq", "rb")

# init
client = Client(trackers=['10.144.129.233:7001'], domain='dom1')

# upload file
response = client.store_file(file, key, timeout=timeout)
print(response)

# download file by path
response = client.get_paths(key, zone='default')
print(response.data)

response = requests.get(response.data.get('paths').get(1))
print(response.text)

# download file by get file
fh = client.get_file(key, timeout=timeout, zone='default')
print(response.text)

# delete file
client.delete_file(key)

try:
    client.get_paths(key)
except MogilefsError:
    pass



