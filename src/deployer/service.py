from dataclasses import dataclass
from typing import Literal


class ServiceException(Exception):
    """Base exception for Service"""

    pass


class ServiceValueError(ServiceException):
    """Value error for Service param"""

    pass


@dataclass
class ServiceVerifyMessage:
    """Verify message for a single config param"""

    type: Literal["warning", "error"] = "error"
    msg: str = ""

    def __str__(self) -> str:
        return f"{self.type}: {self.msg}"


class Service:
    """The base class of any service in Linux"""

    def __init__(self, name: str):
        self._name = name
        self._config_filename = ""
        self._config = {}

    def _set_name(self, name: str) -> None:
        """Set name of service

        Args:
            name (str): name of service
        """
        self._name = name

    def _get_name(self) -> str:
        """Get name of service

        Returns:
            str: name of service
        """
        return self._name

    def _set_config(self, config: dict) -> None:
        """Set config of service

        Args:
            config (dict): Service specific data
        """

        self._config = config

    def _get_config(self) -> dict:
        """Get config of service

        Returns:
            dict: config
        """

        return self._config

    def _set_config_filename(self, filename: str) -> None:
        """Set config file name of service

        Args:
            filename (str): config file name
        """
        self._config_filename = filename

    def _get_config_filename(self) -> str:
        """Get config file name of service

        Returns:
            str: config file name
        """
        return self._config_filename

    def verify(self) -> list:
        """Verify method for checking config params of service"""
        ...

    """Name of service. Like a `stunnel` or `ssh`"""
    name = property(fget=_get_name, fset=_set_name)

    """Config of service. Like a services, log info & etc"""
    config = property(fget=_get_config, fset=_set_config)

    """Config file name"""
    config_filename = property(fget=_get_config_filename, fset=_set_config_filename)
