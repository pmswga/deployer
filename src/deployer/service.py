from dataclasses import dataclass
from typing import Literal


# Common exceptions
class ServiceException(Exception):
    pass


class ServiceValueError(ServiceException):
    pass


# Service verify Message
@dataclass
class ServiceVerifyMessage:
    type: Literal["warning", "error"] = "error"
    msg: str = ""

    def __str__(self) -> str:
        return f"{self.type}: {self.msg}"


# Base class of any Service


class Service:
    """The base class of any service in Unix"""

    def __init__(self, name: str):
        self._name = name
        self._config_filename = ""
        self._config = {}

    def _set_name(self, name: str) -> None:
        self._name = name

    def _get_name(self) -> str:
        return self._name

    def _set_config(self, config: dict) -> None:
        self._config = config

    def _get_config(self) -> dict:
        return self._config

    def _set_config_filename(self, filename: str) -> None:
        self.config_filename = filename

    def _get_config_filename(self) -> str:
        return self.config_filename

    def verify(self) -> list: ...

    name = property(fget=_get_name, fset=_set_name)
    config = property(fget=_get_config, fset=_set_config)
    config_filename = property(fget=_get_config_filename, fset=_set_config_filename)
