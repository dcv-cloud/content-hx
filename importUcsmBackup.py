#!/usr/bin/env python 
from ucsmsdk.ucshandle  import UcsHandle
from ucsmsdk.utils.ucsbackup import import_ucs_backup
import sys
import os
import time
file_dir=r"/root/scripts"
file_name=r"hx-cluster-ucsm-a.xml"


def ucsmUpload():
#while(True):

    time.sleep(90)
    os.system(r'echo "Starting UCSM Config Upload Script..."  >> /root/logs/importUcsmBackup.log')
    try:
        os.system(r'echo "Will Connect to UCSM now..."  >> /root/logs/importUcsmBackup.log')
        handle=UcsHandle("198.18.134.220","admin","C1sco12345",secure=False)
        handle.login()
        os.system(r'echo "Connected to UCSM, will push config now..."  >> /root/logs/importUcsmBackup.log')
        import_ucs_backup(handle, file_dir=file_dir, file_name=file_name, merge=True)
        os.system(r'echo "Configuration uploaded. Disconnecting..."  >> /root/logs/importUcsmBackup.log')
        handle.logout()
        os.system(r' echo "Done" >  /root/logs/ucsm.status')
        os.system(r'echo "Done"  >> /root/logs/importUcsmBackup.log')
        return True

    except Exception as e:
        if ("HTTP Error 503" in str(e)):
            errorMessage=str(e)
            os.system(r'echo "Error while pushing the config to UCS.Will restart the services and try again in 90 sec."  >> /root/logs/importUcsmBackup.log')
            os.system(r' echo ' + errorMessage + ' >> /root/logs/importUcsmBackup.log')
            os.system(r' curl --data "Submit=Restart UCS Emulator with Current Settings&confirm=yes" http://198.18.134.220:8082/settings/restart/emulator >> /root/logs/importUcsmBackup.log')
            return 60
        else:
            errorMessage=str(e)
            os.system(r'echo "Error while connecting to UCSM .Will try to connect again in 90 sec."  >> /root/logs/importUcsmBackup.log')
            #os.system(r' echo ' + errorMessage + ' >> /root/logs/importUcsmBackup.log')
            return 5
 


if __name__=='__main__':

    result=ucsmUpload()
    if result > 1:
        os.chmod(__file__,777)
        os.execv(__file__,sys.argv)
    else:        
        quit()

