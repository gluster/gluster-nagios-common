#
# Copyright 2014 Red Hat, Inc.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301 USA
#
# Refer to the README and COPYING files for full details of the license
#

import errno
import xml.etree.cElementTree as etree

from testrunner import GlusterNagiosTestCase as TestCaseBase
from glusternagios import utils


class RetryTests(TestCaseBase):
    def testStopCallback(self):
        counter = [0]
        limit = 4

        def stopCallback():
            counter[0] += 1
            if counter[0] == limit:
                return True

            return False

        def foo():
            raise RuntimeError("If at first you don't succeed, try, try again."
                               "Then quit. There's no point in being a damn"
                               "fool about it.")
                               # W. C. Fields

        self.assertRaises(RuntimeError, utils.retry, foo, tries=(limit + 10),
                          sleep=0, stopCallback=stopCallback)
        # Make sure we had the proper amount of iterations before failing
        self.assertEquals(counter[0], limit)


class CommandPathTests(TestCaseBase):
    def testExisting(self):
        cp = utils.CommandPath('sh', 'utter nonsense', '/bin/sh')
        self.assertEquals(cp.cmd, '/bin/sh')

    def testMissing(self):
        NAME = 'nonsense'
        try:
            utils.CommandPath(NAME, 'utter nonsense').cmd
        except OSError as e:
            self.assertEquals(e.errno, errno.ENOENT)
            self.assertIn(NAME, e.strerror)


class ExecCmdTests(TestCaseBase):
    def testSuccess(self):
        (rc, out, err) = utils.execCmd(["true"])
        self.assertEquals(rc, 0)

    def testFailure(self):
        (rc, out, err) = utils.execCmd(["false"])
        self.assertEquals(rc, 1)

    def testOSError(self):
        def _runUnknown():
            (rc, out, err) = utils.execCmd(["unknown"])

        self.assertRaises(OSError, _runUnknown)


class xml2dictTests(TestCaseBase):
    def testSuccess(self):
        expectedDict = {'timestamp':
                        {'date': '2014-03-18',
                         'interval': '60',
                         'network': {'net-dev': [{'iface': 'wlp3s0',
                                                  'rxcmp': '0.00',
                                                  'rxkB': '0.00',
                                                  'rxmcst': '0.00',
                                                  'rxpck': '0.00',
                                                  'txcmp': '0.00',
                                                  'txkB': '0.00',
                                                  'txpck': '0.00'},
                                                 {'iface': 'lo',
                                                  'rxcmp': '0.00',
                                                  'rxkB': '0.00',
                                                  'rxmcst': '0.00',
                                                  'rxpck': '0.00',
                                                  'txcmp': '0.00',
                                                  'txkB': '0.00',
                                                  'txpck': '0.00'},
                                                 {'iface': 'virbr0-nic',
                                                  'rxcmp': '0.00',
                                                  'rxkB': '0.00',
                                                  'rxmcst': '0.00',
                                                  'rxpck': '0.00',
                                                  'txcmp': '0.00',
                                                  'txkB': '0.00',
                                                  'txpck': '0.00'},
                                                 {'iface': 'virbr0',
                                                  'rxcmp': '0.00',
                                                  'rxkB': '0.00',
                                                  'rxmcst': '0.00',
                                                  'rxpck': '0.00',
                                                  'txcmp': '0.00',
                                                  'txkB': '0.00',
                                                  'txpck': '0.00'},
                                                 {'iface': 'enp0s26u1u2',
                                                  'rxcmp': '0.00',
                                                  'rxkB': '0.01',
                                                  'rxmcst': '0.00',
                                                  'rxpck': '0.13',
                                                  'txcmp': '0.00',
                                                  'txkB': '0.03',
                                                  'txpck': '0.25'},
                                                 {'iface': 'em1',
                                                  'rxcmp': '0.00',
                                                  'rxkB': '0.00',
                                                  'rxmcst': '0.00',
                                                  'rxpck': '0.00',
                                                  'txcmp': '0.00',
                                                  'txkB': '0.00',
                                                  'txpck': '0.00'}],
                                     'per': 'second'},
                         'time': '13:53:01',
                         'utc': '1'}}
        with open("xml2dictSuccess.xml") as f:
            out = f.read()
            tree = etree.fromstring(out)
            outDict = utils.xml2dict(tree)
        self.assertEquals(expectedDict, outDict)

    def testAttributeError(self):
        def _xml2dict():
            utils.xml2dict("not an etree object")

        self.assertRaises(AttributeError, _xml2dict)


class convertsizeTests(TestCaseBase):
    def testBytesToMB(self):
        retVal = utils.convertSize(778999, 'B', 'MB')
        assert (round(retVal, 2) == 0.74)

    def testPBtoMB(self):
        retVal = utils.convertSize(8, 'PB', 'MB')
        assert (round(retVal, 0) == 8589934592)

    def testInvalidInput(self):
        with self.assertRaises(ValueError):
            utils.convertSize(89, 'P', 'M')

    def testMBToMB(self):
        retVal = utils.convertSize(900, 'MB', 'MB')
        assert (retVal == 900)
