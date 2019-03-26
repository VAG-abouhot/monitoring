from typing import Optional


class MonitoringException(Exception):
    pass


class MissingObjectIdException(MonitoringException):
    def __init__(self, message, obj):
        # type: (str, dict) -> None

        super(MonitoringException, self).__init__(message)
        self.obj = obj


class RequestException(MonitoringException):
    def __init__(self, message, status_code):
        # type: (str, Optional[int]) -> None

        super(MonitoringException, self).__init__(message)
        self.status_code = status_code


class MonitoringUnreachableHostException(Exception):
    pass