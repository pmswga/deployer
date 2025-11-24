import os

from dataclasses import dataclass
from typing import Literal

from .service import Service, ServiceException, ServiceValueError, ServiceVerifyMessage


# Sub types
class StunnelValueRange:
    FACILITY = (
        "emerg",
        "alert",
        "crit",
        "err",
        "warning",
        "notice",
        "info",
        "debug",
    )
    YES_NO = ("yes", "no")
    YES_QUITE_NO = ("yes", "quite", "no")
    APPEND_OVERWRITE = ("append", "overwrite")
    COMPRESSION = ("deflate", "zlib")


@dataclass
class StunnelService:
    """Stunnel service config representation

    Returns:
        _type_: _description_
    """

    name: str = ""
    client: Literal["yes", "no"] = "yes"
    accept: str = ""
    connect: str = ""
    verifyChain: Literal["yes", "no"] = "yes"
    CApath: str = ""
    checkHost: str = ""
    OCSPaia: Literal["yes", "no"] = "yes"
    engineId: str = ""
    key: str = ""
    cert: str = ""

    def __str__(self) -> str:
        string = []
        string.append(f"[{self.name}]")

        for arg in self.__match_args__:
            if arg in ("name"):
                continue

            if getattr(self, arg):
                string.append(f"{arg} = {getattr(self, arg)}")

        return "\n".join(string)


class Stunnel(Service):
    """Stunnel service class representation

    Additional links:
        https://www.stunnel.org/config_unix.html

    Args:
        Service (_type_): _description_
    """

    def __init__(self, *, name: str = "stunnel", **kwargs):
        super().__init__(name)

        # Global options
        self._config.setdefault("chroot")
        self._config.setdefault("compression", "deflate")
        self._config.setdefault("debug", "notice")
        self._config.setdefault("egid")
        self._config.setdefault("engine")
        self._config.setdefault("engineCtrl")
        self._config.setdefault("engineDefault")
        self._config.setdefault("fips", "no")
        self._config.setdefault("foreground", "yes")
        self._config.setdefault("iconActive")
        self._config.setdefault("iconError")
        self._config.setdefault("iconIdle")
        self._config.setdefault("log", "append")
        self._config.setdefault("output")
        self._config.setdefault("pid")
        self._config.setdefault("provider")
        self._config.setdefault("providerParameter")
        self._config.setdefault("RNDbytes")
        self._config.setdefault("RNDfile")
        self._config.setdefault("RNDoverwrite", "yes")
        self._config.setdefault("service", "stunnel")
        self._config.setdefault("setEnv", [])
        self._config.setdefault("syslog", "yes")
        self._config.setdefault("taskbar", "yes")

        # Services
        self._config.setdefault("services", {})

        # Set config values
        for k, v in kwargs.items():
            if k in self._config.keys():
                self._config[k] = v

    def verify(self) -> list[ServiceVerifyMessage]:
        messages = []

        if self._config["chroot"] and not os.path.exists(self._config["chroot"]):
            messages.append(
                ServiceVerifyMessage(
                    "warning", f"'{self._config["chroot"]}' is not exists"
                )
            )

        if (
            self._config["compression"]
            and self._config["compression"] not in StunnelValueRange.COMPRESSION
        ):
            messages.append(
                ServiceVerifyMessage(
                    "error", "compression must be contain deflate or zlib"
                )
            )

        if (
            self._config["debug"]
            and self._config["debug"] not in StunnelValueRange.FACILITY
        ):
            messages.append(
                ServiceVerifyMessage("error", "debug must be contain facility level")
            )

        if (
            self._config["fips"]
            and self._config["fips"] not in StunnelValueRange.YES_NO
        ):
            messages.append(ServiceVerifyMessage("error", "fips must be 'yes' or 'no'"))

        if (
            self._config["foreground "]
            and self._config["foreground "] not in StunnelValueRange.YES_QUITE_NO
        ):
            messages.append(
                ServiceVerifyMessage(
                    "error", f"foreground must be 'yes', 'quite' or 'no'"
                )
            )

        if (
            self._config["log"]
            and self._config["log"] not in StunnelValueRange.APPEND_OVERWRITE
        ):
            messages.append(
                ServiceVerifyMessage("error", "log must be 'append' or 'overwrite'")
            )

        if self._config["pid"] and not os.path.exists(self._config["pid"]):
            messages.append(
                ServiceVerifyMessage(
                    "warning", f"'{self._config["pid"]}' is not exists"
                )
            )

        if (
            self._config["RNDoverwrite"]
            and self._config["RNDoverwrite"] not in StunnelValueRange.YES_NO
        ):
            messages.append(
                ServiceVerifyMessage("error", "RNDoverwrite must be 'yes' or 'no'")
            )

        if self._config["service"] and self._config["service"] == "":
            messages.append(
                ServiceVerifyMessage("error", "service name mustn't be empty")
            )

        if (
            self._config["syslog"]
            and self._config["syslog"] not in StunnelValueRange.YES_NO
        ):
            messages.append(
                ServiceVerifyMessage("error", "syslog must be 'yes' or 'no'")
            )

        if (
            self._config["taskbar "]
            and self._config["taskbar "] not in StunnelValueRange.YES_NO
        ):
            messages.append(
                ServiceVerifyMessage("error", "taskbar  must be 'yes' or 'no'")
            )

        return messages

    def addService(self, **kwargs) -> None:
        service = StunnelService()

        if "name" not in kwargs.keys() or kwargs.get("name") == "":
            raise ServiceValueError("Need name for stunnel service")

        for k, v in kwargs.items():
            if k in StunnelService.__match_args__:
                setattr(service, k, v)

        if service.name not in self._config["services"].keys():
            self._config["services"][service.name] = service
        else:
            raise ServiceException(f"Service '{service.name}' is duplicated")

    def getService(self, name: str) -> StunnelService | None:
        return self._config["services"].get(name)

    def removeService(self, name: str) -> None:
        self._config["service"].pop(name)

    def services(self) -> list:
        return self._config["services"]

    def __str__(self) -> str:
        string = []

        # Render global params
        for k, v in self._config.items():
            # Skip service fields
            if k in ("services"):
                continue

            if v:
                string.append(f"{k} = {v}")

        string.append("")
        # Render services
        for _, service in self._config["services"].items():
            string.append(str(service))
            string.append("")

        return "\n".join(string)
