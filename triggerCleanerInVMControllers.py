import os
import time
import logging
import inspect
import time

import pexpect
import pexpectCommands as p
import filecmp

logging.basicConfig(filename=r'/root/logs/triggerCleanerInVMControllers.log',level=logging.DEBUG,format='%(asctime)s %(message)s')



#install Pip
os.system(r' /bin/python2.7 /root/scripts/get-pip.py')
#install PYVMOMI
os.system(r' /bin/pip2.7 install pyvmomi')
#Modify SSL library to never verify SSL Certificate (Yes, a very bad thing to do)
os.system(r"sed -i 's/self.cert_verify(conn, request.url, verify, cert)/self.cert_verify(conn, request.url, False, cert)/g'  /usr/lib/python2.7/site-packages/requests-2.9.1-py2.7.egg/requests/adapters.py")








#Remove the saved public keys
os.system(r'rm -f /root/.ssh/known_hosts')

cmd=[]
command='sudo chmod 777 /home/admin/storfstool ; sudo mv /home/admin/storfstool /bin/ ; sudo /bin/storfstool -- -f start'
cases=[pexpect.TIMEOUT,pexpect.EOF,"[sudo].*"]
next=['timeout','eof',1]
timeout=120
cmd.append({'order':0,'cmd':command,'cases':cases,'next':next,'timeout':timeout})

command='Cisco123'
cases=[pexpect.TIMEOUT,pexpect.EOF,"admin@HX-CTL-.*"]
next=['timeout','eof','end']
timeout=120
cmd.append({'order':1,'cmd':command,'cases':cases,'next':next,'timeout':timeout})



nodes=[]
nodeUsername='admin'
nodePassword='Cisco123'
prompt='root@rhel7-tools'
sourcePath=r'/root/scripts/storfstool'
destPath='/home/admin/'
nodeLoginPrompt="admin@HX-CTL-0"


nodeIP='198.18.134.205'
nodes.append({'nodeIP':nodeIP, 'nodeUsername':nodeUsername, 'prompt': prompt, 'nodePassword':nodePassword, 'nodeLoginPrompt':nodeLoginPrompt, 'source' : sourcePath, 'dest': destPath})
nodeIP='198.18.134.206'
nodes.append({'nodeIP':nodeIP, 'nodeUsername':nodeUsername, 'prompt': prompt, 'nodePassword':nodePassword, 'nodeLoginPrompt':nodeLoginPrompt, 'source' : sourcePath, 'dest': destPath})
nodeIP='198.18.134.207'
nodes.append({'nodeIP':nodeIP, 'nodeUsername':nodeUsername, 'prompt': prompt, 'nodePassword':nodePassword, 'nodeLoginPrompt':nodeLoginPrompt, 'source' : sourcePath, 'dest': destPath})
nodeIP='198.18.134.208'
nodes.append({'nodeIP':nodeIP, 'nodeUsername':nodeUsername, 'prompt': prompt, 'nodePassword':nodePassword, 'nodeLoginPrompt':nodeLoginPrompt, 'source' : sourcePath, 'dest': destPath})


for node in nodes:
    try:
        logging.info('About to copy storfstool file to VM controller ' + node['nodeIP'] )
        p.pexpectScp(username=node['nodeUsername'], password=node['nodePassword'], prompt=node['prompt'],ipAddress=node['nodeIP'],source=node['source'], dest=node['dest'])
    except Exception as e:
        logging.info('Got error while trying copy storfstool file to VM controller ' + node['nodeIP'] )
        logging.info(e)


while (True):
    logging.info('About to get latest list of vms and put it in /root/scripts/latest_vmlist.txt')
    os.system(r'cd /root/scripts/pyvmomi-community-samples/samples/ && /bin/python2.7 getallvms.py --host 198.18.133.30 -u administrator@vsphere.local --password C1sco12345! > /root/scripts/latest_vmlist.txt')

    logging.info('reading files containing list of VMs')
    compare=True
    try:
        f_new = open('/root/scripts/latest_vmlist.txt', 'r')
        #logging.info("new list")
        #logging.info(f_new.read())
    except Exception as e:
        logging.info("Problem reading latest_vmlist.txt. Maybe it hasnt been created yet")
        logging.info(str(e))
        compare=False
        
    try:
        f_old = open('/root/scripts/old_vmlist.txt','r')
        #logging.info("old list")
        #logging.info(f_old.read())
    except Exception as e:
        logging.info("Problem reading old_vmlist.txt.")
        logging.info(str(e))
        if str(e)=="[Errno 2] No such file or directory: '/root/scripts/old_vmlist.txt'":
            logging.info("File old_vmlist.txt could not be found, let's create it.")
            if compare:
                os.system(r'cp -f /root/scripts/latest_vmlist.txt /root/scripts/old_vmlist.txt')
                try:
                    f_old = open('/root/scripts/old_vmlist.txt','r')
                    #logging.info("old list")
                    #logging.info(f_old.read())
                except Exception as e:
                    logging.info("Problem reading old_vmlist.txt ON SECOND TRY!! ")
                    logging.info(str(e))
                    compare=False
        
            else:
                logging.info("Could not create old_vmlist. Failed to read latest_vmlist")
                compare=False
                          
    if compare:  #Both files were succesfully read
        logging.info('About to compare files. If not the same to the previous list, new VMs are detected')
        if not (filecmp.cmp('/root/scripts/old_vmlist.txt','/root/scripts/latest_vmlist.txt')):
            logging.info('New VMs detected')
            logging.info('Updating new list of vms')
            logging.info('waiting 60 seconds before executing cleaning...')
            time.sleep(60)
            os.system(r'cp -f /root/scripts/latest_vmlist.txt /root/scripts/old_vmlist.txt')
            for node in nodes:        
                try:
                    logging.info('About to execute command in VM Controller  ' + node['nodeIP'] )
                    p.pexpectExecute(username=node['nodeUsername'], password=node['nodePassword'], loginPrompt=node['nodeLoginPrompt'],ipAddress=node['nodeIP'],cmd=cmd)
                except Exception as e:
                    logging.info('Got error while trying to execute command in VM Controller ' + node['nodeIP'] )
                    logging.info(e)
            logging.info('waiting 120 seconds delay...')
            time.sleep(120)
        else:
            logging.info('No new vms detected...')
    logging.info('waiting 60 seconds...')
    time.sleep(60)




