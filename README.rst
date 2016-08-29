JuJu snmpd Charm
----------------

This charm is used to install/configure the SNMPD daemon.

Usage
~~~~~

Step by step instructions on using the charm:

.. code::

   juju deploy snmpd


Configuration may be updated using the JuJu charm configuration variables. This
will automatically update the snmpd.conf and restart snmpd as required.

Configuration
~~~~~~~~~~~~~

There are a couple of configuration knobs:

  - sysLocation: Updates the sysLocation configuration variable
  - sysContact: Updates the sysContact configuration variable
  - acls: Multi-line string that contains ACL information such as community
    strings
  - other: Multi-line string that contains other valid snmpd.conf
    configuration. Allows for great flexibility in building the snmpd.conf as
    required.

Known Limitations and Issues
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

None at this moment.

Contact Information
~~~~~~~~~~~~~~~~~~~

This charm was created by Bert JW Regeer <bertjw@regeer.org>

 - Project: https://gitlab.com/bertjwregeer/juju_snmpd/
 - Issues: https://gitlab.com/bertjwregeer/juju_snmpd/issues

