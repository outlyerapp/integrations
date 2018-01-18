#!/usr/bin/env python3

import socket
import ssl
import sys

from datetime import datetime

from OpenSSL import crypto

from outlyer_plugin import Plugin, Status


class RemoteSslExpirationCheck(Plugin):

    def collect(self, _):

        host = self.get('host')
        port = self.get('port', 443)
        expected_cn = self.get('cn', None)
        warning_days = self.get('warning_days', 30)
        critical_days = self.get('critical_days', 7)

        if not host:
            self.logger.error('Hostname not specified in configuration')
            return Status.UNKNOWN

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
                                        host, x509part[1], expected_cn)

        not_before = datetime.strptime(cert.get_notBefore().decode('utf-8'), "%Y%m%d%H%M%SZ")
        if not_before > datetime.now():
            self.logger.warning('Certificate is not yet valid: %s', not_before)

        not_after = datetime.strptime(cert.get_notAfter().decode('utf-8'), "%Y%m%d%H%M%SZ")
        days_left = (not_after - datetime.utcnow()).days
        self.logger.info('Certificate for %s expires in %d days', host, days_left)

        self.gauge('ssl_days_remaining', {'uom': 'days', 'host': host, 'port': str(port)}).set(days_left)

        if days_left <= critical_days or not_before > datetime.now() or not cn_match:
            return Status.CRITICAL
        elif days_left <= warning_days:
            return Status.WARNING
        else:
            return Status.OK


if __name__ == '__main__':
    sys.exit(RemoteSslExpirationCheck().run())
