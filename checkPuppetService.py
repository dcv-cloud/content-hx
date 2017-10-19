from xml.dom import minidom
import platform
import urllib2
import threading
import logging
import time
import sys
import os

logging.basicConfig(filename=r'/root/logs/checkPuppetService.log',level=logging.DEBUG,format='%(asctime)s %(message)s')

def loop():

    logging.info('Checking puppet status...')
    #os.system(r' echo "Checking puppetserver status" >> /root/logs/checkPuppetService.log ')
    os.system(r' systemctl is-active pe-puppetserver >> /root/logs/checkPuppetService.log && echo "pe-puppetservice is active" >> /root/logs/checkPuppetService.log')
    os.system(r' systemctl is-active pe-puppetserver >> /root/logs/checkPuppetService.log || (echo "pe-puppetservice failed. Restarting..." >> /root/logs/checkPuppetService.log &&  systemctl restart pe-puppetdb >> /root/logs/checkPuppetService.log && systemctl restart pe-puppetserver >> /root/logs/checkPuppetService.log)')
    os.system(r' systemctl is-active pe-puppetserver >> /root/logs/checkPuppetService.log || echo "pe-puppet failed to restart. Aborting"  >> /root/logs/checkPuppetService.log')

    threading.Timer(90,loop).start()
    logging.info('End of check loop...')

if __name__ == "__main__":
    logging.info('Starting checkPuppetService.py')
    loop()

    


    
    



