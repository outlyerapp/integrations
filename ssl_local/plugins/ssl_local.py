import os.path
from datetime import datetime

from OpenSSL import crypto

from outlyer_agent.collection import Status, Plugin, PluginTarget


class LocalSslExpirationCheck(Plugin):

    def collect(self, target: PluginTarget):

        cert_path = target.get('cert_path')
        warning_days = target.get('warning_days', 30)
        critical_days = target.get('critical_days', 7)

        if not cert_path:
            self.logger.error('Path to certificate file not specified in configuration')
            return Status.UNKNOWN

        if not os.path.exists(cert_path):
            self.logger.error("Certificate file not found: %s", cert_path)
            return Status.UNKNOWN

        cert_data = open(cert_path, 'rb').read()
        cert = crypto.load_certificate(crypto.FILETYPE_PEM, cert_data)

        not_before = datetime.strptime(cert.get_notBefore().decode('utf-8'), "%Y%m%d%H%M%SZ")
        if not_before > datetime.now():
            self.logger.warning('Certificate is not yet valid: %s', not_before)

        not_after = datetime.strptime(cert.get_notAfter().decode('utf-8'), "%Y%m%d%H%M%SZ")
        days_left = (not_after - datetime.utcnow()).days
        self.logger.info('Certificate %s expires in %d days', cert_path, days_left)

        target.gauge('ssl_days_remaining', {'uom': 'days', 'certificate_file': cert_path}).set(days_left)

        if days_left > warning_days:
            return Status.OK
        elif days_left > critical_days:
            return Status.WARNING
        else:
            return Status.CRITICAL
