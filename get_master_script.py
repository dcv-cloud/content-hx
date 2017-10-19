from ftplib import FTP
import os
import sys
import subprocess
import time

def get_master_script(directory='/',ftp_server='198.19.255.136',user='download',pwd='C1sco12345',filename='tools_master.py',script_path='/root/scripts/'):

    os.chdir(script_path) # Go to the desired folder, where the file is to be downloaded to
    ftp =FTP(ftp_server)  # Connect to dCloud internal FTP server
    ftp.login(user,pwd)   # login with user/pwd
    ftp.cwd(directory)    # Go to desired folder where to download from (on FTP server)
    try:
        ftp.retrbinary('RETR %s' % filename ,open(filename,'wb').write)   #Download
    except:
        print "Error"        
    ftp.quit()  #Close connection

if __name__ == "__main__":
    #The first argument is the source folder
    get_master_script(directory='/'+sys.argv[1]);

    #Prepare list for Popen argument. Script name part.
    script_name = ['nohup','python2.7','/root/scripts/tools_master.py']

    #Pass all the arguments to master.py
    #Prepare list for Popen.  Script arguments part.
    arguments=[]
    delay=False
    for arg in sys.argv[1:]:
        if arg !='delay':
            arguments.append(arg)
        else:
            delay=True

    #Gathering all the arguments for Popen on a single list
    Popen_args=script_name + arguments

    #Calling Popen, it will execute Master.py asynchronously. 
    p=subprocess.Popen(Popen_args)

    if delay:
        time.sleep(600)

    #exit
    quit()


