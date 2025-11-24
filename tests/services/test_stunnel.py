from deployer import Stunnel


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


def test_create_stunnel():
    service = Stunnel()

    assert service.name == "stunnel"


def test_add_service():
    service = Stunnel()

    service.addService(
        name="gmail-pop3",
        client="yes",
        accept="127.0.0.1:110",
        connect="pop.gmail.com:995",
        verifyChain="yes",
        CApath="/etc/ssl/certs",
        checkHost="pop.gmail.com",
        OCSPaia="yes",
    )

    assert service.getService("gmail-pop3") is not None
