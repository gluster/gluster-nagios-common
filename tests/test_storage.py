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

import mock

from testrunner import GlusterNagiosTestCase as TestCaseBase
import glusternagios


class TestStorageUtils(TestCaseBase):
    @mock.patch('glusternagios.storage.utils')
    def testGetLvs(self, mock_utils):
        tmp_str = ["LVM2_LV_UUID=zjuuHG-HajL-PXxm-fjlL-5i00-EUnV-Wd2qL3^"
                   "LVM2_LV_NAME=lv_root^"
                   "LVM2_LV_PATH=/dev/vg_shubhnd/lv_root^"
                   "LVM2_LV_ATTR=-wi-ao---^"
                   "LVM2_LV_MAJOR=-1^"
                   "LVM2_LV_MINOR=-1^"
                   "LVM2_LV_READ_AHEAD=auto^"
                   "LVM2_LV_KERNEL_MAJOR=253^"
                   "LVM2_LV_KERNEL_MINOR=0^"
                   "LVM2_LV_KERNEL_READ_AHEAD=0.12^"
                   "LVM2_LV_SIZE=46728.00^"
                   "LVM2_LV_METADATA_SIZE=^"
                   "LVM2_SEG_COUNT=1^"
                   "LVM2_ORIGIN=^"
                   "LVM2_ORIGIN_SIZE=0^"
                   "LVM2_DATA_PERCENT=^"
                   "LVM2_SNAP_PERCENT=^"
                   "LVM2_METADATA_PERCENT=^"
                   "LVM2_COPY_PERCENT=^"
                   "LVM2_SYNC_PERCENT=^"
                   "LVM2_MOVE_PV=^"
                   "LVM2_CONVERT_LV=^"
                   "LVM2_MIRROR_LOG=^"
                   "LVM2_DATA_LV=^"
                   "LVM2_METADATA_LV=^"
                   "LVM2_POOL_LV=^"
                   "LVM2_LV_TAGS=^"
                   "LVM2_LV_TIME=2014-03-14 04:27:56 +0530^"
                   "LVM2_LV_HOST=shubh-nd.redhat.com^"
                   "LVM2_MODULES=^"
                   "LVM2_VG_NAME=vg_shubhnd",
                   "LVM2_LV_UUID=klTthp-BXN8-9loo-UUo9-Y2lB-6azb-X9fFdH^"
                   "LVM2_LV_NAME=lv_swap^"
                   "LVM2_LV_PATH=/dev/vg_shubhnd/lv_swap^"
                   "LVM2_LV_ATTR=-wi-ao---^"
                   "LVM2_LV_MAJOR=-1^"
                   "LVM2_LV_MINOR=-1^"
                   "LVM2_LV_READ_AHEAD=auto^"
                   "LVM2_LV_KERNEL_MAJOR=253^"
                   "LVM2_LV_KERNEL_MINOR=1^"
                   "LVM2_LV_KERNEL_READ_AHEAD=0.12^"
                   "LVM2_LV_SIZE=3968.00^"
                   "LVM2_LV_METADATA_SIZE=^"
                   "LVM2_SEG_COUNT=1^"
                   "LVM2_ORIGIN=^"
                   "LVM2_ORIGIN_SIZE=0^"
                   "LVM2_DATA_PERCENT=^"
                   "LVM2_SNAP_PERCENT=^"
                   "LVM2_METADATA_PERCENT=^"
                   "LVM2_COPY_PERCENT=^"
                   "LVM2_SYNC_PERCENT=^"
                   "LVM2_MOVE_PV=^"
                   "LVM2_CONVERT_LV=^"
                   "LVM2_MIRROR_LOG=^"
                   "LVM2_DATA_LV=^"
                   "LVM2_METADATA_LV=^"
                   "LVM2_POOL_LV=^"
                   "LVM2_LV_TAGS=^"
                   "LVM2_LV_TIME=2014-03-14 04:28:01 +0530^"
                   "LVM2_LV_HOST=shubh-nd.redhat.com^"
                   "LVM2_MODULES=^"
                   "LVM2_VG_NAME=vg_shubhnd"]
        mock_utils.execCmd.return_value = (0, tmp_str, "")
        ret_val = glusternagios.storage.getLvs()
        value_to_verify = {'/dev/vg_shubhnd/lv_root':
                          {'LVM2_SYNC_PERCENT': '',
                           'LVM2_LV_METADATA_SIZE': '',
                           'LVM2_LV_ATTR': '-wi-ao---',
                           'LVM2_MIRROR_LOG': '',
                           'LVM2_LV_KERNEL_MINOR': '0',
                           'LVM2_LV_SIZE': '46728.00',
                           'LVM2_LV_MAJOR': '-1',
                           'LVM2_ORIGIN_SIZE': '0',
                           'LVM2_LV_TIME': '2014-03-14 04:27:56 +0530',
                           'LVM2_METADATA_PERCENT': '',
                           'LVM2_POOL_LV': '',
                           'LVM2_COPY_PERCENT': '',
                           'LVM2_CONVERT_LV': '',
                           'LVM2_LV_KERNEL_READ_AHEAD': '0.12',
                           'LVM2_LV_NAME': 'lv_root',
                           'LVM2_LV_HOST': 'shubh-nd.redhat.com',
                           'LVM2_LV_UUID':
                           'zjuuHG-HajL-PXxm-fjlL-5i00-EUnV-Wd2qL3',
                           'LVM2_LV_MINOR': '-1',
                           'LVM2_DATA_PERCENT': '',
                           'LVM2_LV_KERNEL_MAJOR': '253',
                           'LVM2_LV_TAGS': '',
                           'LVM2_MODULES': '',
                           'LVM2_VG_NAME': 'vg_shubhnd',
                           'LVM2_METADATA_LV': '',
                           'LVM2_LV_PATH': '/dev/vg_shubhnd/lv_root',
                           'LVM2_DATA_LV': '',
                           'LVM2_LV_READ_AHEAD': 'auto',
                           'LVM2_SNAP_PERCENT': '',
                           'LVM2_MOVE_PV': '',
                           'LVM2_ORIGIN': '',
                           'LVM2_SEG_COUNT': '1'},
                           '/dev/vg_shubhnd/lv_swap':
                          {'LVM2_SYNC_PERCENT': '',
                           'LVM2_LV_METADATA_SIZE': '',
                           'LVM2_LV_ATTR': '-wi-ao---',
                           'LVM2_MIRROR_LOG': '',
                           'LVM2_LV_KERNEL_MINOR': '1',
                           'LVM2_LV_SIZE': '3968.00',
                           'LVM2_LV_MAJOR': '-1',
                           'LVM2_ORIGIN_SIZE': '0',
                           'LVM2_LV_TIME': '2014-03-14 04:28:01 +0530',
                           'LVM2_METADATA_PERCENT': '',
                           'LVM2_POOL_LV': '',
                           'LVM2_COPY_PERCENT': '',
                           'LVM2_CONVERT_LV': '',
                           'LVM2_LV_KERNEL_READ_AHEAD': '0.12',
                           'LVM2_LV_NAME': 'lv_swap',
                           'LVM2_LV_HOST': 'shubh-nd.redhat.com',
                           'LVM2_LV_UUID':
                           'klTthp-BXN8-9loo-UUo9-Y2lB-6azb-X9fFdH',
                           'LVM2_LV_MINOR': '-1',
                           'LVM2_DATA_PERCENT': '',
                           'LVM2_LV_KERNEL_MAJOR': '253',
                           'LVM2_LV_TAGS': '',
                           'LVM2_MODULES': '',
                           'LVM2_VG_NAME': 'vg_shubhnd',
                           'LVM2_METADATA_LV': '',
                           'LVM2_LV_PATH': '/dev/vg_shubhnd/lv_swap',
                           'LVM2_DATA_LV': '',
                           'LVM2_LV_READ_AHEAD': 'auto',
                           'LVM2_SNAP_PERCENT': '',
                           'LVM2_MOVE_PV': '',
                           'LVM2_ORIGIN': '',
                           'LVM2_SEG_COUNT': '1'}}
        self.assertEquals(ret_val, value_to_verify)

    @mock.patch('glusternagios.storage.utils')
    def testGetVgs(self, mock_utils):
        tmp_str = ["LVM2_VG_FMT=lvm2^"
                   "LVM2_VG_UUID=sTDsBh-DOc7-JR3y-RPHb-yz4R-aWP7-yZWQ0E^"
                   "LVM2_VG_NAME=vg_shubhnd^"
                   "LVM2_VG_ATTR=wz--n-^"
                   "LVM2_VG_SIZE=50696.00^"
                   "LVM2_VG_FREE=0^"
                   "LVM2_VG_SYSID=^"
                   "LVM2_VG_EXTENT_SIZE=4.00^"
                   "LVM2_VG_EXTENT_COUNT=12674^"
                   "LVM2_VG_FREE_COUNT=0^"
                   "LVM2_MAX_LV=0^"
                   "LVM2_MAX_PV=0^"
                   "LVM2_PV_COUNT=1^"
                   "LVM2_LV_COUNT=2^"
                   "LVM2_SNAP_COUNT=0^"
                   "LVM2_VG_SEQNO=3^"
                   "LVM2_VG_TAGS=^"
                   "LVM2_VG_MDA_COUNT=1^"
                   "LVM2_VG_MDA_USED_COUNT=1^"
                   "LVM2_VG_MDA_FREE=0.50^"
                   "LVM2_VG_MDA_SIZE=1.00^"
                   "LVM2_VG_MDA_COPIES=unmanaged^"
                   "LVM2_LV_PATH=/dev/vg_shubhnd/lv_root",
                   "LVM2_VG_FMT=lvm2^"
                   "LVM2_VG_UUID=sTDsBh-DOc7-JR3y-RPHb-yz4R-aWP7-yZWQ0E^"
                   "LVM2_VG_NAME=vg_shubhnd^"
                   "LVM2_VG_ATTR=wz--n-^"
                   "LVM2_VG_SIZE=50696.00^"
                   "LVM2_VG_FREE=0^"
                   "LVM2_VG_SYSID=^"
                   "LVM2_VG_EXTENT_SIZE=4.00^"
                   "LVM2_VG_EXTENT_COUNT=12674^"
                   "LVM2_VG_FREE_COUNT=0^"
                   "LVM2_MAX_LV=0^"
                   "LVM2_MAX_PV=0^"
                   "LVM2_PV_COUNT=1^"
                   "LVM2_LV_COUNT=2^"
                   "LVM2_SNAP_COUNT=0^"
                   "LVM2_VG_SEQNO=3^"
                   "LVM2_VG_TAGS=^"
                   "LVM2_VG_MDA_COUNT=1^"
                   "LVM2_VG_MDA_USED_COUNT=1^"
                   "LVM2_VG_MDA_FREE=0.50^"
                   "LVM2_VG_MDA_SIZE=1.00^"
                   "LVM2_VG_MDA_COPIES=unmanaged^"
                   "LVM2_LV_PATH=/dev/vg_shubhnd/lv_swap"]
        mock_utils.execCmd.return_value = (0, tmp_str, "")
        ret_val = glusternagios.storage.getVgs()
        value_to_verify = {'vg_shubhnd':
                           {'LVM2_VG_EXTENT_SIZE': '4.00',
                            'LVM2_VG_MDA_COUNT': '1',
                            'LVM2_VG_SYSID': '',
                            'LVM2_VG_ATTR': 'wz--n-',
                            'LVM2_VG_UUID':
                            'sTDsBh-DOc7-JR3y-RPHb-yz4R-aWP7-yZWQ0E',
                            'LVM2_VG_MDA_COPIES': 'unmanaged',
                            'LVM2_VG_MDA_FREE': '0.50',
                            'LVM2_VG_TAGS': '',
                            'LVM2_VG_FMT': 'lvm2',
                            'LVM2_PV_COUNT': '1',
                            'LVM2_VG_EXTENT_COUNT': '12674',
                            'LVM2_VG_MDA_SIZE': '1.00',
                            'LVM2_SNAP_COUNT': '0',
                            'LVM2_LV_COUNT': '2',
                            'LVM2_VG_NAME': 'vg_shubhnd',
                            'LVM2_VG_MDA_USED_COUNT': '1',
                            'LVM2_VG_FREE': '0',
                            'LVM2_VG_SEQNO': '3',
                            'LVM2_LV_PATH':
                            ['/dev/vg_shubhnd/lv_root',
                            '/dev/vg_shubhnd/lv_swap'],
                            'LVM2_VG_FREE_COUNT': '0',
                            'LVM2_MAX_PV': '0',
                            'LVM2_MAX_LV': '0',
                            'LVM2_VG_SIZE': '50696.00'}}
        self.assertEquals(ret_val, value_to_verify)

    @mock.patch('glusternagios.storage.utils')
    def testGetPvs(self, mock_utils):
        tmp_str = ["LVM2_PV_FMT=lvm2^"
                   "LVM2_PV_UUID=NF1uv0-eXJM-YJrn-Rc7b-Z2nw-E1Ly-3S24zn^"
                   "LVM2_DEV_SIZE=50699.00^"
                   "LVM2_PV_NAME=/dev/vda2^"
                   "LVM2_PV_MDA_FREE=0.50^"
                   "LVM2_PV_MDA_SIZE=1.00^"
                   "LVM2_PE_START=1.00^"
                   "LVM2_PV_SIZE=50696.00^"
                   "LVM2_PV_FREE=0^"
                   "LVM2_PV_USED=50696.00^"
                   "LVM2_PV_ATTR=a--^"
                   "LVM2_PV_PE_COUNT=12674^"
                   "LVM2_PV_PE_ALLOC_COUNT=12674^"
                   "LVM2_PV_TAGS=^"
                   "LVM2_PV_MDA_COUNT=1^"
                   "LVM2_PV_MDA_USED_COUNT=1^"
                   "LVM2_VG_NAME=vg_shubhnd"]
        mock_utils.execCmd.return_value = (0, tmp_str, "")
        ret_val = glusternagios.storage.getPvs()
        value_to_verify = {'/dev/vda2':
                           {'LVM2_PV_MDA_USED_COUNT': '1',
                            'LVM2_PV_UUID':
                            'NF1uv0-eXJM-YJrn-Rc7b-Z2nw-E1Ly-3S24zn',
                            'LVM2_PE_START': '1.00',
                            'LVM2_DEV_SIZE': '50699.00',
                            'LVM2_PV_NAME': '/dev/vda2',
                            'LVM2_PV_FMT': 'lvm2',
                            'LVM2_PV_MDA_COUNT': '1',
                            'LVM2_PV_MDA_FREE': '0.50',
                            'LVM2_PV_TAGS': '',
                            'LVM2_PV_FREE': '0',
                            'LVM2_PV_SIZE': '50696.00',
                            'LVM2_PV_PE_ALLOC_COUNT': '12674',
                            'LVM2_PV_MDA_SIZE': '1.00',
                            'LVM2_VG_NAME': 'vg_shubhnd',
                            'LVM2_PV_USED': '50696.00',
                            'LVM2_PV_ATTR': 'a--',
                            'LVM2_PV_PE_COUNT': '12674'}}
        self.assertEquals(ret_val, value_to_verify)

    @mock.patch('glusternagios.storage._getBrickMountPoints')
    @mock.patch('glusternagios.storage._getMountPoint')
    @mock.patch('glusternagios.storage._getProcMounts')
    @mock.patch('glusternagios.storage.glustercli.utils')
    @mock.patch('glusternagios.storage._getLvDetails')
    def testGetBricksForDisk(self,
                             mock_get_lv_details,
                             mock_utils,
                             mock_proc_mounts,
                             mock_get_mount_point,
                             mock_get_brick_mount_points):
        mock_get_lv_details.return_value = {'lv_root':
                                            {'LVM2_LV_NAME': 'lv_root',
                                             'LVM2_PV_NAME': '/dev/vda2',
                                             'LVM2_VG_NAME': 'vg_shubhnd'},
                                            'lv_swap':
                                            {'LVM2_LV_NAME': 'lv_swap',
                                             'LVM2_PV_NAME': '/dev/vda2',
                                             'LVM2_VG_NAME': 'vg_shubhnd'}}
        tmp_out = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
                   '<cliOutput>',
                   '  <opRet>0</opRet>',
                   '  <opErrno>0</opErrno>',
                   '  <opErrstr/>',
                   '  <volInfo>',
                   '    <volumes>',
                   '      <volume>',
                   '        <name>vol1</name>',
                   '        <id>9510c150-f471-450c-9c6e-1c489792bfb2</id>',
                   '        <status>1</status>',
                   '        <statusStr>Started</statusStr>',
                   '        <brickCount>1</brickCount>',
                   '        <distCount>1</distCount>',
                   '        <stripeCount>1</stripeCount>',
                   '        <replicaCount>1</replicaCount>',
                   '        <type>0</type>',
                   '        <typeStr>Distribute</typeStr>',
                   '        <transport>0</transport>',
                   '        <bricks>',
                   '          <brick>server-1:/tmp/vol1-a</brick>',
                   '        </bricks>',
                   '        <optCount>0</optCount>',
                   '        <options/>',
                   '      </volume>',
                   '      <count>1</count>',
                   '    </volumes>',
                   '  </volInfo>',
                   '</cliOutput>']
        mock_utils.execCmd.return_value = (0, tmp_out, "")
        mock_proc_mounts.return_value = {'devpts': '/dev/pts',
                                         '/dev/mapper/vg_shubhnd-lv_root': '/',
                                         'sysfs': '/sys',
                                         '/proc/bus/usb': '/proc/bus/usb',
                                         'proc': '/proc'}
        mock_get_mount_point.return_value = "/"
        mock_get_brick_mount_points.return_value = {'server-1:/tmp/vol1-a': "/"}
        bricks = glusternagios.storage.getBricksForDisk("/dev/vda2")
        self.assertEquals(bricks, ['server-1:/tmp/vol1-a'])

    @mock.patch('glusternagios.storage._getBrickDeviceName')
    @mock.patch('glusternagios.storage._getLvDetails')
    @mock.patch('glusternagios.storage.glustercli.utils')
    @mock.patch('glusternagios.storage._getMountPoint')
    def testGetDisksForBrick(self,
                             mock_get_mount_point,
                             mock_utils,
                             mock_get_lv_details,
                             mock_get_brick_device_name):
        mock_get_mount_point.return_value = "/"
        tmp_out = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
                   '<cliOutput>',
                   '  <opRet>0</opRet>',
                   '  <opErrno>0</opErrno>',
                   '  <opErrstr>(null)</opErrstr>',
                   '  <volStatus>',
                   '    <volumes>',
                   '      <volume>',
                   '        <volName>vol1</volName>',
                   '        <nodeCount>1</nodeCount>',
                   '        <node>',
                   '          <hostname>server-1</hostname>',
                   '          <path>/tmp/vol1-a</path>',
                   '          <status>1</status>',
                   '          <port>49152</port>',
                   '          <pid>8716</pid>',
                   '          <sizeTotal>48228589568</sizeTotal>',
                   '          <sizeFree>45994987520</sizeFree>',
                   '          <device>/dev/mapper/vg_shubhnd-lv_root</device>',
                   '          <blockSize>4096</blockSize>',
                   '          <mntOptions>rw</mntOptions>',
                   '          <fsName>ext4</fsName>',
                   '        </node>',
                   '      </volume>',
                   '    </volumes>',
                   '  </volStatus>',
                   '</cliOutput>']
        mock_utils.execCmd.return_value = (0, tmp_out, "")
        mock_get_lv_details.return_value = {'lv_root':
                                            {'LVM2_LV_NAME': 'lv_root',
                                             'LVM2_PV_NAME': '/dev/vda2',
                                             'LVM2_VG_NAME': 'vg_shubhnd'},
                                            'lv_swap':
                                            {'LVM2_LV_NAME': 'lv_swap',
                                             'LVM2_PV_NAME': '/dev/vda2',
                                             'LVM2_VG_NAME': 'vg_shubhnd'}}
        disk = glusternagios.storage.getDisksForBrick("server-1:"
                                                      "/tmp/vol1-a")
        self.assertEquals(disk, "/dev/vda2")
        mock_get_brick_device_name.return_value = "/dev/mapper/" \
                                                  "vg_shubhnd-lv_root"

        disk = glusternagios.storage.getDisksForBrick("server-1:/tmp/vol1-a",
                                                      "/dev/mapper/"
                                                      "vg_shubhnd-lv_root")
        self.assertEquals(disk, "/dev/vda2")
