import os
import ftplib
from ftplib import FTP
import logging
import sys
import time
import subprocess
COMMON_FOLDER='/dcloud_maintenance'

logging.basicConfig(filename='/root/logs/tools_masterpy.log',level=logging.DEBUG,format='%(asctime)s %(message)s')

if __name__ == "__main__":

    #get arguments: First one is the source folder
    folder=sys.argv[1]
    #Second Argument is the type of session: demo or lab
    session_type=sys.argv[2]

    if session_type == "demo":

        #Delete Old Log Files
        os.system(r' rm -f /root/logs/* ')
        os.system(r"echo '***************** Old log files deleted...*****************' >>/root/logs/tools_masterpy.log" )
 
        #Download Scripts from folder /dcv/hyperflex_v4/tools-scripts to /root/scripts
        #os.system(r"echo '***************** Download Scripts from /dcv/hyperflex_v4/tools-scripts *****************' >>/root/logs/tools_masterpy.log") 
        #os.system(r'cd /root/downloads && wget -r ftp://download:C1sco12345@198.19.255.136/dcv/hyperflex_v4/tools-scripts/* >> /root/logs/tools_masterpy.log')
        #os.system(r'cp -r /root/downloads/198.19.255.136/dcv/hyperflex_v4/tools-scripts/* /root/scripts >> /root/logs/tools_masterpy.log ')
        #os.system(r'rm -fr /root/downloads/198.19.255.136/ >> /root/logs/tools_masterpy.log ')

        #Enable Task View for all Users in vCenter
        #os.system(r' nohup /bin/python2.7 /root/scripts/enableAllUsersTaskViewInVcenter.py &')

        #Execute Script that triggers Cleaner Service in each HX VM Controller
        #os.system(r' nohup /bin/python2.7 /root/scripts/triggerCleanerInVMControllers.py &')

        #Execute Script that adds NTP/DNS Services in the HX Controllers and Configures the CLeaner
        #os.system(r' nohup /bin/python2.7 /root/scripts/addServicesInHX.py &')

        #Install DvFilter in the Nested Hosts
        #os.system(r' nohup /bin/python2.7 /root/scripts/installDvfilterInHosts.py &')

        #Run pingall.sh in all hosts
        #os.system(r' nohup /bin/python2.7 /root/scripts/runPingallInHosts.py &')

        #Run import UCSM-A Configuration
        os.system(r' nohup /bin/python2.7 /root/scripts/importUcsmBackupA.py &')


