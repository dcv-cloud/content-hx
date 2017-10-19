import os
import time
import logging
import inspect
import time

import pexpect
import pexpectCommands as p

logging.basicConfig(filename=r'/root/logs/installDvfilterInHosts.log',level=logging.DEBUG,format='%(asctime)s %(message)s')

#Remove the saved public keys
os.system(r'rm -f /root/.ssh/known_hosts')

cmd=[]
command='esxcli software vib install -v /tmp/vmware-esx-dvfilter-maclearn-1.0.vib -f'
cases=[pexpect.TIMEOUT,pexpect.EOF,"root@HX-0"]
next=['timeout','eof','end']
timeout=120
cmd.append({'order':0,'cmd':command,'cases':cases,'next':next,'timeout':timeout})

nodes=[]
nodeUsername='root'
nodePassword='Cisco123'
prompt='root@rhel7-tools'
sourcePath=r'/root/scripts/vmware-esx-dvfilter-maclearn-1.0.vib'
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
        logging.info('About to copy vib file to host ' + node['nodeIP'] )
        p.pexpectScp(username=node['nodeUsername'], password=node['nodePassword'], prompt=node['prompt'],ipAddress=node['nodeIP'],source=node['source'], dest=node['dest'])
    except Exception as e:
        logging.info('Got error while trying to copy vib file to ' + node['nodeIP'] )
        logging.info(e)
        
    try:
        time.sleep(5)
        logging.info('About to Install VIB to host  ' + node['nodeIP'] )
        p.pexpectExecute(username=node['nodeUsername'], password=node['nodePassword'], loginPrompt=node['nodeLoginPrompt'],ipAddress=node['nodeIP'],cmd=cmd)
    except Exception as e:
        logging.info('Got error while trying to install vib to host ' + node['nodeIP'] )
        logging.info(e)
        

# This needs to be aplied on the Nested EXis itself, not the VMs in the nested hosts. 
#logging.info('Will add Tags to Controller VM in host 1')
#os.system(r' /bin/python2.7 /root/scripts/add_vm_extra_config_tags.py -s 198.18.133.30 -u administrator@vsphere.local -p C1sco12345! -j 564d57d5-2c46-4443-88e4-6a89ad3f330d ')
#logging.info('Will add Tags to Controller VM in host 2')
#os.system(r' /bin/python2.7 /root/scripts/add_vm_extra_config_tags.py -s 198.18.133.30 -u administrator@vsphere.local -p C1sco12345! -j 564dd9e2-26fa-7a10-5719-7efdddea75a5 ')
#logging.info('Will add Tags to Controller VM in host 3')
#os.system(r' /bin/python2.7 /root/scripts/add_vm_extra_config_tags.py -s 198.18.133.30 -u administrator@vsphere.local -p C1sco12345! -j 564d4b7f-9076-f7cf-9345-b9a7acf0d675 ')
#logging.info('Will add Tags to Controller VM in host 4')
#os.system(r' /bin/python2.7 /root/scripts/add_vm_extra_config_tags.py -s 198.18.133.30 -u administrator@vsphere.local -p C1sco12345! -j 564d2fad-b66e-951e-9bba-ff36ca5f9263 ')

