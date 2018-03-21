#!/usr/bin/env python3

"""
Scrapes the Kubernetes API /healthz and /metrics endpoints using the Kubernetes
client to enable Authentication with the server
"""

import sys
import os

from kubernetes import client, config

# Get endpoint, defaults to healthz
endpoint = '/' + os.environ['endpoint'] if 'endpoint' in os.environ else '/healthz'

config.load_incluster_config()
v1 = client.CoreV1Api()
# Authentication setting
auth_settings = ['BearerToken']

if 'healthz' in endpoint:
    try:
        res = v1.api_client.call_api(endpoint, 'GET',
                                     auth_settings=auth_settings,
                                     _request_timeout=20,
                                     response_type=str)
        if res[1] == 200:
            sys.exit(0)
        else:
            sys.exit(2)
    except Exception as err:
        sys.exit(2)
else:
    try:
        # Scrape a Promtheus endpoint
        res = v1.api_client.call_api(endpoint, 'GET',
                                     auth_settings=auth_settings,
                                     _request_timeout=20,
                                     _return_http_data_only=True,
                                     response_type=str)

        print(res)
        sys.exit(0)
    except Exception:
        sys.exit(2)