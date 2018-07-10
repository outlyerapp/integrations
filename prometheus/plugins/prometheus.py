#!/usr/bin/env python3

import requests
import sys
import os
from requests.auth import HTTPBasicAuth

HOST = os.environ['ip'] if 'ip' in os.environ else 'localhost'
# Allow plugin to override IP if remote host endpoint
if 'PROMHOST' in os.environ:
  HOST = os.environ['PROMHOST']
PORT = os.environ['PROMPORT']
PATH = os.environ['PROMPATH'] if 'PROMPATH' in os.environ else 'metrics'
auth = False
if 'PROMUSER' in os.environ:
  USER = os.environ['PROMUSER']
  PASS = os.environ['PROMPASS']
  auth = True

try:
  if auth:
    metrics = requests.get(f'http://{HOST}:{PORT}/{PATH}', auth=HTTPBasicAuth(USER, PASS), timeout=20).text
  else:
    metrics = requests.get(f'http://{HOST}:{PORT}/{PATH}', timeout=20).text
  print(metrics)
except:
  print(f"Error connecting to http://{HOST}:{PORT}/{PATH}")
  sys.exit(2)
