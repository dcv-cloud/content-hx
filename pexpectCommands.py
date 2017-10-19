import os
import time
import logging
import inspect

#os.system("wget http://pexpect.sourceforge.net/pexpect-2.3.tar.gz")
#os.system("tar xzf pexpect-2.3.tar.gz")
#os.chdir("/root/pexpect-2.3")
#os.system("python ./setup.py install")



import pexpect

def isArgEmpty(frame):
    logging.debug('Checking arguments for function ' + inspect.getframeinfo(frame)[2])
    args, _,_, values = inspect.getargvalues(frame)
    empty=False
    for arg in args:
        if values[arg]=='':
            empty=True
            logging.debug('Argument ' + arg + ' is empty')
    return empty

def pexpectLogin(ipAddress='', username='', password='', prompt=''):

    if(isArgEmpty(inspect.currentframe())):
        logging.info('At least one argument is empty for pexpectLogin. Aborting pexpectLogin')
        return False

    logging.info('About to start SSH session to ' + ipAddress)
    try:
        child=pexpect.spawn('ssh ' + username + '@' + ipAddress)
        i=child.expect(["The authenticity.*","Password:.*","password:"])
        if i==0:
            logging.info('Got security Banner, will send a YESS' )
            child.sendline('yes')
            child.expect(["password:.*","Password:.*"])
            logging.info('Got asked for password, will send it')
            child.sendline(password)
        if i==1:
            logging.info('Got asked for Password, will send it')
            child.sendline(password)
        if i==2:
            logging.info('Got asked for password, will send it')
            child.sendline(password)


        logging.info('Expecting for prompt')
        child.expect(prompt+".*")

    except Exception as e:
        logging.info('Failed to login')
        logging.info(e)
        return False
    return child


def pexpectScp(ipAddress='', username='', password='', prompt='', scope=' ', source='', dest=''):

    logging.info('About to start SCP')
    if(isArgEmpty(inspect.currentframe())):
        logging.info('At least one argument is empty for pexpectScp. Aborting pexpectScp')
        return False

    scpCmd='scp ' + scope + ' ' + source + ' ' + username + '@' + ipAddress + ':' + dest
    logging.info('About to start SCP session to ' + ipAddress)
    logging.info('SCP command is: ' + scpCmd)
    try:
        child=pexpect.spawn(scpCmd )
        i=child.expect(["The authenticity.*","Password:.*","password:","Are you sure you want to continue connecting.*"])
        if i==0:
            logging.info('Got security Banner, will send a YESS' )
            child.sendline('yes')
            child.expect(["password:.*","Password:.*"])
            logging.info('Got asked for password, will send it')
            child.sendline(password)
        if i==1:
            logging.info('Got asked for Password, will send it')
            child.sendline(password)
        if i==2:
            logging.info('Got asked for password, will send it')
            child.sendline(password)
        if i==3:
            logging.info('Got the Are You Sure Question...., will send a YES' )
            child.sendline('yes')
            child.expect(["password:.*","Password:.*"])
            logging.info('Got asked for password, will send it')
            child.sendline(password)


        logging.info('Expecting for prompt')
        i=child.expect([pexpect.TIMEOUT,pexpect.EOF,prompt+".*"])
        if i==0:
            logging.info('Got Timeout' )
        if i==1:
            logging.info('Got EOF')
        if i==2:
            logging.info('Got prompt')
        str(child.before)

    except Exception as e:
        logging.info('Failed while SCP')
        logging.info(e)
        return False
    return True


    

def pexepectCommand(command, child):
    now=command['cmd']
    cases=command['cases']
    next=command['next']
    timeout=command['timeout']


    try:
        logging.info('Will send command: ' + now)
        child.sendline(now)
        logging.info('Expecting for ' + str(cases))
        i=child.expect(cases,timeout=timeout)
        logging.info('Got case ' + str(cases[i]))
        logging.info('Next cmd is ' + str(next[i]))
        logging.info(str(child.before))

    except Exception as e:
        logging.info('Error while attempting to execute ' + now)
        logging.info(e)
        return -1
    return next[i]


def pexpectExecute(username='',password='',loginPrompt='',ipAddress='',cmd=''):

    if(isArgEmpty(inspect.currentframe())):
        logging.info('At least one argument is empty. Aborting pexpectExecute')
        return False

    logging.info('##############    pexpectExecute on node: ' + ipAddress + ' #############' )

    child=pexpectLogin(username=username,password=password,ipAddress=ipAddress, prompt=loginPrompt)
    next=0
    if child:
        while next not in ['timeout', 'eof','end','fail']:
            logging.info('In 2 seconds we will execute cmd: ' + str(cmd[next]['cmd']))
            time.sleep(2)
            next=pexepectCommand(cmd[next], child)
            if next==-1:
                break
            logging.info('Next comand index is: ' + str(next))
        logging.info(str(child.before))
        print (str(child.before))
        logging.info('Last command exited with ' + str(next))
        if str(next) not in ['end']:
            return False
        else:
            return True

        

