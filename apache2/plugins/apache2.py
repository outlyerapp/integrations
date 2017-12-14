#!/usr/bin/env python3

import sys
import requests
from outlyer_plugin import Plugin, Status

class ApachePlugin(Plugin):
    def collect(self, _):

        protocol = self.get('protocol', 'http')
        host = self.get('ip')
        port = self.get('port', '80')
        status_url = self.get('status_url', 'server-status?auto')

        try:
            res = requests.get('%s://%s:%s/%s' % (protocol, host, port, status_url), verify=False)
        except Exception:
            print("Plugin Failed! Check the settings at the top of the plugin. For Apache2 configuration see " \
                  "https://github.com/outlyerapp/packs/blob/master/apache2/README.md")
            return Status.UNKNOWN

        if res.status_code == 404:
            print("Status page URL %s://%s:%s/%s not found" % (protocol, host, port, status_url))
            return Status.UNKNOWN

        for line in res.iter_lines():
            decoded_line = line.decode('utf-8')
            if ': ' in decoded_line:
                key, value = decoded_line.split(': ')
                if key == 'Scoreboard':

                    self.gauge('apache.stats.open', {}).set(value.count('.'))
                    self.gauge('apache.stats.waiting', {}).set(value.count('_'))
                    self.gauge('apache.stats.starting', {}).set(value.count('S'))
                    self.gauge('apache.stats.reading', {}).set(value.count('R'))
                    self.gauge('apache.stats.sending', {}).set(value.count('W'))
                    self.gauge('apache.stats.keepalive', {}).set(value.count('K'))
                    self.gauge('apache.stats.dnslookup', {}).set(value.count('D'))
                    self.gauge('apache.stats.closing', {}).set(value.count('C'))
                    self.gauge('apache.stats.logging', {}).set(value.count('L'))
                    self.gauge('apache.stats.finishing', {}).set(value.count('G'))
                    self.gauge('apache.stats.idle_cleanup', {}).set(value.count('I'))
                    self.gauge('apache.stats.total', {}).set(len(value))
                elif key == 'Load1':
                    self.gauge('apache2.load1', {}).set(float(value))
                elif key == 'Load5':
                    self.gauge('apache2.load5', {}).set(float(value))
                elif key == 'Load15':
                    self.gauge('apache2.load15', {}).set(float(value))
                elif key == 'Total Accesses':
                    self.counter('apache2.total_accesses', {}).set(float(value))
                elif key == 'Total kBytes':
                    self.counter('apache2.total_kbytes', {}).set(float(value))
                elif key == 'Uptime':
                    self.counter('apache2.uptime', {}).set(float(value))
                elif key == 'ReqPerSec':
                    self.counter('apache2.req_per_sec', {}).set(float(value))
                elif key == 'BytesPerSec':
                    self.counter('apache2.bytes_per_sec', {}).set(float(value))
                elif key == 'BytesPerReq':
                    self.counter('apache2.bytes_per_req', {}).set(float(value))
                elif key == 'BusyWorkers':
                    self.gauge('apache2.busy_workers', {}).set(float(value))
                elif key == 'IdleWorkers':
                    self.gauge('apache2.idle_workers', {}).set(float(value))
                elif key == 'ConnsTotal':
                    self.gauge('apache2.conns_total', {}).set(float(value))
                elif key == 'ConnsAsyncWriting':
                    self.gauge('apache2.conns_async_writing', {}).set(float(value))
                elif key == 'ConnsAsyncKeepAlive':
                    self.gauge('apache2.conns_async_keepalive', {}).set(float(value))
                elif key == 'ConnsAsyncClosing':
                    self.gauge('apache2.conns_async_closing', {}).set(float(value))
                elif key == 'CacheSharedMemory':
                    self.gauge('apache2.cache_shared_memory', {}).set(float(value))
                elif key == 'CacheCurrentEntries':
                    self.gauge('apache2.cache_current_entries', {}).set(float(value))
                elif key == 'CacheSubcaches':
                    self.gauge('apache2.cache_subcaches', {}).set(float(value))
                elif key == 'CacheIndexesPerSubcaches':
                    self.gauge('apache2.cache_indexes_per_subcaches', {}).set(float(value))
                elif key == 'CacheIndexUsage':
                    self.gauge('apache2.cache_index_usage', {}).set(float(value.replace('%', '')))
                elif key == 'CacheUsage':
                    self.gauge('apache2.cache_usage', {}).set(float(value.replace('%', '')))
                elif key == 'CacheStoreCount':
                    self.gauge('apache2.cache_store_count', {}).set(float(value))
                elif key == 'CacheReplaceCount':
                    self.gauge('apache2.cache_replace_count', {}).set(float(value))
                elif key == 'CacheExpireCount':
                    self.gauge('apache2.cache_expire_count', {}).set(float(value))
                elif key == 'CacheDiscardCount':
                    self.gauge('apache2.cache_discard_count', {}).set(float(value))
                elif key == 'CacheRetrieveHitCount':
                    self.gauge('apache2.cache_retrieve_hit_count', {}).set(float(value))
                elif key == 'CacheRetrieveMissCount':
                    self.gauge('apache2.cache_retrieve_miss_count', {}).set(float(value))
                elif key == 'CacheRemoveHitCount':
                    self.gauge('apache2.cache_remove_hit_count', {}).set(float(value))
                elif key == 'CacheRemoveMissCount':
                    self.gauge('apache2.cache_remove_miss_count', {}).set(float(value))

        return Status.OK


if __name__ == '__main__':
    # To run the collection
    sys.exit(ApachePlugin().run())