import sys
import logging
import mt_hydra_config
import ipaddress

class MtLogger:
    def __init__(self, clientip):
        self.clientip = clientip
        self.logger = logging.getLogger("mainLog")
        self.fh = logging.FileHandler(mt_hydra_config.log)
        self.formatter = logging.Formatter('%(asctime)-15s %(clientip)-15s' '%(message)s')
        self.fh.setFormatter(self.formatter)
        self.logger.addHandler(self.fh)
        self.logger.setLevel(logging.INFO)

    def log_entry(self, msg):
        addition = {"clientip": self.clientip}
        self.logger.info(msg, extra=addition)



class MtHydra:

    def __init__(self, apiclient, clientip):
        self.clientip = clientip
        self.mtlog = MtLogger(clientip)
        self.apiclient = apiclient

    def get_queue(self):
        try:
            res = self.apiclient.talk(["/queue/simple/print", "?target=" + self.clientip, "=.proplist=.id"])
        except:
            self.mtlog.log_entry('EXCEPTION could not get clients QUEUE for {}'.format(self.clientip))
            self.mtlog.log_entry('EXCEPTION - {}'.format(res))
            sys.exit(1)
        else:
            self.mtlog.log_entry('clients QUEUE position found at - {}'.format(res))
            return res

    def get_ipclient_list(self):
        if self.clientip[-3:] == '/32':
            clientip = self.clientip[:-3]
        try:
            res = self.apiclient.talk(["/ip/firewall/address-list/print", "?address=" + clientip, "=.proplist=.id"])
        except:
            self.mtlog.log_entry('EXCEPTION could not get clients IP list position for {}'.format(self.clientip))
            self.mtlog.log_entry('EXCEPTION - {}'.format(res))
            sys.exit(1)
        else:
            self.mtlog.log_entry('clients IP position found at - {}'.format(res))
            return res

    def add_queue(self, ul, dl):
        ul = str(ul) + 'K'
        dl = str(dl) + 'K'
        try:
            res = self.apiclient.talk(["/queue/simple/add",
                                       "=target=" + self.clientip, "=max-limit=" + ul + "/" + dl, "=.proplist=.id"])
        except:
            self.mtlog.log_entry('EXCEPTION could not add QUEUE for {}'.format(self.clientip))
            self.mtlog.log_entry('EXCEPTION - {}'.format(res))
            sys.exit(1)
        else:
            self.mtlog.log_entry('clients QUEUE was added at - {}'.format(res))
            return res

    def add_ipclient_list(self, list_name):
        try:
            res = self.apiclient.talk(["/ip/firewall/address-list/add", \
                                       "=address=" + self.clientip, "=list=" + list_name, "=.proplist=.id"])
        except:
            self.mtlog.log_entry('EXCEPTION could not add IP list entry for {}'.format(self.clientip))
            self.mtlog.log_entry('EXCEPTION - {}'.format(res))
            sys.exit(1)
        else:
            self.mtlog.log_entry('clients IP was added to list - {}'.format(list_name))
            return res

    def mod_queue(self, ul, dl):
        ul = str(ul) + 'K'
        dl = str(dl) + 'K'
        queue = self.get_queue()
        if len(queue) > 0:
            key = list(queue.keys())[0]
            queue_id = queue[key]['.id']
            try:
                res = self.apiclient.talk(["/queue/simple/set", "=max-limit=" + ul + "/" + dl, "=.id=" + queue_id, ])
            except:
                self.mtlog.log_entry('EXCEPTION could not modify QUEUE entry for {}'.format(self.clientip))
                self.mtlog.log_entry('EXCEPTION - {}'.format(res))
                sys.exit(1)
            else:
                self.mtlog.log_entry('clients new QUEUE params - UL {} DL {}'.format(ul, dl))
                return res
        else:
            self.mtlog.log_entry('EXCEPTION old QUEUE entry for {} was not found'.format(self.clientip))
            sys.exit(1)


    def mod_ipclient_list(self, list_name):
        ipclient_list = self.get_ipclient_list()
        if len(ipclient_list) > 0:
            key = list(ipclient_list.keys())[0]
            ipclient_list_id = ipclient_list[key]['.id']
            try:
                res = self.apiclient.talk(["/ip/firewall/address-list/set",
                                      "=list=" + list_name, "=.id=" + ipclient_list_id, ])
            except:
                self.mtlog.log_entry('EXCEPTION could not modify IP list entry for {}'.format(self.clientip))
                self.mtlog.log_entry('EXCEPTION - {}'.format(res))
                sys.exit(1)
            else:
                self.mtlog.log_entry('clients new IP list - {}'.format(list_name))
                return res
        else:
            self.mtlog.log_entry('EXCEPTION old IP list entry for {} was not found'.format(self.clientip))
            sys.exit(1)

    def rmv_queue(self):
        queue = self.get_queue()
        if len(queue) > 0:
            key = list(queue.keys())[0]
            queue_id = queue[key]['.id']
            try:
                res = self.apiclient.talk(["/queue/simple/remove", "=.id=" + queue_id, ])
            except:
                self.mtlog.log_entry('EXCEPTION could not remove QUEUE for {}'.format(self.clientip))
                self.mtlog.log_entry('EXCEPTION - {}'.format(res))
                sys.exit(1)
            else:
                self.mtlog.log_entry(' - QUEUE for {} was removed'.format(self.clientip))
                return res
        else:
            self.mtlog.log_entry(' - QUEUE for {} did not exist'.format(self.clientip))
            return queue

    def rmv_ipclient_list(self):
        ipclient_list = self.get_ipclient_list()
        if len(ipclient_list) > 0:
            key = list(ipclient_list.keys())[0]
            ipclient_list_id= ipclient_list[key]['.id']
            try:
                res = self.apiclient.talk(["/ip/firewall/address-list/remove", "=.id=" + ipclient_list_id, ])
            except:
                self.mtlog.log_entry('EXCEPTION could not remove IP list entry for {}'.format(self.clientip))
                self.mtlog.log_entry('EXCEPTION - {}'.format(res))
                sys.exit(1)
            else:
                self.mtlog.log_entry(' - IP list entry for {} was removed'.format(self.clientip))
                return res
        else:
            self.mtlog.log_entry(' - IP list entry for {} did not exist'.format(self.clientip))
            return ipclient_list


class MtCheckParams:
    def __init__(self, clientip, ul, dl, state, action):
        self.clientip = clientip
        self.ul = ul
        self.dl = dl
        self.state = state
        self.action = action
        self.mtlog = MtLogger(clientip)

    def check_rate(self, rate):
        try:
            int(rate)
        except:
            self.mtlog.log_entry('{} - wrong RATE format'.format(rate))
            sys.exit(1)
        else:
            return True

    def check_ip(self, clientip):
        try:
            ipaddress.ip_network(clientip)
        except:
            self.mtlog.log_entry('IP/CIDR {} is not valid'.format(clientip))
            sys.exit(1)
        else:
            return True

    def check_state(self, state):
        if state in mt_hydra_config.state_list:
            return True
        else:
            self.mtlog.log_entry('{} - no such STATE available'.format(state))

            sys.exit(1)

    def check_action(self, action):
        if action in mt_hydra_config.action_list:
            return True
        else:
            self.mtlog.log_entry('{} - no such ACTION available'.format(action))
            sys.exit(1)