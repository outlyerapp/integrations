#!/usr/bin/env python3

import os.path
import sys
import socket
import ssl
from datetime import datetime
from OpenSSL import crypto
from outlyer_plugin import Plugin, Status


class SslCheck(Plugin):

    def collect(self, _):
        # Local SSL
        cert_path = self.get('cert_path')
        
        # Remote SSL
        host = self.get('host')
        port = self.get('port', 443)

        expected_cn = self.get('cert_common_name', None)
        warning_days = int(self.get('warning_days', 30))
        critical_days = int(self.get('critical_days', 7))

        if not cert_path and not host or cert_path and host:
            self.logger.error('Must either specify host or cert_path environment variables')
            return Status.UNKNOWN

        if cert_path and not host:
            if not os.path.exists(cert_path):
                self.logger.error("Certificate file not found: %s", cert_path)
                return Status.UNKNOWN

            cert_data = open(cert_path, 'rb').read()
            cert = crypto.load_certificate(crypto.FILETYPE_PEM, cert_data)
        elif host and not cert_path:
            try:
                cert_data = ssl.get_server_certificate((host, port))
            except socket.gaierror as ex:
                self.logger.error('Error retrieving certifcate for %s: %s', host, str(ex))
                return Status.CRITICAL
            cert = crypto.load_certificate(crypto.FILETYPE_PEM, cert_data)

        cn_match = True
        if expected_cn:
            for x509part in cert.get_subject().get_components():
                if x509part[0] == b'CN' and x509part[1].decode('utf-8') != expected_cn:
                    cn_match = False
                    self.logger.warning('CN for certificate at %s is %s, was expecting %s',
                                        host, x509part[1].decode('utf-8'), expected_cn)

        not_before = datetime.strptime(cert.get_notBefore().decode('utf-8'), "%Y%m%d%H%M%SZ")
        if not_before > datetime.now():
            self.logger.warning('Certificate is not yet valid: %s', not_before)

        not_after = datetime.strptime(cert.get_notAfter().decode('utf-8'), "%Y%m%d%H%M%SZ")
        days_left = (not_after - datetime.utcnow()).days
        self.logger.info('Certificate for %s expires in %d days', host, days_left)

        if cert_path:
            self.gauge('ssl.days_remaining', {'ssl_cert_source': cert_path}).set(days_left)
        else:
            self.gauge('ssl.days_remaining', {'ssl_cert_source': host}).set(days_left)

        if days_left <= critical_days or not_before > datetime.now() or not cn_match:
            return Status.CRITICAL
        elif days_left <= warning_days:
            return Status.WARNING
        else:
            return Status.OK


if __name__ == '__main__':
    sys.exit(SslCheck().run())
