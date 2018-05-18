#!/usr/bin/env python3

import sys
import requests
from datetime import datetime

from outlyer_plugin import Plugin, Status


class SolrPlugin(Plugin):
    METRICS_URL = '/metrics?wt=json'
    CORES_URL = '/cores?wt=json&action=STATUS&indexInfo=true'

    def collect(self, _):

        solr_scheme = self.get('solr_scheme', 'http')
        solr_host_ip = self.get('ip', '127.0.0.1')
        solr_port = self.get('port', '8080')
        solr_admin_url = self.get('solr_admin_url', 'solr/admin')
        solr_username = self.get('username', None)
        solr_password = self.get('password', None)

        if solr_username and solr_password:
            solr_url = f"{solr_scheme}://{solr_username}:{solr_password}@{solr_host_ip}:{solr_port}/{solr_admin_url}"
        else:
            solr_url = f"{solr_scheme}://{solr_host_ip}:{solr_port}/{solr_admin_url}"

        metrics = requests.get(solr_url + self.METRICS_URL).json()['metrics']
        cores = requests.get(solr_url + self.CORES_URL).json()

        # Get JVM Metrics
        jvm_metrics = metrics['solr.jvm']
        self.gauge('solr.jvm_classes_loaded').set(jvm_metrics['classes.loaded']['value'])
        self.gauge('solr.jvm_classes_unloaded').set(jvm_metrics['classes.unloaded']['value'])
        self.counter('solr.jvm_gc_concurrentmarksweep_count').set(jvm_metrics['gc.ConcurrentMarkSweep.count']['value'])
        self.counter('solr.jvm_gc_concurrentmarksweep_time').set(jvm_metrics['gc.ConcurrentMarkSweep.time']['value'])
        self.counter('solr.jvm_gc_parnew_count').set(jvm_metrics['gc.ParNew.count']['value'])
        self.counter('solr.jvm_gc_parnew_time').set(jvm_metrics['gc.ParNew.time']['value'])
        self.gauge('solr.jvm_memory_heap_committed').set(jvm_metrics['memory.heap.committed']['value'])
        self.gauge('solr.jvm_memory_heap_init').set(jvm_metrics['memory.heap.init']['value'])
        self.gauge('solr.jvm_memory_heap_max').set(jvm_metrics['memory.heap.max']['value'])
        self.gauge('solr.jvm_memory_heap_used').set(jvm_metrics['memory.heap.used']['value'])
        self.gauge('solr.jvm_memory_nonheap_committed').set(jvm_metrics['memory.non-heap.committed']['value'])
        self.gauge('solr.jvm_memory_nonheap_init').set(jvm_metrics['memory.non-heap.init']['value'])
        self.gauge('solr.jvm_memory_nonheap_max').set(jvm_metrics['memory.non-heap.max']['value'])
        self.gauge('solr.jvm_memory_nonheap_used').set(jvm_metrics['memory.non-heap.used']['value'])
        self.gauge('solr.jvm_threads_blocked_count').set(jvm_metrics['threads.blocked.count']['value'])
        self.gauge('solr.jvm_threads_count').set(jvm_metrics['threads.count']['value'])
        self.gauge('solr.jvm_threads_daemon_count').set(jvm_metrics['threads.daemon.count']['value'])
        self.gauge('solr.jvm_threads_deadlock_count').set(jvm_metrics['threads.deadlock.count']['value'])
        self.gauge('solr.jvm_threads_new_count').set(jvm_metrics['threads.new.count']['value'])
        self.gauge('solr.jvm_threads_runnable_count').set(jvm_metrics['threads.runnable.count']['value'])
        self.gauge('solr.jvm_threads_terminated_count').set(jvm_metrics['threads.terminated.count']['value'])
        self.gauge('solr.jvm_threads_timed_waiting_count').set(jvm_metrics['threads.timed_waiting.count']['value'])
        self.gauge('solr.jvm_threads_waiting_count').set(jvm_metrics['threads.waiting.count']['value'])

        # Get Core Metrics Per Core
        coreCount = 0
        for corename in cores['status']:
            core = cores['status'][corename]
            labels = {"core": corename}
            coreCount += 1
            self.gauge('solr.core_numdocs', labels).set(core['index']['numDocs'])
            self.gauge('solr.core_maxdocs', labels).set(core['index']['maxDoc'])
            self.gauge('solr.core_deleteddocs', labels).set(core['index']['deletedDocs'])
            self.gauge('solr.core_size_in_bytes', labels).set(core['index']['sizeInBytes'])
            self.gauge('solr.core_segmentcount', labels).set(core['index']['segmentCount'])
            self.gauge('solr.core_index_heap_usage_bytes', labels).set(core['index']['indexHeapUsageBytes'])

            core_metrics = metrics['solr.core.' + corename]
            self.counter('solr.core_select_errors', labels).set(core_metrics['QUERY./select.serverErrors']['count'])
            self.counter('solr.core_select_requests', labels).set(core_metrics['QUERY./select.requests']['count'])
            self.counter('solr.core_select_timeouts', labels).set(core_metrics['QUERY./select.timeouts']['count'])
            self.counter('solr.core_update_errors', labels).set(core_metrics['UPDATE./update.errors']['count'])
            self.counter('solr.core_update_requests', labels).set(core_metrics['UPDATE./update.requests']['count'])
            self.counter('solr.core_update_timeouts', labels).set(core_metrics['UPDATE./update.timeouts']['count'])

        # General core status
        self.gauge('solr.core_count').set(coreCount)
        if 'lastCommitComplete' in cores:
            lastCommitCompleteDate = cores['lastCommitComplete']
            lastSoftCommitCompleteDate = cores['lastSoftCommitCompleteDate']
            now = datetime.now()
            lastCommitComplete = datetime.strptime(lastCommitCompleteDate, "%Y-%m-%dT%H:%M:%S.%fZ")
            self.gauge('solr.last_commit_complete_age').set(int((now - lastCommitComplete).total_seconds()))
            lastSoftCommitComplete = datetime.strptime(lastSoftCommitCompleteDate, "%Y-%m-%dT%H:%M:%S.%fZ")
            self.gauge('solr.last_soft_commit_complete_age').set(int((now - lastSoftCommitComplete).total_seconds()))
        else:
            self.gauge('solr.last_commit_complete_age').set(0)
            self.gauge('solr.last_soft_commit_complete_age').set(0)


if __name__ == '__main__':
    sys.exit(SolrPlugin().run())