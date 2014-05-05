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

import xml.etree.cElementTree as etree
import ethtool

import utils
from utils import CommandPath
from hostname import getHostNameFqdn, HostNameException

glusterCmdPath = CommandPath("gluster",
                             "/usr/sbin/gluster")


# Class for exception definition
class GlusterCmdFailedException(Exception):
    message = "command execution failed"

    def __init__(self, rc=0, out=(), err=()):
        self.rc = rc
        self.out = out
        self.err = err

    def __str__(self):
        o = '\n'.join(self.out)
        e = '\n'.join(self.err)
        if o and e:
            m = o + '\n' + e
        else:
            m = o or e

        s = self.message
        if m:
            s += '\nerror: ' + m
        if self.rc:
            s += '\nreturn code: %s' % self.rc
        return s


if hasattr(etree, 'ParseError'):
    _etreeExceptions = (etree.ParseError, AttributeError, ValueError)
else:
    _etreeExceptions = (SyntaxError, AttributeError, ValueError)


def _getGlusterVolCmd():
    return [glusterCmdPath.cmd, "--mode=script", "volume"]


def _getGlusterPeerCmd():
    return [glusterCmdPath.cmd, "--mode=script", "peer"]


def _getGlusterSystemCmd():
    return [glusterCmdPath.cmd, "system::"]


class HostStatus:
    CONNECTED = 'CONNECTED'
    DISCONNECTED = 'DISCONNECTED'
    UNKNOWN = 'UNKNOWN'


class VolumeStatus:
    ONLINE = 'ONLINE'
    OFFLINE = 'OFFLINE'


class VolumeQuotaStatus:
    DISABLED = 'DISABLED'
    OK = 'OK'
    SOFT_LIMIT_EXCEEDED = 'SOFT_LIMIT_EXCEEDED'
    HARD_LIMIT_EXCEEDED = 'HARD_LIMIT_EXCEEDED'


class VolumeSplitBrainStatus:
    NOTAPPLICABLE = 'NA'
    OK = 'OK'
    SPLITBRAIN = 'SPLITBRAIN'


class GeoRepStatus:
    OK = 'OK'
    NOT_STARTED = "NOT_STARTED"
    FAULTY = "FAULTY"
    PARTIAL_FAULTY = "PARTIAL_FAULTY"


class TransportType:
    TCP = 'TCP'
    RDMA = 'RDMA'


class TaskType:
    REBALANCE = 'REBALANCE'
    REPLACE_BRICK = 'REPLACE_BRICK'
    REMOVE_BRICK = 'REMOVE_BRICK'


def _getaddr(dev):
    dev_info_list = ethtool.get_interfaces_info(dev.encode('utf8'))
    addr = dev_info_list[0].ipv4_address
    if addr is None:
        addr = ''
    return addr


def _getIpAddresses():
    devinfo = {}
    for dev in ethtool.get_active_devices():
        try:
            devinfo[dev] = ethtool.get_ipaddr(dev)
        except IOError, e:
            print e

    return devinfo


def _getGlusterHostName():
    try:
        return getHostNameFqdn()
    except HostNameException:
        return ''


def _getLocalIpAddress():
    for ip in _getIpAddresses():
        if not ip.startswith('127.'):
            return ip
    return ''


def _execGluster(cmd):
    return utils.execCmd(cmd)


def _execGlusterXml(cmd):
    cmd.append('--xml')
    rc, out, err = utils.execCmd(cmd)
    if rc != 0:
        raise GlusterCmdFailedException(rc, out, err)
    try:
        tree = etree.fromstring('\n'.join(out))
        rv = int(tree.find('opRet').text)
        msg = tree.find('opErrstr').text
        errNo = int(tree.find('opErrno').text)
    except _etreeExceptions:
        raise GlusterCmdFailedException(err=out)
    if rv == 0:
        return tree
    else:
        if errNo != 0:
            rv = errNo
        raise GlusterCmdFailedException(rc=rv, err=[msg])


def hostUUIDGet():
    command = _getGlusterSystemCmd() + ["uuid", "get"]
    rc, out, err = _execGluster(command)
    if rc == 0:
        for line in out:
            if line.startswith('UUID: '):
                return line[6:]

    raise GlusterCmdFailedException()


def _parseVolumeStatus(tree):
    status = {'name': tree.find('volStatus/volumes/volume/volName').text,
              'bricks': [],
              'nfs': [],
              'shd': []}
    hostname = _getLocalIpAddress() or _getGlusterHostName()
    for el in tree.findall('volStatus/volumes/volume/node'):
        value = {}

        for ch in el.getchildren():
            value[ch.tag] = ch.text or ''

        if value['path'] == 'localhost':
            value['path'] = hostname

        if value['status'] == '1':
            value['status'] = 'ONLINE'
        else:
            value['status'] = 'OFFLINE'

        if value['hostname'] == 'NFS Server':
            status['nfs'].append({'hostname': value['path'],
                                  'port': value['port'],
                                  'status': value['status'],
                                  'pid': value['pid']})
        elif value['hostname'] == 'Self-heal Daemon':
            status['shd'].append({'hostname': value['path'],
                                  'status': value['status'],
                                  'pid': value['pid']})
        else:
            status['bricks'].append({'brick': '%s:%s' % (value['hostname'],
                                                         value['path']),
                                     'port': value['port'],
                                     'status': value['status'],
                                     'pid': value['pid']})
    return status


def _parseVolumeStatusDetail(tree):
    status = {'name': tree.find('volStatus/volumes/volume/volName').text,
              'bricks': []}
    for el in tree.findall('volStatus/volumes/volume/node'):
        value = {}

        for ch in el.getchildren():
            value[ch.tag] = ch.text or ''

        sizeTotal = int(value['sizeTotal'])
        value['sizeTotal'] = sizeTotal / (1024.0 * 1024.0)
        sizeFree = int(value['sizeFree'])
        value['sizeFree'] = sizeFree / (1024.0 * 1024.0)
        status['bricks'].append({'brick': '%s:%s' % (value['hostname'],
                                                     value['path']),
                                 'sizeTotal': '%.3f' % (value['sizeTotal'],),
                                 'sizeFree': '%.3f' % (value['sizeFree'],),
                                 'device': value['device'],
                                 'blockSize': value['blockSize'],
                                 'mntOptions': value['mntOptions'],
                                 'fsName': value['fsName']})
    return status


def _parseVolumeStatusClients(tree):
    status = {'name': tree.find('volStatus/volumes/volume/volName').text,
              'bricks': []}
    for el in tree.findall('volStatus/volumes/volume/node'):
        hostname = el.find('hostname').text
        path = el.find('path').text

        clientsStatus = []
        for c in el.findall('clientsStatus/client'):
            clientValue = {}
            for ch in c.getchildren():
                clientValue[ch.tag] = ch.text or ''
            clientsStatus.append({'hostname': clientValue['hostname'],
                                  'bytesRead': clientValue['bytesRead'],
                                  'bytesWrite': clientValue['bytesWrite']})

        status['bricks'].append({'brick': '%s:%s' % (hostname, path),
                                 'clientsStatus': clientsStatus})
    return status


def _parseVolumeStatusMem(tree):
    status = {'name': tree.find('volStatus/volumes/volume/volName').text,
              'bricks': []}
    for el in tree.findall('volStatus/volumes/volume/node'):
        brick = {'brick': '%s:%s' % (el.find('hostname').text,
                                     el.find('path').text),
                 'mallinfo': {},
                 'mempool': []}

        for ch in el.find('memStatus/mallinfo').getchildren():
            brick['mallinfo'][ch.tag] = ch.text or ''

        for c in el.findall('memStatus/mempool/pool'):
            mempool = {}
            for ch in c.getchildren():
                mempool[ch.tag] = ch.text or ''
            brick['mempool'].append(mempool)

        status['bricks'].append(brick)
    return status


def volumeStatus(volumeName, brick=None, option=None):
    """
    Get volume status

    Arguments:
       * VolumeName
       * brick
       * option = 'detail' or 'clients' or 'mem' or None
    Returns:
       When option=None,
         {'name': NAME,
          'bricks': [{'brick': BRICK,
                      'port': PORT,
                      'status': STATUS,
                      'pid': PID}, ...],
          'nfs': [{'hostname': HOST,
                   'port': PORT,
                   'status': STATUS,
                   'pid': PID}, ...],
          'shd: [{'hostname': HOST,
                  'status': STATUS,
                  'pid': PID}, ...]}

      When option='detail',
         {'name': NAME,
          'bricks': [{'brick': BRICK,
                      'sizeTotal': SIZE,
                      'sizeFree': FREESIZE,
                      'device': DEVICE,
                      'blockSize': BLOCKSIZE,
                      'mntOptions': MOUNTOPTIONS,
                      'fsName': FSTYPE}, ...]}

       When option='clients':
         {'name': NAME,
          'bricks': [{'brick': BRICK,
                      'clientsStatus': [{'hostname': HOST,
                                         'bytesRead': BYTESREAD,
                                         'bytesWrite': BYTESWRITE}, ...]},
                    ...]}

       When option='mem':
         {'name': NAME,
          'bricks': [{'brick': BRICK,
                      'mallinfo': {'arena': int,
                                   'fordblks': int,
                                   'fsmblks': int,
                                   'hblkhd': int,
                                   'hblks': int,
                                   'keepcost': int,
                                   'ordblks': int,
                                   'smblks': int,
                                   'uordblks': int,
                                   'usmblks': int},
                      'mempool': [{'allocCount': int,
                                   'coldCount': int,
                                   'hotCount': int,
                                   'maxAlloc': int,
                                   'maxStdAlloc': int,
                                   'name': NAME,
                                   'padddedSizeOf': int,
                                   'poolMisses': int},...]}, ...]}
    """
    command = _getGlusterVolCmd() + ["status", volumeName]
    if brick:
        command.append(brick)
    if option:
        command.append(option)
    try:
        xmltree = _execGlusterXml(command)
    except GlusterCmdFailedException as e:
        raise GlusterCmdFailedException(rc=e.rc, err=e.err)
    try:
        if option == 'detail':
            return _parseVolumeStatusDetail(xmltree)
        elif option == 'clients':
            return _parseVolumeStatusClients(xmltree)
        elif option == 'mem':
            return _parseVolumeStatusMem(xmltree)
        else:
            return _parseVolumeStatus(xmltree)
    except _etreeExceptions:
        raise GlusterCmdFailedException(err=[etree.tostring(xmltree)])


def _parseVolumeInfo(tree):
    """
        {VOLUMENAME: {'brickCount': BRICKCOUNT,
                      'bricks': [BRICK1, BRICK2, ...],
                      'options': {OPTION: VALUE, ...},
                      'transportType': [TCP,RDMA, ...],
                      'uuid': UUID,
                      'volumeName': NAME,
                      'volumeStatus': STATUS,
                      'volumeType': TYPE}, ...}
    """
    volumes = {}
    for el in tree.findall('volInfo/volumes/volume'):
        value = {}
        value['volumeName'] = el.find('name').text
        value['uuid'] = el.find('id').text
        value['volumeType'] = el.find('typeStr').text.upper().replace('-', '_')
        status = el.find('statusStr').text.upper()
        if status == 'STARTED':
            value["volumeStatus"] = VolumeStatus.ONLINE
        else:
            value["volumeStatus"] = VolumeStatus.OFFLINE
        value['brickCount'] = el.find('brickCount').text
        value['distCount'] = el.find('distCount').text
        value['stripeCount'] = el.find('stripeCount').text
        value['replicaCount'] = el.find('replicaCount').text
        transportType = el.find('transport').text
        if transportType == '0':
            value['transportType'] = [TransportType.TCP]
        elif transportType == '1':
            value['transportType'] = [TransportType.RDMA]
        else:
            value['transportType'] = [TransportType.TCP, TransportType.RDMA]
        value['bricks'] = []
        value['options'] = {}
        value['bricksInfo'] = []
        for b in el.findall('bricks/brick'):
            value['bricks'].append(b.text)
        for o in el.findall('options/option'):
            value['options'][o.find('name').text] = o.find('value').text
        for d in el.findall('bricks/brick'):
            brickDetail = {}
            #this try block is to maintain backward compatibility
            #it returns an empty list when gluster doesnot return uuid
            try:
                brickDetail['name'] = d.find('name').text
                brickDetail['hostUuid'] = d.find('hostUuid').text
                value['bricksInfo'].append(brickDetail)
            except AttributeError:
                break
        volumes[value['volumeName']] = value
    return volumes


def volumeInfo(volumeName=None, remoteServer=None):
    """
    Returns:
        {VOLUMENAME: {'brickCount': BRICKCOUNT,
                      'bricks': [BRICK1, BRICK2, ...],
                      'options': {OPTION: VALUE, ...},
                      'transportType': [TCP,RDMA, ...],
                      'uuid': UUID,
                      'volumeName': NAME,
                      'volumeStatus': STATUS,
                      'volumeType': TYPE}, ...}
    """
    command = _getGlusterVolCmd() + ["info"]
    if remoteServer:
        command += ['--remote-host=%s' % remoteServer]
    if volumeName:
        command.append(volumeName)
    try:
        xmltree = _execGlusterXml(command)
    except GlusterCmdFailedException as e:
        raise GlusterCmdFailedException(rc=e.rc, err=e.err)
    try:
        return _parseVolumeInfo(xmltree)
    except _etreeExceptions:
        raise GlusterCmdFailedException(err=[etree.tostring(xmltree)])


def _parseVolumeQuotaStatus(out, isDisabled=False):
    status_detail = {'status': VolumeQuotaStatus.OK,
              'soft_ex_dirs': [],
              'hard_ex_dirs': []}

    if isDisabled or out[0].startswith(
        'quota: No quota') or out[0].find('not enabled') > -1:
        status_detail['status'] = VolumeQuotaStatus.DISABLED
        return status_detail
    for line in out[2:]:
        l = line.split()
        if l[-1].find('Yes') > -1:
            status_detail[
                'status'] = VolumeQuotaStatus.HARD_LIMIT_EXCEEDED
            status_detail['hard_ex_dirs'].append(l[0])
            continue
        elif l[-2].find('Yes') > -1:
            if status_detail['status'
                             ] != VolumeQuotaStatus.HARD_LIMIT_EXCEEDED:
                status_detail['status'] = VolumeQuotaStatus.SOFT_LIMIT_EXCEEDED
            status_detail['soft_ex_dirs'].append(l[0])

    return status_detail


def _parseVolumeSelfHealSplitBrainInfo(out):
    value = {}
    splitbrainentries = 0
    for line in out:
        if line.startswith('Number of entries:'):
            entries = int(line.split(':')[1])
            if entries > 0:
                splitbrainentries += entries
    if splitbrainentries > 0:
        value['status'] = VolumeSplitBrainStatus.SPLITBRAIN
    else:
        value['status'] = VolumeSplitBrainStatus.OK
    value['unsyncedentries'] = splitbrainentries
    return value


def _parseVolumeGeoRepStatus(volumeName, out):
    detail = ""
    status = GeoRepStatus.OK
    # https://bugzilla.redhat.com/show_bug.cgi?id=1090910 - opened for xml
    # output. For now parsing below string output format
    # MASTER NODE                MASTER VOL    MASTER BRICK
    # SLAVE                     STATUS     CHECKPOINT STATUS  CRAWL STATUS
    slaves = {}
    all_status = ['ACTIVE', 'PASSIVE', 'FAULTY', 'NOT STARTED', 'INITIALISING']
    for line in out:
        if any(gstatus in line.upper() for gstatus in all_status):
            nodeline = line.split()
            slave = nodeline[3]
            if slaves.get(slave) is None:
                slaves[slave] = {'nodecount': 0,
                                 'faultcount': 0,
                                 'notstarted': 0}
            slaves[slave]['nodecount'] += 1
            if GeoRepStatus.FAULTY in line.upper() \
               or "NOT STARTED" in line.upper():
                node = nodeline[0]
                if GeoRepStatus.FAULTY == nodeline[4].upper():
                    slaves[slave]['faultcount'] += 1
                    tempstatus = GeoRepStatus.FAULTY
                else:
                    slaves[slave]['notstarted'] += 1
                    tempstatus = GeoRepStatus.NOT_STARTED
                detail += ("%s - %s - %s;" % (slave,
                                              node,
                                              tempstatus))
    for slave, count_dict in slaves.iteritems():
        if count_dict['nodecount'] == count_dict['faultcount']:
            status = GeoRepStatus.FAULTY
            break
        elif count_dict['faultcount'] > 0:
            status = GeoRepStatus.PARTIAL_FAULTY
        elif count_dict['notstarted'] > 0 and status == GeoRepStatus.OK:
            status = GeoRepStatus.NOT_STARTED
    return {volumeName: {'status': status, 'detail': detail}}


def volumeGeoRepStatus(volumeName, remoteServer=None):
    """
    Arguments:
       * VolumeName
    Returns:
        {VOLUMENAME: {'status': GEOREPSTATUS,
                      'detail': detailed message}}
    """
    command = _getGlusterVolCmd() + ["geo-replication", volumeName, "status"]
    if remoteServer:
        command += ['--remote-host=%s' % remoteServer]

    rc, out, err = _execGluster(command)

    if rc == 0:
        return _parseVolumeGeoRepStatus(volumeName, out)
    raise GlusterCmdFailedException(rc=rc, err=err)


def volumeHealSplitBrainStatus(volumeName, remoteServer=None):
    """
    Arguments:
       * VolumeName
    Returns:
        {VOLUMENAME: {'status': SELFHEALSTATUS,
                      'unsyncedentries': ENTRYCOUNT}}
    """
    command = _getGlusterVolCmd() + ["heal", volumeName, "info"]
    if remoteServer:
        command += ['--remote-host=%s' % remoteServer]

    rc, out, err = _execGluster(command)
    volume = {}
    value = {}
    if rc == 0:
        value = _parseVolumeSelfHealSplitBrainInfo(out)
        volume[volumeName] = value
        return volume
    else:
        if len(err) > 0 and err[0].find("is not of type replicate") > -1:
            value['status'] = VolumeSplitBrainStatus.NOTAPPLICABLE
            value['unsyncedentries'] = 0
            volume[volumeName] = value
            return volume
    raise GlusterCmdFailedException(rc=rc, err=err)


def volumeQuotaStatus(volumeName, remoteServer=None):
    """
    Returns:

        {status: OK|SOFT_LIMIT_EXCEEDED|HARD_LIMIT_EXCEEDED|DISABLED,
         soft_ex_dirs: ["dir1","dir2".....],
         hard_ex_dirs: ["dir1","dir2".....]}

    """
    command = _getGlusterVolCmd() + ["quota", volumeName, "list"]
    if remoteServer:
        command += ['--remote-host=%s' % remoteServer]

    rc, out, err = _execGluster(command)
    if rc == 0:
        return _parseVolumeQuotaStatus(out, isDisabled=False)
    else:
        if len(err) > 0 and err[0].find("Quota is disabled") > -1:
            return _parseVolumeQuotaStatus(out, isDisabled=True)
    raise GlusterCmdFailedException(rc, err)


def _parsePeerStatus(tree, gHostName, gUuid, gStatus):
    hostList = [{'hostname': gHostName,
                 'uuid': gUuid,
                 'status': gStatus}]

    for el in tree.findall('peerStatus/peer'):
        if el.find('state').text != '3':
            status = HostStatus.UNKNOWN
        elif el.find('connected').text == '1':
            status = HostStatus.CONNECTED
        else:
            status = HostStatus.DISCONNECTED
        hostList.append({'hostname': el.find('hostname').text,
                         'uuid': el.find('uuid').text,
                         'status': status})

    return hostList


def peerStatus():
    """
    Returns:
        [{'hostname': HOSTNAME, 'uuid': UUID, 'status': STATE}, ...]
    """
    command = _getGlusterPeerCmd() + ["status"]
    try:
        xmltree = _execGlusterXml(command)
    except GlusterCmdFailedException as e:
        raise GlusterCmdFailedException(rc=e.rc, err=e.err)
    try:
        return _parsePeerStatus(xmltree,
                                _getLocalIpAddress() or _getGlusterHostName(),
                                hostUUIDGet(), HostStatus.CONNECTED)
    except _etreeExceptions:
        raise GlusterCmdFailedException(err=[etree.tostring(xmltree)])
