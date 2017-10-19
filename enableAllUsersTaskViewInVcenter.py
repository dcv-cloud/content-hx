import os
import time
import logging
import inspect
import time



import pexpect
import pexpectCommands as p

logging.basicConfig(filename=r'/root/logs/enableAllTaskViewInVcenter.log',level=logging.DEBUG,format='%(asctime)s %(message)s')


#Remove the saved public keys
os.system(r'rm -f /root/.ssh/known_hosts')

cmd=[]

command='shell.set --enabled True'
cases=[pexpect.TIMEOUT,pexpect.EOF,"Command>.*"]
next=['timeout','eof',1]
timeout=15
cmd.append({'order':0,'cmd':command,'cases':cases,'next':next,'timeout':timeout})

command='shell'
cases=[pexpect.TIMEOUT,pexpect.EOF,"vc1:~.*","Command>.*"]
next=['timeout','eof',2,'fail']
timeout=15
cmd.append({'order':1,'cmd':command,'cases':cases,'next':next,'timeout':timeout})


command="sed -i s'/show.allusers.tasks = false/show.allusers.tasks = true/g' /etc/vmware/vsphere-client/webclient.properties"
cases=[pexpect.TIMEOUT,pexpect.EOF,"vc1:~.*"]
next=['timeout','eof',3]
timeout=15
cmd.append({'order':2,'cmd':command,'cases':cases,'next':next,'timeout':timeout})

command='service vsphere-client restart'
cases=[pexpect.TIMEOUT,pexpect.EOF,"vc1:~.*"]
next=['timeout','eof','end']
timeout=900
cmd.append({'order':3,'cmd':command,'cases':cases,'next':next,'timeout':timeout})


nodes=[]

nodeIP='198.18.133.30'
nodeUsername='root'
nodePassword='C1sco12345!'
nodeLoginPrompt='Command>'
nodes.append({'nodeIP':nodeIP, 'nodeUsername':nodeUsername, 'nodePassword':nodePassword, 'nodeLoginPrompt':nodeLoginPrompt})


#Let's wait 60 seconds
#time.sleep(60)

executed=False

while not executed: 
    for node in nodes:
        logging.info('Now going to execute the set commands on node ' + node['nodeIP'])
        executed=p.pexpectExecute(username=node['nodeUsername'], password=node['nodePassword'], loginPrompt=node['nodeLoginPrompt'],ipAddress=node['nodeIP'],cmd=cmd)
        logging.info('The excution of the set of commands on node ' + node['nodeIP'] + ' returned with ' + str(executed) )
        time.sleep(30)






