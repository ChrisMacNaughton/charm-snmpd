from charms.reactive import (
    when,
    when_not,
    when_file_changed,
)

import charms.apt

from charms.templating.jinja2 import render

from charmhelpers.core import hookenv
from charmhelpers.core.hookenv import status_set

SNMPD_CONF = '/etc/snmp/snmpd.conf'

@when_not('apt.installed.snmpd')
def install_snmpd():
    charms.apt.queue_install(['snmpd'])
    status_set('maintenance', 'Queued installation of snmpd.')

@when('apt.installed.snmpd')
def snmpd_installed():
    status_set('maintenance', 'snmpd has been installed.')

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
        'snmpd.conf',
        SNMPD_CONF,
        config_attrs,
        owner='root',
        group='root'
    )

    status_set('active', 'snmpd has been installed and re-configured.')

@when_file_changed('/etc/snmp/snmpd.conf', hash_type='sha256')
def config_file_updated():
    hookenv.service_restart('snmpd')
    status_set('active', 'snmpd has been installed and re-configured.')
