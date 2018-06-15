#!/usr/bin/env python3

import sys
import requests
from outlyer_plugin import Plugin, Status

class ApachePlugin(Plugin):
    def collect(self, _):
        protocol = self.get('protocol', 'http')
        host = self.get('ip', '127.0.0.1')
        port = self.get('port', '80')
        status_location = self.get('status_location', '/server-status?auto')

        try:
            res = requests.get('%s://%s:%s%s' % (protocol, host, port, status_location), verify=False, timeout=10)
            res.raise_for_status()

            for line in res.iter_lines():
                decoded_line = line.decode('utf-8')
                if ': ' in decoded_line:
                    key, value = decoded_line.split(': ')
                    if key == 'Scoreboard':
                        self.gauge('apache2.stats.open', {}).set(value.count('.'))
                        self.gauge('apache2.stats.waiting', {}).set(value.count('_'))
                        self.gauge('apache2.stats.starting', {}).set(value.count('S'))
                        self.gauge('apache2.stats.reading', {}).set(value.count('R'))
                        self.gauge('apache2.stats.sending', {}).set(value.count('W'))
                        self.gauge('apache2.stats.keepalive', {}).set(value.count('K'))
                        self.gauge('apache2.stats.dnslookup', {}).set(value.count('D'))
                        self.gauge('apache2.stats.closing', {}).set(value.count('C'))
                        self.gauge('apache2.stats.logging', {}).set(value.count('L'))
                        self.gauge('apache2.stats.finishing', {}).set(value.count('G'))
                        self.gauge('apache2.stats.idle_cleanup', {}).set(value.count('I'))
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
                        self.gauge('apache2.uptime', {}).set(float(value))
                    elif key == 'ReqPerSec':
                        self.gauge('apache2.req_per_sec', {}).set(float(value))
                    elif key == 'BytesPerSec':
                        self.gauge('apache2.bytes_per_sec', {}).set(float(value))
                    elif key == 'BytesPerReq':
                        self.gauge('apache2.bytes_per_req', {}).set(float(value))
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

        except Exception as ex:
            self.logger.error('Unable to scrape metrics from Apache2: %s', str(ex))
            return Status.CRITICAL


if __name__ == '__main__':
    # To run the collection
    sys.exit(ApachePlugin().run())
