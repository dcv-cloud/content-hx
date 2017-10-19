import os
import logging
import sys
import time
import subprocess

logging.basicConfig(filename='/root/logs/createClusterBFromScript.log',level=logging.DEBUG,format='%(asctime)s %(message)s')

if __name__ == "__main__":

    logging.info("Starting unattended creation of HX Cluster B")
#    quit()

    os.system(r'rm -f /root/logs/*.status ')

    #Import UCSD Configuration
    logging.info("Starting UCSM config upload")
    os.system(r' nohup /bin/python2.7 /root/scripts/importUcsmBackupB.py &')

    #Create Vmware Cluster
    logging.info("Starting vCenter Cluster creation")
    os.system(r' nohup /bin/python /root/scripts/createVmwareCluster.py &')

    time.sleep(30)

    #Create HX 4-node Cluster
    logging.info("Starting 4Node Cluster Creation")
    os.system(r' nohup /bin/python /root/scripts/create4NodeHxCluster.py &')








