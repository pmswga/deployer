Overview
========

The main idea of ​​the library is to provide the ability to work with services from Python.

A service is an entity that has:

- name
- data
- configuration file name

Configuration actions:

- create/edit/delete
- check configuration values
- save configuration file

Simple example
--------------

.. code-block:: python

    from deployer import Stunnel

    stunnel = Stunnel()

    stunnel.addService(
        name="gmail-pop3",
        client="yes",
        accept="127.0.0.1:110",
        connect="pop.gmail.com:995",
        verifyChain="yes",
        CApath="/etc/ssl/certs",
        checkHost="pop.gmail.com",
        OCSPaia="yes",
    )

    with open(stunnel.config_filename, "w") as fp:
        print(str(stunnel), file=fp)
