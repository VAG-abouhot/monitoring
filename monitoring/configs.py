import abc
import os

from typing import Dict, Optional

from monitoring.exceptions import MonitoringException
from monitoring.http.hosts import Host, HostsCollection, CallType
from monitoring.user_agent import UserAgent


class Config(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, app_id=None, api_key=None):
        # type: (Optional[str], Optional[str]) -> None

        app_id = os.environ['VALIDANDGO_APP_ID'] if app_id is None else app_id
        api_key = os.environ['VALIDANDGO_API_KEY'] if api_key is None else api_key

        self.app_id = str(app_id)

        assert app_id, 'app_id cannot be empty.'

        self.api_key = str(api_key)

        # In seconds
        self.read_timeout = 5
        self.write_timeout = 30
        self.connect_timeout = 2

        # In microseconds
        self.wait_task_time_before_retry = 100000

        self.hosts = self.build_hosts()

        self.headers = {
            'X-Validandgo-Application-Id': app_id,
            'X-Validandgo-API-Key': api_key,
            'User-Agent': UserAgent.get(),
            'Content-Type': 'application/json',
        }

    @abc.abstractmethod
    def build_hosts(self):
        # type: () -> HostsCollection

        pass  # pragma: no cover


class MonitoringConfig(Config):

    def __init__(self, app_id=None, api_key=None):
        # type: (Optional[str], Optional[str]) -> None

        super(MonitoringConfig, self).__init__(app_id, api_key)
        
        self.batch_size = 1000

    def build_hosts(self):
        # type: () -> HostsCollection

        return HostsCollection([
            Host('{}-dsn.validandgo.net'.format(self.app_id), 10, CallType.READ),
            Host('{}.validandgo.net'.format(self.app_id), 10, CallType.WRITE),
            Host('{}-1.validandgonet.com'.format(self.app_id)),
            Host('{}-2.validandgonet.com'.format(self.app_id)),
            Host('{}-3.validandgonet.com'.format(self.app_id))
        ])