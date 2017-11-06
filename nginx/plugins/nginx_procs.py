from outlyer_agent.collection import Status, Plugin, PluginTarget
import psutil


class NginxProcessesPlugin(Plugin):

    def collect(self, target: PluginTarget):

        master_count = 0
        worker_count = 0

        for proc in psutil.process_iter():
            try:
                arg0 = proc.cmdline()[0]
                if 'nginx: master process' in arg0:
                    master_count += 1
                elif 'nginx: worker process' in arg0:
                    worker_count += 1
            except ProcessLookupError:
                pass
            except psutil.AccessDenied:
                pass
            except psutil.ZombieProcess:
                pass
            except IndexError:
                pass

        target.gauge('nginx_master_proc_count').set(master_count)
        target.gauge('nginx_worker_proc_count').set(worker_count)

        if master_count != 1:
            return Status.CRITICAL
        elif worker_count < target.get('min_workers', 1) or worker_count > target.get('max_workers', 5):
            return Status.CRITICAL
        else:
            return Status.OK
