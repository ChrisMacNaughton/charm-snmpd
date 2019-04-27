#!/usr/bin/env python3

import unittest
import zaza.model
import zaza.utilities.juju as juju_utils
from pysnmp.hlapi import *

class BasicTest(unittest.TestCase):
    def test_snmp_works(self):
        status = zaza.model.get_status().applications['ubuntu']
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