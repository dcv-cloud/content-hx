#!/usr/bin/python
"""
Using the pyVmomi python bindings for vSphere connect to a VCSA and configure Datacenters and Clusters as per th spefified configuration file.
"""
import atexit
import yaml
import inspect
import time
import os
import subprocess
class Vcenter(object):
    def __init__(self, vcenter_params):
        self.pyVmomi =  __import__("pyVmomi")
        self.server = vcenter_params['ip']
        self.username = vcenter_params['user']
        self.password = vcenter_params['pw']
        self.connect_to_vcenter()
    def create_datacenter(self, dcname=None, folder=None):
        datacenter = self.get_obj([self.pyVmomi.vim.Datacenter], dcname)
        if datacenter is not None:
            print("datacenter %s already exists" % dcname)
            return datacenter
        else:
            if len(dcname) > 79:
                raise ValueError("The name of the datacenter must be under 80 characters.")
            if folder is None:
                folder = self.service_instance.content.rootFolder
            if folder is not None and isinstance(folder, self.pyVmomi.vim.Folder):
                print("Creating Datacenter %s " % dcname )
                dc_moref = folder.CreateDatacenter(name=dcname)
                return dc_moref
    def create_cluster(self, cluster_name, datacenter):
        cluster = self.get_obj([self.pyVmomi.vim.ClusterComputeResource], cluster_name)
        if cluster is not None:
            print("cluster already exists")
            return cluster
        else:
            if cluster_name is None:
                raise ValueError("Missing value for name.")
            if datacenter is None:
                raise ValueError("Missing value for datacenter.")
            print("Creating Cluster %s " % cluster_name )
            cluster_spec = self.pyVmomi.vim.cluster.ConfigSpecEx()
            host_folder = datacenter.hostFolder
            cluster = host_folder.CreateClusterEx(name=cluster_name, spec=cluster_spec)
            return cluster
    def add_host(self, cluster_name, hostname, sslthumbprint,  username, password):
        host = self.get_obj([self.pyVmomi.vim.HostSystem], hostname)
        if host is not None:
            print("host already exists")
            return host
        else:
            if hostname is None:
                raise ValueError("Missing value for name.")
            cluster = self.get_obj([self.pyVmomi.vim.ClusterComputeResource], cluster_name)
            if cluster is None:
                error = 'Error - Cluster %s not found. Unable to add host %s' % (cluster_name, hostname)
                raise ValueError(error)
            try:
                hostspec = self.pyVmomi.vim.host.ConnectSpec(hostName=hostname,userName=username, sslThumbprint=sslthumbprint, password=password, force=True)
                task=cluster.AddHost(spec=hostspec,asConnected=True)
            except self.pyVmomi.vmodl.MethodFault as error:
                print "Caught vmodl fault : " + error.msg
                return -1
            self.wait_for_task(task)
            host = self.get_obj([self.pyVmomi.vim.HostSystem], hostname)
            return host
    def get_obj(self, vimtype, name):
        """
        Get the vsphere object associated with a given text name
        """
        obj = None
        container = self.content.viewManager.CreateContainerView(self.content.rootFolder, vimtype, True)
        for c in container.view:
                if c.name == name:
                    obj = c
                    break
        return obj
    def wait_for_task(self, task):
        while task.info.state == (self.pyVmomi.vim.TaskInfo.State.running or self.pyVmomi.vim.TaskInfo.State.queued):
            time.sleep(2)
        if task.info.state == self.pyVmomi.vim.TaskInfo.State.success:
            if task.info.result is not None:
                out = 'Task completed successfully, result: %s' % (task.info.result,)
                print out
        elif task.info.state == self.pyVmomi.vim.TaskInfo.State.error:
            out = 'Error - Task did not complete successfully: %s' % (task.info.error,)
            raise ValueError(out)
        return task.info.result
    def connect_to_vcenter(self):
        from pyVim import connect
        print("Connecting to %s using username %s" % (self.server, self.username))
        self.service_instance = connect.SmartConnect(host=self.server,
                                                user=self.username,
                                                pwd=self.password,
                                                port=443)
                                                #protocol='http')
        self.content = self.service_instance.RetrieveContent()
        about = self.service_instance.content.about
        print("Connected to %s, %s" % (self.server, about.fullName))
        atexit.register(connect.Disconnect, self.service_instance)
    def getsslThumbprint(self,ip):
        p1 = subprocess.Popen(('echo', '-n'), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p2 = subprocess.Popen(('openssl', 's_client', '-connect', '{0}:443'.format(ip)), stdin=p1.stdout, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p3 = subprocess.Popen(('openssl', 'x509', '-noout', '-fingerprint', '-sha1'), stdin=p2.stdout, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out = p3.stdout.read()
        ssl_thumbprint = out.split('=')[-1].strip()
        return ssl_thumbprint
def main():
    config = yaml.load(open("/root/scripts/vcConfig.yaml"))
    vc=Vcenter(config["lab"]["vsphere"]["vcenter"]);
    dc=config["lab"]["vsphere"]["topology"]
    hostlist = config['lab']['vsphere']['host']
    # for each datacenter, get the name and optionally if there is a key for clusters then create matching clusters
    # in this datacenter, otherwise just create the datacenter.
    for i in dc:
       datacenter = vc.create_datacenter(dcname=i['dc']['name'])
       if i['dc'].has_key('clusters') :
          for j in i['dc']['clusters']:
             cluster=vc.create_cluster(j['name'],datacenter)
             if j.has_key('members') :
                for k in j['members']:
                   iptoadd=None
                   user=None
                   pw=None
                   for l in hostlist:             # lookup the member details in the hosts section in the YAML to find the
                      if l['ip']==k['ip']:        #
                         iptoadd=l['ip']          #
                         user=l['user']           # user and pasword details
                         pw=l['pw']
                   if iptoadd == None:
                       print("Couldnt find credentials for ip %s" % k['ip'])
                   else:
                       sslthumbprint=vc.getsslThumbprint(iptoadd)
                       vc.add_host(j['name'],iptoadd,sslthumbprint,user,pw)
    return 0
# Start program
if __name__ == "__main__":
    main()
    os.system(r' echo "Done" >> /root/logs/vc.status')
