"""
Written by Michael Rice <michael@michaelrice.org>
Github: https://github.com/michaelrice
Website: https://michaelrice.github.io/
Blog: http://www.errr-online.com/
This code has been released under the terms of the Apache 2.0 licenses
http://www.apache.org/licenses/LICENSE-2.0.html
"""

from __future__ import print_function
from pyVmomi import VmomiSupport

from pyVmomi import vim
import time
import atexit
import logging
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import SubElement
from xml.etree.ElementTree import tostring
import ssl
import requests
from pyVim import connect




logging.basicConfig(filename=r'/root/logs/fixHxDisks.log',level=logging.DEBUG,format='%(asctime)s %(message)s')




def reset_alarm(**kwargs):
    """
    Resets an alarm on a given HostSystem in a vCenter to the green state
    without someone having to log in to do it manually.
    This is done by using an unexposed API call. This requires us
    to manually construct the SOAP envelope. We use the session key
    that pyvmomi provides during its connection.
    More information can be found about this process
    in this article written by William Lam:
    http://www.virtuallyghetto.com/2010/10/how-to-ack-reset-vcenter-alarm.html
    I adopted his process from perl to groovy:
    https://gist.github.com/michaelrice/d54a237295e017b032a5
    and from groovy now to python.
    Usage:
    SI = SmartConnect(xxx)
    HOST = SI.content.searchIndex.FindByxxx(xxx)
    alarm.reset_alarm(entity_moref=HOST._moId, entity_type='HostSystem',
                      alarm_moref='alarm-1', service_instance=SI)
    :param service_instance:
    :param entity_moref:
    :param alarm:
    :return boolean:
    """
    service_instance = kwargs.get("service_instance")
    payload = _build_payload(**kwargs)
    logging.debug(payload)
    session = service_instance._stub
    if not _send_request(payload, session):
        return False
    return True


def _build_payload(**kwargs):
    """
    Builds a SOAP envelope to send to the vCenter hidden API
    :param entity_moref:
    :param alarm_moref:
    :param entity_type:
    :return:
    """
    entity_moref = kwargs.get("entity_moref")
    entity_type = kwargs.get("entity_type")
    alarm_moref = kwargs.get("alarm_moref")
    if not entity_moref or not entity_type or not alarm_moref:
        raise ValueError("entity_moref, entity_type, and alarm_moref "
                         "must be set")

    attribs = {
        'xmlns:xsd': 'http://www.w3.org/2001/XMLSchema',
        'xmlns:xsi': 'http://www.w3.org/2001/XMLSchema-instance',
        'xmlns:soap': 'http://schemas.xmlsoap.org/soap/envelope/'
    }
    root = Element('soap:Envelope', attribs)
    body = SubElement(root, 'soap:Body')
    alarm_status = SubElement(body, 'SetAlarmStatus', {'xmlns': 'urn:vim25'})
    this = SubElement(alarm_status, '_this', {
        'xsi:type': 'ManagedObjectReference',
        'type': 'AlarmManager'
    })
    this.text = 'AlarmManager'
    alarm = SubElement(alarm_status, 'alarm', {'type': 'Alarm'})
    alarm.text = alarm_moref
    entity = SubElement(alarm_status, 'entity', {
        'xsi:type': 'ManagedObjectReference',
        'type': entity_type
    })
    entity.text = entity_moref
    status = SubElement(alarm_status, 'status')
    status.text = 'green'
    # I hate hard coding this but I have no idea how to do it any other way
    # pull requests welcome :)
    return '<?xml version="1.0" encoding="UTF-8"?>{0}'.format(tostring(root))


def _send_request(payload=None, session=None):
    """
    Using requests we send a SOAP envelope directly to the
    vCenter API to reset an alarm to the green state.
    :param payload:
    :param session:
    :return:
    """
    stub = session
    host_port = stub.host
    # Ive seen some code in pyvmomi where it seems like we check for http vs
    # https but since the default is https do people really run it on http?
    url = 'https://{0}/sdk'.format(host_port)
    logging.debug("Sending {0} to {1}".format(payload, url))
    # I opted to ignore invalid ssl here because that happens in pyvmomi.
    # Once pyvmomi validates ssl it wont take much to make it happen here.
    res = requests.post(url=url, data=payload, headers={
        'Cookie': stub.cookie,
        'SOAPAction': 'urn:vim25',
        'Content-Type': 'application/xml'
    }, verify=False)
    if res.status_code != 200:
        logging.debug("Failed to reset alarm. HTTP Status: {0}".format(
            res.status_code))
        return False
    return True


def print_triggered_alarms(entity=None):
    """
    This is a useful method if you need to print out the alarm morefs
    :param entity:
    """
    alarms = entity.triggeredAlarmState
    for alarm in alarms:
        logging.info("#"*40)
        # The alarm key looks like alarm-101.host-95
        logging.info("alarm_moref: {0}".format(alarm.key.split('.')[0]))
        logging.info("alarm status: {0}".format(alarm.overallStatus))


def get_alarm_refs(entity=None):
    """
    Useful method that will return a list of dict with the moref and alarm
    status for all triggered alarms on a given entity.
    :param entity:
    :return list: [{'alarm':'alarm-101', 'status':'red'}]
    """
    alarm_states = entity.triggeredAlarmState
    ret = []
    for alarm_state in alarm_states:
        tdict = {
            "alarm": alarm_state.key.split('.')[0],
            "status": alarm_state.overallStatus
        }
        ret.append(tdict)
    return ret

def connectVcenter(host='', user='', password='', port=443):
    context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
    context.verify_mode = ssl.CERT_NONE

    service_instance = connect.SmartConnect(host=host,
                                            user=user,
                                            pwd=password,
                                            port=int(port),
                                            sslContext=context)
    if not service_instance:
        logging.info("Unable to connect with the vCenter Server using the provided credentials")
        return False

    atexit.register(connect.Disconnect, service_instance)
    #content = service_instance.RetrieveContent()
    logging.info('Conntected to ' + str(host))
    return service_instance



def powerOnVms(content, vim_type=[vim.VirtualMachine], vmNames=[]):
    logging.info('Looking for Virtual Machines')
    objView = content.viewManager.CreateContainerView(content.rootFolder,[vim.VirtualMachine],True)
    vmList = objView.view
    objView.Destroy()
    tasks = [vm.PowerOn() for vm in vmList if vm.name in vmNames]
    return 




def getStorageSystem(content, vim_type=[vim.host.StorageSystem], hostName=''):
    logging.info('Looking for Storage system')

    hostObjectView = content.viewManager.CreateContainerView(content.rootFolder,[vim.HostSystem],True)
    hosts = hostObjectView.view
    hostObjectView.Destroy()

    theHost=[]
    for host in hosts:
        logging.info('Looking for host with hostname  ' + str(hostName) + ', now checking host  ' + str(host.name))
        if host.name == hostName:
            theHost= host
            logging.info('Found name matching Host ( '+hostName+'). Compute Resource is ' + str(theHost))
    if not theHost:
        logging.info('Could not find a name matching host. There must be an error. Failing...')
        return False

    configManager= theHost.configManager
    storageSystem = configManager.storageSystem
    host_file_sys_vol_mount_info = storageSystem.fileSystemVolumeInfo.mountInfo
    # Map all filesystems
    #for host_mount_info in host_file_sys_vol_mount_info:
    # Extract only VMFS volumes
            #logging.info(str(host_mount_info.volume.type))
            #logging.info('uuid: ' + str(host_mount_info.volume.uuid))
            #logging.info('capacity: ' + str(host_mount_info.volume.capacity))
            #logging.info('vmfs_version: ' +str(host_mount_info.volume.version))
            #logging.info('local: ' + str(host_mount_info.volume.local))
            #logging.info('ssd: ' + str(host_mount_info.volume.ssd))

    return storageSystem



def mountVmfsWithVmfsLabel(uuid='' , vmName='', vmfsLabel='', hostName='', host='', user='', password='', port=443):

    logging.info('About to mount VMfs Datastores with UUID ' + str(uuid) + ' @host ' + str(host))

    service_instance = connectVcenter(host=host, user=user, password=password)
    if not service_instance:
        logginginfo('Not able to connect to host. Failing...')
        return False

    content = service_instance.RetrieveContent()
    storageSystem = getStorageSystem(content, hostName=hostName)
    if storageSystem:
        #logging.info('Refreshing Storage System for Host')
        #storageSystem.RefreshStorageSystem()
        #storageSystem.RescanVmfs()
        #storageSystem.MountVmfsVolume(uuid)

        UnresolvedVmfsResolutionSpec=vim.host.UnresolvedVmfsResolutionSpec() 
        UnresolvedVmfsResolutionSpec.uuidResolution='forceMount'

        UnresolvedVmfsVolumes=storageSystem.QueryUnresolvedVmfsVolume()
        extentDevicePath=[]
        for UnresolvedVmfsVolume in UnresolvedVmfsVolumes:
            logging.info('UnresolvedVmfsVolume with Label ' + str(UnresolvedVmfsVolume.vmfsLabel) + ' and UUID ' + str(UnresolvedVmfsVolume.vmfsUuid))
            if UnresolvedVmfsVolume.vmfsLabel == vmfsLabel:
                for extent in UnresolvedVmfsVolume.extent:
                    logging.info('Device Path is ' + str(extent.devicePath))
                    logging.info('Device is ' +str(extent.device))
                    extentDevicePath.append(extent.devicePath)
                    #UnresolvedVmfsResolutionSpec.extentDevicePath.append(str(extent.devicePath))


        if len(extentDevicePath)>0 :
            logging.info('extenDevicePath is not empty, there is a vmfs to mount. Lets send request')
            logging.info(str(extentDevicePath))
            UnresolvedVmfsResolutionSpec=vim.host.UnresolvedVmfsResolutionSpec() 
            UnresolvedVmfsResolutionSpec.uuidResolution='forceMount'
            UnresolvedVmfsResolutionSpec.extentDevicePath=extentDevicePath
            #UnresolvedVmfsResolutionSpec.extentDevicePath=[r'/vmfs/devices/disks/naa.6000c29441cac359dc2375d51883b62d:3']
            print(str(vars(UnresolvedVmfsResolutionSpec)))
            logging.info('UnresolvedVmfsResolutionSpec : ' + str(UnresolvedVmfsResolutionSpec)+ ' ' + str(UnresolvedVmfsResolutionSpec.extentDevicePath) + ' ' + str(UnresolvedVmfsResolutionSpec.uuidResolution))
            storageSystem.ResolveMultipleUnresolvedVmfsVolumes([UnresolvedVmfsResolutionSpec])
            logging.info("VMFS mount operation request sent")
            time.sleep(10)
            powerOnVms(content, vmNames=[vmName])
            return True
        else:
            logging.info('VMFS with vmfsLabel ' +str(vmfsLabel)+ '  not found. Mount Operation NOT send')
            return False
    else:
        logging.info('StorageSystem not found. Mount operation request NOT sent')
        return False 





def mountAllVmfs():
    while(True):
        toMount=[{'host':'198.18.134.201','vmName':'stCtlVM-198.18.134.201','hostName':'HX-01.eng.storvisor.com','vmfsLabel':'SpringpathDS-198.18.134.201','done':False},\
                 {'host':'198.18.134.202','vmName':'stCtlVM-198.18.134.202','hostName':'HX-02.eng.storvisor.com','vmfsLabel':'SpringpathDS-198.18.134.202','done':False},\
                 {'host':'198.18.134.203','vmName':'stCtlVM-198.18.134.203','hostName':'HX-03.eng.storvisor.com','vmfsLabel':'SpringpathDS-198.18.134.203','done':False},\
                 {'host':'198.18.134.204','vmName':'stCtlVM-198.18.134.204','hostName':'HX-04.eng.storvisor.com','vmfsLabel':'SpringpathDS-198.18.134.204','done':False},\
                 {'host':'198.18.135.201','vmName':'stCtlVM-198.18.135.201','hostName':'HX-01.eng.storvisor.com','vmfsLabel':'SpringpathDS-198.18.135.201','done':False},\
                 {'host':'198.18.135.202','vmName':'stCtlVM-198.18.135.202','hostName':'HX-02.eng.storvisor.com','vmfsLabel':'SpringpathDS-198.18.135.202','done':False},\
                 {'host':'198.18.135.203','vmName':'stCtlVM-198.18.135.203','hostName':'HX-03.eng.storvisor.com','vmfsLabel':'SpringpathDS-198.18.135.203','done':False},\
                 {'host':'198.18.135.204','vmName':'stCtlVM-198.18.135.204','hostName':'HX-04.eng.storvisor.com','vmfsLabel':'SpringpathDS-198.18.135.204','done':False}]



        for vmfs in toMount:
            try:
                mountVmfsWithVmfsLabel(hostName=vmfs['hostName'],vmName=vmfs['vmName'], host=vmfs['host'], vmfsLabel=vmfs['vmfsLabel'], user='root', password='Cisco123')
            except Exception as e:
                logging.info("Error while trying to fix disks  for host " + str(vmfs['host']) + " : " + str(e))

        time.sleep(30)


def clearAlarms():

    while(True):
        SI=connectVcenter(host='198.18.133.30', user='administrator@vsphere.local', password='C1sco12345!')

        for host in ['198.18.134.201','198.18.134.202','198.18.134.203','198.18.134.204','198.18.135.201','198.18.135.202','198.18.135.203','198.18.135.204']:
            try:
                theHost = SI.content.searchIndex.FindByIp(None, host, False)
                if theHost:
                    logging.info("Getting list of Alarms for host " + str(host))
                    #print_triggered_alarms(entity=theHost)
                    alarms=get_alarm_refs(entity=theHost)
                    logging.info(str(alarms))
                    for alarm in alarms:
                        logging.info("Resetting Alarm " + str(alarm['alarm']) + " on host " + str(host)) 
                        reset_alarm(entity_moref=theHost._moId, entity_type='HostSystem',alarm_moref=alarm['alarm'], service_instance=SI)
                  
                    logging.info("Trying to Disable SSH warning on host " + str(host))
                    advOpt =theHost.configManager.advancedOption
                    opt = advOpt.QueryOptions('UserVars.SuppressShellWarning')
                    opt[0].value = VmomiSupport.vmodlTypes['long'](1)
                    advOpt.UpdateOptions(opt)

                else:
                    logging.info("Unable to find host " + str(host))
            except Exception as e:
                logging.info("Error while searching for host " + str(host) + " : " + str(e))

        time.sleep(30)

  




mountAllVmfs()
