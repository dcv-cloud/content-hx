import os
import time
import logging
import inspect
import time



import pexpect
import pexpectCommands as p

logging.basicConfig(filename=r'/root/logs/enableCleanerInHX.log',level=logging.DEBUG,format='%(asctime)s %(message)s')


cmd=[]

command='sudo stcli cleaner start'
cases=[pexpect.TIMEOUT,pexpect.EOF,"[sudo].*"]
next=['timeout','eof',1]
timeout=15
cmd.append({'order':0,'cmd':command,'cases':cases,'next':next,'timeout':timeout})

command='Cisco123'
cases=[pexpect.TIMEOUT,pexpect.EOF,"admin@HX-CTL-.*"]
next=['timeout','eof','end']
timeout=120
cmd.append({'order':1,'cmd':command,'cases':cases,'next':next,'timeout':timeout})

nodes=[]

nodeIP='198.18.134.201'
nodeUsername='admin'
nodePassword='Cisco123'
nodeLoginPrompt='HX-CTL-0'
nodes.append({'nodeIP':nodeIP, 'nodeUsername':nodeUsername, 'nodePassword':nodePassword, 'nodeLoginPrompt':nodeLoginPrompt})

nodeIP='198.18.134.202'
nodeUsername='admin'
nodePassword='Cisco123'
nodeLoginPrompt='HX-CTL-0'
nodes.append({'nodeIP':nodeIP, 'nodeUsername':nodeUsername, 'nodePassword':nodePassword, 'nodeLoginPrompt':nodeLoginPrompt})

nodeIP='198.18.134.203'
nodeUsername='admin'
nodePassword='Cisco123'
nodeLoginPrompt='HX-CTL-0'
nodes.append({'nodeIP':nodeIP, 'nodeUsername':nodeUsername, 'nodePassword':nodePassword, 'nodeLoginPrompt':nodeLoginPrompt})

nodeIP='198.18.134.204'
nodeUsername='admin'
nodePassword='Cisco123'
nodeLoginPrompt='HX-CTL-0'
nodes.append({'nodeIP':nodeIP, 'nodeUsername':nodeUsername, 'nodePassword':nodePassword, 'nodeLoginPrompt':nodeLoginPrompt})





while(1):
    for node in nodes:
        try:
            logging.info('Cleaning Public keys...')
            #Remove the saved public keys
            os.system(r'rm -f /root/.ssh/known_hosts')
            logging.info('About to enable Cleaner --if Cluster and DS exists--- ' + node['nodeIP'])
            p.pexpectExecute(username=node['nodeUsername'], password=node['nodePassword'], loginPrompt=node['nodeLoginPrompt'],ipAddress=node['nodeIP'],cmd=cmd)
            #time.sleep(30)
        except Exception as e:
            logging.info('Got error while trying to Enable Cleaner in HX node. Ignoring... ' + node['nodeIP'] )
    time.sleep(60)



