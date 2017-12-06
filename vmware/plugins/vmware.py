import json

from datetime import datetime, timedelta

from typing import List, Dict

from pyVim import connect
from pyVmomi import vim
from pyVmomi.VmomiSupport import ManagedObject

from outlyer_agent.collection import Status, Plugin, PluginTarget
from outlyer_agent.java import canonicalize_name

# TODO: metrics for individual VMs

ADJUSTMENTS = {
    'cpu.usage.average': lambda x: x / 100.0
}


# noinspection PyMethodMayBeStatic
class VmwarePlugin(Plugin):

    def get_objects_by_type(self, content: vim.ServiceInstanceContent,
                            object_type: str, recursive: bool = True) -> List[ManagedObject]:
        container_view = content.viewManager.CreateContainerView(content.rootFolder,
                                                                 [object_type],
                                                                 recursive)
        return container_view.view

    def get_perf_counter_list(self, content: vim.ServiceInstanceContent) -> Dict[str, str]:
        counters = {}
        # menu = []
        for counter in content.perfManager.perfCounter:
            key = f'{counter.groupInfo.key}.{counter.nameInfo.key}.{counter.rollupType}'
            counters[key] = counter.key
            # menu.append({
            #     'key': key,
            #     'desc': counter.nameInfo.summary,
            #     'uom': counter.unitInfo.key
            # })
        # with open('temp/vmware_counters.json', 'w', encoding="utf8") as f:
        #     json.dump(menu, f)
        return counters

    def get_metric_ids_for_object(self, perf_counters: Dict[str, str],
                                  instance: str,
                                  *counters: str) -> List[vim.PerformanceManager.MetricId]:
        metric_ids = []
        for counter in counters:
            counter_num = perf_counters[counter]
            counter_id = vim.PerformanceManager.MetricId(counterId=counter_num, instance=instance)
            metric_ids.append(counter_id)
        return metric_ids

    def get_metrics_for_object(self,
                               target: PluginTarget,
                               content: vim.ServiceInstanceContent,
                               perf_counters: Dict[str, str],
                               host: ManagedObject,
                               instance: str,
                               *counters: str) -> None:
        metric_ids = self.get_metric_ids_for_object(perf_counters, instance, *counters)
        end_time = datetime.now()
        start_time = end_time - timedelta(minutes=1)
        query = vim.PerformanceManager.QuerySpec(entity=host, metricId=metric_ids, intervalId=20,
                                                 startTime=start_time, endTime=end_time)
        stats = content.perfManager.QueryPerf(querySpec=[query])

        labels = {}
        if isinstance(host, vim.HostSystem):
            labels['host_name'] = host.name
        elif isinstance(host, vim.VirtualMachine):
            labels['vm_name'] = host.name

        if len(stats) == 0:
            return

        self.logger.info('metric count for %s = %d', host.name, len(stats[0].value))

        for result in stats[0].value:
            name = [k for k, v in perf_counters.items() if v == result.id.counterId][0]
            name = 'vmware.' + canonicalize_name(name)

            instance = canonicalize_name(result.id.instance)
            labels['instance'] = instance

            val = float(sum(result.value)) / len(result.value)

            if name.endswith('_summation'):
                target.counter(name, labels).set(val)
            else:
                target.gauge(name, labels).set(val)


    def collect(self, target: PluginTarget) -> Status:

        proto = target.get('protocol', 'https')
        port = target.get('port', 443)
        hostname = target.get('host')
        username = target.get('username')
        password = target.get('password')
        if not hostname or not username or not password:
            self.logger.error('Incomplete configuration for F5 LTM plugin')
            return Status.UNKNOWN

        srv = connect.SmartConnectNoSSL(protocol=proto, host=hostname, port=port,
                                        user=username, pwd=password)  # type: vim.ServiceInstance

        content = srv.RetrieveContent()  # type: vim.ServiceInstanceContent

        perf_counters = self.get_perf_counter_list(content)
        hosts = self.get_objects_by_type(content, vim.HostSystem)
        vms = self.get_objects_by_type(content, vim.VirtualMachine)
        objects = hosts + vms

        for obj in objects:
            self.get_metrics_for_object(target, content, perf_counters, obj, '*',
                                        'cpu.system.summation',
                                        'cpu.wait.summation',
                                        'cpu.ready.summation',
                                        'cpu.used.summation',
                                        'cpu.idle.summation',
                                        'cpu.swapwait.summation',
                                        'cpu.usagemhz.average',
                                        'cpu.usage.average',
                                        'cpu.utilization.average',
                                        'cpu.coreUtilization.average',
                                        'cpu.latency.average',
                                        'disk.usage.average',
                                        'disk.numberRead.summation',
                                        'disk.numberWrite.summation',
                                        'disk.read.average',
                                        'disk.write.average',
                                        'disk.maxQueueDepth.average',
                                        'mem.active.average',
                                        'mem.shared.average',
                                        'mem.vmmemctl.average',
                                        'mem.swapped.average',
                                        'mem.swapinRate.average',
                                        'mem.swapoutRate.average',
                                        'mem.usage.average',
                                        'mem.granted.average',
                                        'mem.swapused.average',
                                        'net.usage.average',
                                        'net.bytesRx.average',
                                        'net.bytesTx.average',
                                        'net.transmitted.average',
                                        'net.received.average',
                                        'virtualDisk.read.average',
                                        'virtualDisk.write.average',
                                        'virtualDisk.totalReadLatency.average',
                                        'virtualDisk.totalWriteLatency.average',
                                        'datastore.read.average',
                                        'datastore.write.average',
                                        'datastore.totalReadLatency.average',
                                        'datastore.totalWriteLatency.average',
                                        'datastore.datastoreMaxQueueDepth.latest')

        connect.Disconnect(srv)

        return Status.OK
