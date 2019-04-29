#!/usr/bin/env python3

import unittest
import zaza.model
from pysnmp.hlapi import (
    SnmpEngine,
    getCmd,
    CommunityData,
    UdpTransportTarget,
    ContextData,
    ObjectType,
    ObjectIdentity,
)


class BasicTest(unittest.TestCase):
    def test_snmp_works(self):
        for series in ['xenial', 'bionic', 'cosmic', 'disco']:
            status = zaza.model.get_status() \
                .applications['ubuntu-{}'.format(series)]
            for unit in status["units"]:
                details = status['units'][unit]
                address = details['public-address']
                errorIndication, errorStatus, errorIndex, varBinds = next(
                    getCmd(SnmpEngine(),
                           CommunityData('public'),
                           UdpTransportTarget((address, 161)),
                           ContextData(),
                           ObjectType(ObjectIdentity('1.3.6.1.2.1.1.1.0')),
                           ObjectType(ObjectIdentity('1.3.6.1.2.1.1.6.0')))
                )
                self.assertIsNone(errorIndication)
