import os
import time
import logging
import inspect
import time

import pexpect
import pexpectCommands as p

logging.basicConfig(filename=r'/root/logs/runPingallInHosts.log',level=logging.DEBUG,format='%(asctime)s %(message)s')

#Remove the saved public keys
os.system(r'rm -f /root/.ssh/known_hosts')

cmd=[]
command='chmod 777 /tmp/pingall.sh && nohup /tmp/pingall.sh & '
cases=[pexpect.TIMEOUT,pexpect.EOF,"root@HX-0"]
next=['timeout','eof','end']
timeout=120
cmd.append({'order':0,'cmd':command,'cases':cases,'next':next,'timeout':timeout})

nodes=[]
nodeUsername='root'
nodePassword='Cisco123'
prompt='root@rhel7-tools'
sourcePath=r'/root/scripts/pingall.sh'
destPath='/tmp/'
nodeLoginPrompt="root@HX-0"


nodeIP='198.18.134.201'
nodes.append({'nodeIP':nodeIP, 'nodeUsername':nodeUsername, 'prompt': prompt, 'nodePassword':nodePassword, 'nodeLoginPrompt':nodeLoginPrompt, 'source' : sourcePath, 'dest': destPath})
nodeIP='198.18.134.202'
nodes.append({'nodeIP':nodeIP, 'nodeUsername':nodeUsername, 'prompt': prompt, 'nodePassword':nodePassword, 'nodeLoginPrompt':nodeLoginPrompt, 'source' : sourcePath, 'dest': destPath})
nodeIP='198.18.134.203'
nodes.append({'nodeIP':nodeIP, 'nodeUsername':nodeUsername, 'prompt': prompt, 'nodePassword':nodePassword, 'nodeLoginPrompt':nodeLoginPrompt, 'source' : sourcePath, 'dest': destPath})
nodeIP='198.18.134.204'
nodes.append({'nodeIP':nodeIP, 'nodeUsername':nodeUsername, 'prompt': prompt, 'nodePassword':nodePassword, 'nodeLoginPrompt':nodeLoginPrompt, 'source' : sourcePath, 'dest': destPath})

for node in nodes:
    try:
        logging.info('About to copy pingall.sh to host ' + node['nodeIP'] )
        p.pexpectScp(username=node['nodeUsername'], password=node['nodePassword'], prompt=node['prompt'],ipAddress=node['nodeIP'],source=node['source'], dest=node['dest'])
    except Exception as e:
        logging.info('Got error while trying to copy pingall.sh to ' + node['nodeIP'] )
        logging.info(e)
        
    try:
        time.sleep(5)
        logging.info('About to execute pingall.sh script in host  ' + node['nodeIP'] )
        p.pexpectExecute(username=node['nodeUsername'], password=node['nodePassword'], loginPrompt=node['nodeLoginPrompt'],ipAddress=node['nodeIP'],cmd=cmd)
    except Exception as e:
        logging.info('Got error while trying executing pingall.sh in host ' + node['nodeIP'] )
        logging.info(e)

