from charms.reactive import (
    when,
    when_any,
    when_not,
    when_file_changed,
)

import charms.apt

from charmhelpers.core import hookenv
from charmhelpers.core.hookenv import status_set
from charmhelpers.core.services.base import service_restart
from charmhelpers.core.templating import render


SNMPD_CONF = '/etc/snmp/snmpd.conf'


@when_not('apt.installed.snmpd')
def install_snmpd():
    charms.apt.queue_install(['snmpd'])
    status_set('maintenance', 'Queued installation of snmpd.')


@when('apt.installed.snmpd')
@when('config.changed')
def update_snmpd_conf():
    config = hookenv.config()
    status_set('maintenance', 'Updating snmpd configuration.')

    config_attrs = {
        'sysLocation': config['sysLocation'],
        'sysContact': config['sysContact'],
        'acls': [l.strip() for l in config['acls'].splitlines()],
        'other': [l.strip() for l in config['other'].splitlines()],
    }
    render(
        source='snmpd.conf',
        target=SNMPD_CONF,
        context=config_attrs,
        owner='root',
        group='root'
    )
    hookenv.open_port(161, protocol='UDP')
    hookenv.open_port(162, protocol='UDP')
    status_set('active', 'snmpd has been installed and re-configured.')


@when_file_changed('/etc/snmp/snmpd.conf', hash_type='sha256')
def config_file_updated():
    service_restart('snmpd')
    status_set('active', 'snmpd has been installed and re-configured.')


@when_any('host-system.available', 'host-system.connected')
def host_available():
    pass
