import os
import time
import logging
import inspect
import time

import pexpect
import pexpectCommands as p

logging.basicConfig(filename=r'/root/logs/editValidationInHX.log',level=logging.DEBUG,format='%(asctime)s %(message)s')



#'sed -i "s/return is_cluster_node_type_mismatch/return False #is_cluster_node_type_mismatch/g"  /usr/share/springpath/storfs-misc/validation/springpath_lib_validate_cluster_node_model.py'





#Remove the saved public keys
os.system(r'rm -f /root/.ssh/known_hosts')

cmd=[]
command='sed -i "s/stctlvm.resources.vcpu.min=8/stctlvm.resources.vcpu.min=0/g"  /usr/share/springpath/storfs-misc/validation/springpath-hcl.conf'
cases=[pexpect.TIMEOUT,pexpect.EOF,"root.*"]
next=['timeout','eof',1]
timeout=15
cmd.append({'order':0,'cmd':command,'cases':cases,'next':next,'timeout':timeout})


command='sed -i "s/stctlvm.resources.memory.min=49152/stctlvm.resources.memory.min=0/g"  /usr/share/springpath/storfs-misc/validation/springpath-hcl.conf'
cases=[pexpect.TIMEOUT,pexpect.EOF,"root.*"]
next=['timeout','eof',2]
timeout=15
cmd.append({'order':1,'cmd':command,'cases':cases,'next':next,'timeout':timeout})


command='sed -i "s/stctlvm.resources.vcpu.min=8/stctlvm.resources.vcpu.min=0/g"  /usr/share/springpath/storfs-appliance/springpath-hcl.conf'
cases=[pexpect.TIMEOUT,pexpect.EOF,"root.*"]
next=['timeout','eof',3]
timeout=15
cmd.append({'order':2,'cmd':command,'cases':cases,'next':next,'timeout':timeout})


command='sed -i "s/stctlvm.resources.memory.min=49152/stctlvm.resources.memory.min=0/g" /usr/share/springpath/storfs-appliance/springpath-hcl.conf'
cases=[pexpect.TIMEOUT,pexpect.EOF,"root.*"]
next=['timeout','eof',4]
timeout=15
cmd.append({'order':3,'cmd':command,'cases':cases,'next':next,'timeout':timeout})


command='sed -i "s/stctlvm.resources.vcpu.min=8/stctlvm.resources.vcpu.min=0/g"  /usr/share/springpath/storfs-fw/springpath-hcl.conf'
cases=[pexpect.TIMEOUT,pexpect.EOF,"root.*"]
next=['timeout','eof',5]
timeout=15
cmd.append({'order':4,'cmd':command,'cases':cases,'next':next,'timeout':timeout})


command='sed -i "s/stctlvm.resources.memory.min=49152/stctlvm.resources.memory.min=0/g" /usr/share/springpath/storfs-fw/springpath-hcl.conf'
cases=[pexpect.TIMEOUT,pexpect.EOF,"root.*"]
next=['timeout','eof','end']
timeout=15
cmd.append({'order':5,'cmd':command,'cases':cases,'next':next,'timeout':timeout})








nodes=[]

#nodeIP='198.18.134.208'
nodeUsername='root'
nodePassword='Cisco123'
nodeLoginPrompt='root@'
#nodes.append({'nodeIP':nodeIP, 'nodeUsername':nodeUsername, 'nodePassword':nodePassword, 'nodeLoginPrompt':nodeLoginPrompt})
#nodeIP='198.18.134.206'
#nodes.append({'nodeIP':nodeIP, 'nodeUsername':nodeUsername, 'nodePassword':nodePassword, 'nodeLoginPrompt':nodeLoginPrompt})
#nodeIP='198.18.134.207'
#nodes.append({'nodeIP':nodeIP, 'nodeUsername':nodeUsername, 'nodePassword':nodePassword, 'nodeLoginPrompt':nodeLoginPrompt})
#nodeIP='198.18.134.208'
#nodes.append({'nodeIP':nodeIP, 'nodeUsername':nodeUsername, 'nodePassword':nodePassword, 'nodeLoginPrompt':nodeLoginPrompt})

nodeIP='198.18.135.205'
nodes.append({'nodeIP':nodeIP, 'nodeUsername':nodeUsername, 'nodePassword':nodePassword, 'nodeLoginPrompt':nodeLoginPrompt})
nodeIP='198.18.135.206'
nodes.append({'nodeIP':nodeIP, 'nodeUsername':nodeUsername, 'nodePassword':nodePassword, 'nodeLoginPrompt':nodeLoginPrompt})
nodeIP='198.18.135.207'
nodes.append({'nodeIP':nodeIP, 'nodeUsername':nodeUsername, 'nodePassword':nodePassword, 'nodeLoginPrompt':nodeLoginPrompt})
nodeIP='198.18.135.208'
nodes.append({'nodeIP':nodeIP, 'nodeUsername':nodeUsername, 'nodePassword':nodePassword, 'nodeLoginPrompt':nodeLoginPrompt})


#nodeIP='198.18.136.205'
#nodes.append({'nodeIP':nodeIP, 'nodeUsername':nodeUsername, 'nodePassword':nodePassword, 'nodeLoginPrompt':nodeLoginPrompt})
#nodeIP='198.18.136.206'
#nodes.append({'nodeIP':nodeIP, 'nodeUsername':nodeUsername, 'nodePassword':nodePassword, 'nodeLoginPrompt':nodeLoginPrompt})
#nodeIP='198.18.136.207'
#nodes.append({'nodeIP':nodeIP, 'nodeUsername':nodeUsername, 'nodePassword':nodePassword, 'nodeLoginPrompt':nodeLoginPrompt})
#nodeIP='198.18.136.208'
#nodes.append({'nodeIP':nodeIP, 'nodeUsername':nodeUsername, 'nodePassword':nodePassword, 'nodeLoginPrompt':nodeLoginPrompt})



for node in nodes:
    try:
        logging.info('About to edit validation configuration  @ HX Controller ' + node['nodeIP'] )
        p.pexpectExecute(username=node['nodeUsername'], password=node['nodePassword'], loginPrompt=node['nodeLoginPrompt'],ipAddress=node['nodeIP'],cmd=cmd)
        #time.sleep(30)
    except Exception as e:
        logging.info('Got error while trying to edit validation configuration @  HX Controller ' + node['nodeIP'] )
        logging.info(str(e))
