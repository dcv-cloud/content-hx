import os
import time
import logging
import inspect
import time

import pexpect
import pexpectCommands as p

logging.basicConfig(filename=r'/root/logs/stopDriveMonitorInHX.log',level=logging.DEBUG,format='%(asctime)s %(message)s')

#Remove the saved public keys
os.system(r'rm -f /root/.ssh/known_hosts')

cmd=[]
command='stop drive-monitor'
cases=[pexpect.TIMEOUT,pexpect.EOF,"root.*"]
next=['timeout','eof''end']
timeout=15
cmd.append({'order':0,'cmd':command,'cases':cases,'next':next,'timeout':timeout})






nodes=[]

nodeIP='198.18.134.205'
nodeUsername='root'
nodePassword='C1sco12345'
nodeLoginPrompt='root@'
nodes.append({'nodeIP':nodeIP, 'nodeUsername':nodeUsername, 'nodePassword':nodePassword, 'nodeLoginPrompt':nodeLoginPrompt})
nodeIP='198.18.134.206'
nodes.append({'nodeIP':nodeIP, 'nodeUsername':nodeUsername, 'nodePassword':nodePassword, 'nodeLoginPrompt':nodeLoginPrompt})
nodeIP='198.18.134.207'
nodes.append({'nodeIP':nodeIP, 'nodeUsername':nodeUsername, 'nodePassword':nodePassword, 'nodeLoginPrompt':nodeLoginPrompt})
nodeIP='198.18.134.208'
nodes.append({'nodeIP':nodeIP, 'nodeUsername':nodeUsername, 'nodePassword':nodePassword, 'nodeLoginPrompt':nodeLoginPrompt})

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


while(True):
    for node in nodes:
        try:
            logging.info('About to stop drive monitor @ HX Controller ' + node['nodeIP'] )
            p.pexpectExecute(username=node['nodeUsername'], password=node['nodePassword'], loginPrompt=node['nodeLoginPrompt'],ipAddress=node['nodeIP'],cmd=cmd)
            #time.sleep(30)
        except Exception as e:
            logging.info('Got error while trying to stop drive @  HX Controller ' + node['nodeIP'] )
            logging.info(str(e))
    time.sleep(30)
