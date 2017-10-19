import os
import time
import logging
import inspect
import time



import pexpect
import pexpectCommands as p

logging.basicConfig(filename=r'/root/logs/createHxCluster.log',level=logging.DEBUG,format='%(asctime)s %(message)s')


#Remove the saved public keys
os.system(r'rm -f /root/.ssh/known_hosts')

cmd=[]

#command='sudo stcli cluster create --name hx-demo --ip 192.168.0.100 --mgmt-ip 198.18.134.200 --node-ips 198.18.134.201 198.18.134.202 198.18.134.203 198.18.134.204  --vcenter-datacenter dCloud-HX-DC --vcenter-cluster dCloud-HX-Cluster --vcenter-url https://198.18.133.30 --vcenter-user administrator@vsphere.local --vcenter-password C1sco12345! --data-replication-factor 2'
command='sudo stcli cluster create --name hx-storage-cluster --ip 192.168.0.100 --mgmt-ip 198.18.134.200 --node-ips 198.18.134.201 198.18.134.202 198.18.134.203 --vcenter-datacenter dCloud-HX-DC --vcenter-cluster dCloud-HX-Cluster --vcenter-url https://198.18.133.30 --vcenter-user administrator@vsphere.local --vcenter-password C1sco12345! --data-replication-factor 2'

cases=[pexpect.TIMEOUT,pexpect.EOF,"[sudo].*"]
next=['timeout','eof',1]
timeout=15
cmd.append({'order':0,'cmd':command,'cases':cases,'next':next,'timeout':timeout})

command='Cisco123'
cases=[pexpect.TIMEOUT,pexpect.EOF,"Enter Controller's Root Password.*"]
next=['timeout','eof',2]
timeout=20
cmd.append({'order':1,'cmd':command,'cases':cases,'next':next,'timeout':timeout})


command='Cisco123'
cases=[pexpect.TIMEOUT,pexpect.EOF,"Do you accept this EULA.*"]
next=['timeout','eof',3]
timeout=20
cmd.append({'order':2,'cmd':command,'cases':cases,'next':next,'timeout':timeout})

command='Y'
cases=[pexpect.TIMEOUT,pexpect.EOF,"admin@HX-CTL-.*"]
next=['timeout','eof','end']
timeout=900
cmd.append({'order':3,'cmd':command,'cases':cases,'next':next,'timeout':timeout})


nodes=[]

nodeIP='198.18.134.205'
nodeUsername='admin'
nodePassword='Cisco123'
nodeLoginPrompt='HX-CTL-01'
nodes.append({'nodeIP':nodeIP, 'nodeUsername':nodeUsername, 'nodePassword':nodePassword, 'nodeLoginPrompt':nodeLoginPrompt})


for node in nodes:
    p.pexpectExecute(username=node['nodeUsername'], password=node['nodePassword'], loginPrompt=node['nodeLoginPrompt'],ipAddress=node['nodeIP'],cmd=cmd)
    time.sleep(30)






