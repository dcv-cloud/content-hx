import os
import time
import logging
import inspect
import time

import pexpect
import pexpectCommands as p

logging.basicConfig(filename=r'/root/logs/addServicesInHX.log',level=logging.DEBUG,format='%(asctime)s %(message)s')

#Remove the saved public keys
os.system(r'rm -f /root/.ssh/known_hosts')

cmd=[]

command='sudo stcli services ntp remove --ntp 172.16.0.20'
cases=[pexpect.TIMEOUT,pexpect.EOF,"[sudo].*"]
next=['timeout','eof',1]
timeout=15
cmd.append({'order':0,'cmd':command,'cases':cases,'next':next,'timeout':timeout})

command='Cisco123'
cases=[pexpect.TIMEOUT,pexpect.EOF,"admin@HX-CTL-.*"]
next=['timeout','eof',2]
timeout=120
cmd.append({'order':1,'cmd':command,'cases':cases,'next':next,'timeout':timeout})

command='sudo stcli services ntp add --ntp 198.18.128.1'
cases=[pexpect.TIMEOUT,pexpect.EOF,"admin@HX-CTL-.*"]
next=['timeout','eof',3]
timeout=120
cmd.append({'order':2,'cmd':command,'cases':cases,'next':next,'timeout':timeout})

command='sudo stcli services dns add --dns 198.18.133.1'
cases=[pexpect.TIMEOUT,pexpect.EOF,"admin@HX-CTL-.*"]
next=['timeout','eof',4]
timeout=120
cmd.append({'order':3,'cmd':command,'cases':cases,'next':next,'timeout':timeout})

command='sudo chmod 777 /opt/springpath/config/nested.tunes'
cases=[pexpect.TIMEOUT,pexpect.EOF,"admin@HX-CTL-.*"]
next=['timeout','eof',5]
timeout=120
cmd.append({'order':4,'cmd':command,'cases':cases,'next':next,'timeout':timeout})


command='sudo sed -i "s/crmZKSessionTimeout=45000//g" /opt/springpath/config/nested.tunes'
cases=[pexpect.TIMEOUT,pexpect.EOF,"admin@HX-CTL-.*"]
next=['timeout','eof',6]
timeout=120
cmd.append({'order':4,'cmd':command,'cases':cases,'next':next,'timeout':timeout})


command='sudo sed -i "/^$/d" /opt/springpath/config/nested.tunes'
cases=[pexpect.TIMEOUT,pexpect.EOF,"admin@HX-CTL-.*"]
next=['timeout','eof',7]
timeout=120
cmd.append({'order':6,'cmd':command,'cases':cases,'next':next,'timeout':timeout})


command='sudo echo "crmZKSessionTimeout=45000" >> /opt/springpath/config/nested.tunes '
cases=[pexpect.TIMEOUT,pexpect.EOF,"admin@HX-CTL-.*"]
next=['timeout','eof','end']
timeout=120
cmd.append({'order':7,'cmd':command,'cases':cases,'next':next,'timeout':timeout})


nodes=[]

nodeIP='198.18.134.205'
nodeUsername='admin'
nodePassword='Cisco123'
nodeLoginPrompt='HX-CTL-0'
nodes.append({'nodeIP':nodeIP, 'nodeUsername':nodeUsername, 'nodePassword':nodePassword, 'nodeLoginPrompt':nodeLoginPrompt})

nodeIP='198.18.134.206'
nodes.append({'nodeIP':nodeIP, 'nodeUsername':nodeUsername, 'nodePassword':nodePassword, 'nodeLoginPrompt':nodeLoginPrompt})
nodeIP='198.18.134.207'
nodes.append({'nodeIP':nodeIP, 'nodeUsername':nodeUsername, 'nodePassword':nodePassword, 'nodeLoginPrompt':nodeLoginPrompt})
nodeIP='198.18.134.208'
nodes.append({'nodeIP':nodeIP, 'nodeUsername':nodeUsername, 'nodePassword':nodePassword, 'nodeLoginPrompt':nodeLoginPrompt})

for node in nodes:
    try:
        logging.info('About to add services NTP/DNS to HX Controller ' + node['nodeIP'] )
        p.pexpectExecute(username=node['nodeUsername'], password=node['nodePassword'], loginPrompt=node['nodeLoginPrompt'],ipAddress=node['nodeIP'],cmd=cmd)
        #time.sleep(30)
    except Exception as e:
        logging.info('Got error while trying to add services NTP/DNS to HX Controller ' + node['nodeIP'] )
