import os
import time
import logging
import inspect
import time
import pexpect
import pexpectCommands as p

#Logging Config
logging.basicConfig(filename=r'/root/logs/create4NodeHxCluster.log',level=logging.DEBUG,format='%(asctime)s %(message)s')

#Remove the saved public keys
os.system(r'rm -f /root/.ssh/known_hosts')



def changePassword(currentPassword,newPassword):
    ###################################################################
    #Change Password in all controllers to dCloud standard C1sco12345
    ###################################################################

    logging.info("Changing Controller's password")

    cmd=[]

    command='passwd'
    cases=[pexpect.TIMEOUT,pexpect.EOF,"New password.*"]
    next=['timeout','eof',1]
    timeout=15
    cmd.append({'order':0,'cmd':command,'cases':cases,'next':next,'timeout':timeout})

    command=newPassword
    cases=[pexpect.TIMEOUT,pexpect.EOF,"Retype new password.*"]
    next=['timeout','eof',2]
    timeout=15
    cmd.append({'order':1,'cmd':command,'cases':cases,'next':next,'timeout':timeout})

    command=newPassword
    cases=[pexpect.TIMEOUT,pexpect.EOF,"root@HX-CTL-.*"]
    next=['timeout','eof', 'end']
    timeout=15
    cmd.append({'order':2,'cmd':command,'cases':cases,'next':next,'timeout':timeout})

    nodes=[]

    nodeIP='198.18.135.205'
    nodeUsername='root'
    nodePassword=currentPassword
    nodeLoginPrompt='HX-CTL-01'
    nodes.append({'nodeIP':nodeIP, 'nodeUsername':nodeUsername, 'nodePassword':nodePassword, 'nodeLoginPrompt':nodeLoginPrompt})

    nodeIP='198.18.135.206'
    nodeUsername='root'
    nodePassword=currentPassword
    nodeLoginPrompt='HX-CTL-02'
    nodes.append({'nodeIP':nodeIP, 'nodeUsername':nodeUsername, 'nodePassword':nodePassword, 'nodeLoginPrompt':nodeLoginPrompt})

    nodeIP='198.18.135.207'
    nodeUsername='root'
    nodePassword=currentPassword
    nodeLoginPrompt='HX-CTL-03'
    nodes.append({'nodeIP':nodeIP, 'nodeUsername':nodeUsername, 'nodePassword':nodePassword, 'nodeLoginPrompt':nodeLoginPrompt})

    nodeIP='198.18.135.208'
    nodeUsername='root'
    nodePassword=currentPassword
    nodeLoginPrompt='HX-CTL-04'
    nodes.append({'nodeIP':nodeIP, 'nodeUsername':nodeUsername, 'nodePassword':nodePassword, 'nodeLoginPrompt':nodeLoginPrompt})


    for node in nodes:
        logging.info("Changing password for node " + str(node))
        p.pexpectExecute(username=node['nodeUsername'], password=node['nodePassword'], loginPrompt=node['nodeLoginPrompt'],ipAddress=node['nodeIP'],cmd=cmd)
        time.sleep(2)
    logging.info("Changing passwords done")



def createCluster():
    ###################################################################
    #Start HX Cluster Creation  
    ###################################################################

    cmd=[]

    logging.info("About to start Cluster Creation")

    command='sudo stcli cluster create --name hx-storage-b --ip 192.168.0.100 --mgmt-ip 198.18.135.200 --node-ips 198.18.135.201 198.18.135.202 198.18.135.203 198.18.135.204  --vcenter-datacenter dCloud-HX-DC-B  --vcenter-cluster hx-cluster-b  --vcenter-url https://198.18.133.30 --vcenter-user administrator@vsphere.local --vcenter-password C1sco12345! --data-replication-factor 2'
    cases=[pexpect.TIMEOUT,pexpect.EOF,"Enter Controller's Root Password.*"]
    next=['timeout','eof',1]
    timeout=20
    cmd.append({'order':0,'cmd':command,'cases':cases,'next':next,'timeout':timeout})

    command='C1sco12345'
    cases=[pexpect.TIMEOUT,pexpect.EOF,"Enter ESX Username.*"]
    next=['timeout','eof',2]
    timeout=20
    cmd.append({'order':1,'cmd':command,'cases':cases,'next':next,'timeout':timeout})

    command='root'
    cases=[pexpect.TIMEOUT,pexpect.EOF,"Enter ESX Root Password.*"]
    next=['timeout','eof',3]
    timeout=20
    cmd.append({'order':2,'cmd':command,'cases':cases,'next':next,'timeout':timeout})

    command='Cisco123'
    cases=[pexpect.TIMEOUT,pexpect.EOF,"Do you accept this EULA.*"]
    next=['timeout','eof',4]
    timeout=20
    cmd.append({'order':3,'cmd':command,'cases':cases,'next':next,'timeout':timeout})

    command='Y'
    cases=[pexpect.TIMEOUT,pexpect.EOF,"root@HX-CTL-.*"]
    next=['timeout','eof','end']
    timeout=1000
    cmd.append({'order':4,'cmd':command,'cases':cases,'next':next,'timeout':timeout})


    nodes=[]

    nodeIP='198.18.135.205'
    nodeUsername='root'
    nodePassword='C1sco12345'
    nodeLoginPrompt='HX-CTL-01'
    nodes.append({'nodeIP':nodeIP, 'nodeUsername':nodeUsername, 'nodePassword':nodePassword, 'nodeLoginPrompt':nodeLoginPrompt})


    for node in nodes:
        p.pexpectExecute(username=node['nodeUsername'], password=node['nodePassword'], loginPrompt=node['nodeLoginPrompt'],ipAddress=node['nodeIP'],cmd=cmd)
        time.sleep(30)


    ###################################################################
    #Mark  HX Cluster Creation  Complete on file /root/logs/hx.status
    ###################################################################
    os.system(r' echo "Done" >> /root/logs/hx.status')


changePassword('Cisco123','C1sco12345')
createCluster()

