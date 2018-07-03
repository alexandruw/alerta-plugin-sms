
import json
import logging
import os
import requests

try:
    from alerta.plugins import app  # alerta >= 5.0
except ImportError:
    from alerta.app import app  # alerta < 5.0

from alerta.plugins import PluginBase

LOG = logging.getLogger('alerta.plugins.sms')

SMS_URL = os.environ.get(
    'SMS_URL') or app.config['SMS_URL']

SMS_SEND_ON_ACK = os.environ.get(
    'SMS_SEND_ON_ACK') or app.config.get('SMS_SEND_ON_ACK', False)

SMS_SEVERITY_MAP = app.config.get('sms_SEVERITY_MAP', {})

SMS_DEFAULT_SEVERITY_MAP = {'security': '#000000', # black
                              'critical': '#FF0000', # red
                              'major': '#FFA500', # orange
                              'minor': '#FFFF00', # yellow
                              'warning': '#1E90FF', #blue
                              'informational': '#808080', #gray
                              'debug': '#808080', # gray
                              'trace': '#808080', # gray
                              'ok': '#00CC00'} # green

class ServiceIntegration(PluginBase):

    def __init__(self, name=None):
        # override user-defined severities
        self._severities = SMS_DEFAULT_SEVERITY_MAP
        self._severities.update(SMS_SEVERITY_MAP)

        super(ServiceIntegration, self).__init__(name)

    def pre_receive(self, alert):
        return alert

    def _sms_prepare_payload(self, alert, status=None, text=None):
        summary = "*[%s] %s %s - _%s on %s_* " % (
            (status if status else alert.status).capitalize(), alert.environment, alert.severity.capitalize(
            ), alert.event, alert.resource)
        )

        payload = {
            "text": summary
        }

        return payload

    def post_receive(self, alert):

#        if alert.repeat:
#            return

        payload = self._sms_prepare_payload(alert)

        LOG.info('sms payload: %s', payload)

        try:
            r = requests.post(SMS_URL,data=json.dumps(payload), timeout=2)
        except Exception as e:
            raise RuntimeError("sms connection error: %s", e)

        LOG.info('sms response: %s', r.status_code)

    def status_change(self, alert, status, text):
        if SMS_SEND_ON_ACK == False or status not in ['ack', 'assign']:
            return

        payload = self._sms_prepare_payload(alert, status, text)

        LOG.info('sms payload: %s', payload)
        try:
            r = requests.post(SMS_URL,
                              data=json.dumps(payload), timeout=2)
        except Exception as e:
            raise RuntimeError("sms connection error: %s", e)

        LOG.info('sms response: %s', r.status_code)

