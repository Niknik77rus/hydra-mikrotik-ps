from mt_hydra_controller import MtHydra, MtCheckParams
import sys


class MtHydraLogic:
    def __init__(self, apiclient, clientip):
        self.mt = MtHydra(apiclient, clientip)

    def mt_create(self, ul, dl, ip_list):
        try:

            if len(self.mt.get_ipclient_list()) == 0:
                self.mt.add_ipclient_list(ip_list)
            else:
                self.mt.mtlog.log_entry('Fail! cannot create new client - IP/CIDR {} already exist'.format(self.mt.clientip))
                sys.stderr.write('Fail! could not create new client - IP/CIDR {} already exist \n'.format(self.mt.clientip))
                sys.exit(1)
            if len(self.mt.get_queue()) == 0:
                self.mt.add_queue(ul, dl)
            else:
                self.mt.mtlog.log_entry('Fail! cannot create new client - QUEUE for {} already exist'.format(self.mt.clientip))
                sys.stderr.write('Fail! cannot create new client - QUEUE for {} already exist \n'.format(self.mt.clientip))
                sys.exit(1)
        except:
            self.mt.mtlog.log_entry('Fail! cannot create new client with IP/CIDR {}'.format(self.mt.clientip))
            sys.stderr.write('Fail! cannot create new client with IP/CIDR {} \n'.format(self.mt.clientip))
            sys.exit(1)
        else:
            self.mt.mtlog.log_entry('Success. New client was created with IP/CIDR {} and UL {} DL {}'.format(self.mt.clientip, ul, dl))
            print('Success. New client was created with IP/CIDR {} and UL {} DL {}'.format(self.mt.clientip, ul, dl))

    def mt_remove(self):
        try:
            self.mt.rmv_ipclient_list()
            self.mt.rmv_queue()
        except:
            self.mt.mtlog.log_entry('Fail! cannot remove client with IP/CIDR {}'.format(self.mt.clientip))
            sys.stderr.write('Fail! cannot remove client with IP/CIDR {} \n'.format(self.mt.clientip))
            sys.exit(1)
        else:
            self.mt.mtlog.log_entry('Success. Client {} was removed successfully'.format(self.mt.clientip))
            print('Success. Client {} was removed successfully'.format(self.mt.clientip))

    def mt_modify_queue(self, ul, dl):
        try:
            self.mt.mod_queue(ul, dl)
        except:
            self.mt.mtlog.log_entry('Fail! cannot modify QUEUE for IP/CIDR {}'.format(self.mt.clientip))
            sys.stderr.write('Fail! cannot modify QUEUE for IP/CIDR {} \n'.format(self.mt.clientip))
            sys.exit(1)
        else:
            self.mt.mtlog.log_entry('Success. QUEUE for client {} was  modified: UL {} DL {}'.format(self.mt.clientip, ul, dl))
            print('Success. QUEUE for client {} was  modified: UL {} DL {}'.format(self.mt.clientip, ul, dl))

    def mt_modify_iplist(self, ip_list):
        try:
            self.mt.mod_ipclient_list(ip_list)
        except:
            self.mt.mtlog.log_entry('Fail! cannot modify IP LIST for IP/CIDR {}'.format(self.mt.clientip))
            sys.stderr.write('Fail! cannot modify IP LIST for IP/CIDR {} \n'.format(self.mt.clientip))
            sys.exit(1)
        else:
            self.mt.mtlog.log_entry('Success. New IP-LIST for client {} - {}'.format(self.mt.clientip, ip_list))
            print('Success. New IP-LIST for client {} - {}'.format(self.mt.clientip, ip_list))