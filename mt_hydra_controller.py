import sys
import logging
import mt_hydra_config
import ipaddress

class MtLogger:
    def __init__(self, clientip):
        self.clientip = clientip
        self.logger = logging.getLogger("mainLog")
        if not len(self.logger.handlers):
            self.fh = logging.FileHandler(mt_hydra_config.log)
            self.formatter = logging.Formatter('%(asctime)s  %(clientip)s ' '%(message)s')
            self.fh.setFormatter(self.formatter)
            self.logger.addHandler(self.fh)
            self.logger.setLevel(logging.INFO)

    def log_entry(self, msg):
        addition = {"clientip": self.clientip}
        self.logger.info(msg, extra=addition)


class MtHydra:

    def __init__(self, apiclient, clientip):
        self.clientip = list(filter(None, clientip.split(',')))
        for i in range(len(self.clientip)):
            if '/' not in self.clientip[i]:
                self.clientip[i] = self.clientip[i] + '/32'
        self.mtlog = MtLogger(clientip)
        self.apiclient = apiclient

    def get_queue(self):
        target = ",".join(self.clientip)
        try:
            res = self.apiclient.talk(["/queue/simple/print", "?target=" + target, "=.proplist=.id,target,max-limit"])
        except:
            self.mtlog.log_entry('Warning! cannot get clients QUEUE for {}'.format(target))
            self.mtlog.log_entry('EXCEPTION - {}'.format(res))
            sys.stderr.write("Warning! cannot get clients queue\n")
            sys.exit(1)
        else:
            self.mtlog.log_entry('Info. Clients QUEUE was found with params - {}'.format(res))
            print('Info. Clients QUEUE was found with params  - {}'.format(res))
            return res

    def get_ipclient_list(self):
        res_list = []
        for ipaddr in self.clientip:

            if '/32' in ipaddr:
                ipaddr = ipaddr[:ipaddr.find("/")]
            try:
                res = self.apiclient.talk(["/ip/firewall/address-list/print", "?address=" + ipaddr, "=.proplist=.id,list"])
            except:
                self.mtlog.log_entry('Warning! cannot get clients IP list entry for {}'.format(ipaddr))
                self.mtlog.log_entry('EXCEPTION - {}'.format(res))
                sys.stderr.write('Warning! cannot get clients IP list entry\n')
                sys.exit(1)
            else:
                self.mtlog.log_entry('Info. clients IP was found with params - {}'.format(res))
                print('Info. clients IP was found with params  - {}'.format(res))
                res_list.append(res)
        print(res_list)
        return res_list

    def add_queue(self, ul, dl):
        if 'K' not in ul:
            ul = ul + 'K'
        if 'K' not in dl:
            dl = dl + 'K'
        target = ",".join(self.clientip)
        try:
            #240222019 nnk - add queue name prefix with 1 address of provided list
            res = self.apiclient.talk(["/queue/simple/add",
                                       "=target=" + target, "=name=hydra_auth_" + self.clientip[0],
                                       "=max-limit=" + ul + "/" + dl, "=.proplist=.id"])
        except:
            self.mtlog.log_entry('Fail! cannot add QUEUE for {}'.format(target))
            self.mtlog.log_entry('EXCEPTION - {}'.format(res))
            sys.stderr.write('Fail! cannot add QUEUE for {} \n'.format(target))
            sys.exit(1)
        else:
            self.mtlog.log_entry('Info. Clients QUEUE was added at - {}'.format(res))
            print('Info. Clients QUEUE was added at - {} \n'.format(res))
            return res

    def add_ipclient_list(self, list_name):
        res_list = []
        for ipaddr in self.clientip:
            try:
                res = self.apiclient.talk(["/ip/firewall/address-list/add", \
                                           "=address=" + ipaddr, "=list=" + list_name, "=.proplist=.id"])
            except:
                self.mtlog.log_entry('Fail! cannot add IP list entry for {}'.format(ipaddr))
                self.mtlog.log_entry('EXCEPTION - {}'.format(res))
                sys.stderr.write('Fail! cannot add IP list entry for {} \n'.format(ipaddr))
                sys.exit(1)
            else:
                self.mtlog.log_entry('Info. Clients IP was added to list - {}'.format(list_name))
                print('Info. Clients IP was added to list - {}'.format(list_name))
                res_list.append(res)
        return res_list

    def mod_queue(self, ul, dl):
        ul = ul + 'K'
        dl = dl + 'K'
        queue = self.get_queue()
        if len(queue) > 0:
            key = list(queue.keys())[0]
            queue_id = queue[key]['.id']
            try:
                res = self.apiclient.talk(["/queue/simple/set", "=max-limit=" + ul + "/" + dl, "=.id=" + queue_id, ])
            except:
                self.mtlog.log_entry('Fail! cannot modify QUEUE entry for {}'.format(self.clientip))
                self.mtlog.log_entry('EXCEPTION - {}'.format(res))
                sys.stderr.write('Fail! cannot modify QUEUE entry for {} \n'.format(self.clientip))
                sys.exit(1)
            else:
                self.mtlog.log_entry('Info. Clients new QUEUE params - UL {} DL {}'.format(ul, dl))
                print('Info. Clients new QUEUE params - UL {} DL {} \n'.format(ul, dl))
                return res
        elif len(queue) == 0 and len(self.get_ipclient_list()) > 0:
            print("Info. State changed. Adding new QUEUE for client\n")
            self.add_queue(ul, dl)
        else:
            self.mtlog.log_entry('Fail! QUEUE entry for {} was not found. Nothing to change'.format(self.clientip))
            sys.stderr.write('Fail! QUEUE entry for {} was not found. Nothing to change \n'.format(self.clientip))
            sys.exit(1)

    def mod_ipclient_list(self, list_name):
        res_list = []
        ipclient_list = self.get_ipclient_list()
        if len(ipclient_list) > 0:
            for ip_position in ipclient_list:
                key = list(ip_position.keys())[0]
                ipclient_list_id = ip_position[key]['.id']
                try:
                    res = self.apiclient.talk(["/ip/firewall/address-list/set",
                                          "=list=" + list_name, "=.id=" + ipclient_list_id, ])
                except:
                    self.mtlog.log_entry('Fail! cannot modify IP list entry for {}'.format(self.clientip))
                    self.mtlog.log_entry('EXCEPTION - {}'.format(res))
                    sys.stderr.write('Fail! cannot modify IP list entry for {} \n'.format(self.clientip))
                    sys.exit(1)
                else:
                    self.mtlog.log_entry('Info. Clients new IP list - {}'.format(list_name))
                    print('Info. Clients new IP list - {} '.format(list_name))
                    res_list.append(res)
        else:
            self.mtlog.log_entry('Fail! IP list entry for {} was not found'.format(self.clientip))
            sys.stderr.write('Fail! IP list entry for {} was not found \n'.format(self.clientip))
            sys.exit(1)
        return res_list

    def mod_queue_target(self, old_ip, ul, dl):
        new_target = ",".join(self.clientip)
        new_prefix = self.clientip[0]
        self.clientip = list(filter(None, old_ip.split(',')))
        for i in range(len(self.clientip)):
             if len(self.clientip[i]) > 1 and '/' not in self.clientip[i]:
                self.clientip[i] = str(self.clientip[i]) + '/32'
        queue = self.get_queue()
        if len(queue) > 0:
            key = list(queue.keys())[0]
            queue_id = queue[key]['.id']
            try:
                # 240222019 nnk - add queue name prefix with 1 address of provided list
                res = self.apiclient.talk(["/queue/simple/set", "=target=" + new_target,
                                           "=name=hydra_auth_" + new_prefix,"=.id=" + queue_id, ])
            except:
                self.mtlog.log_entry('Fail! cannot modify QUEUE TARGET for {}'.format(new_target))
                self.mtlog.log_entry('EXCEPTION - {}'.format(res))
                sys.stderr.write('Fail! cannot modify QUEUE TARGET for {} \n'.format(new_target))
                sys.exit(1)
            else:
                self.mtlog.log_entry('Info. Clients new QUEUE TARGET - {}'.format(new_target))
                print('Info. Clients new QUEUE TARGET - {} \n'.format(new_target))
                return res
        elif len(queue) == 0 and len(self.get_ipclient_list()[0]) > 0:
            print("Info. Adding new QUEUE for client")
            self.add_queue(ul, dl)
        else:
            self.mtlog.log_entry('Fail! QUEUE entry for {} was not found. Nothing to change'.format(self.clientip))
            sys.stderr.write('Fail! QUEUE entry for {} was not found. Nothing to change \n'.format(self.clientip))
            sys.exit(1)

    def rmv_queue(self):
        queue = self.get_queue()
        if len(queue) > 0:
            key = list(queue.keys())[0]
            queue_id = queue[key]['.id']
            try:
                res = self.apiclient.talk(["/queue/simple/remove", "=.id=" + queue_id, ])
            except:
                self.mtlog.log_entry('Fail! cannot remove QUEUE for {}'.format(self.clientip))
                self.mtlog.log_entry('EXCEPTION - {}'.format(res))
                sys.stderr.write('Fail! cannot remove QUEUE for {} '.format(self.clientip))
                sys.exit(1)
            else:
                self.mtlog.log_entry('Info. QUEUE for {} was removed'.format(self.clientip))
                print('Info. QUEUE for {} was removed'.format(self.clientip))
                return res
        else:
            self.mtlog.log_entry('Warning! QUEUE for {} did not exist'.format(self.clientip))
            print('Warning! QUEUE for {} did not exist '.format(self.clientip))
            return queue

    def rmv_ipclient_list(self):
        res_list = []
        ipclient_list = self.get_ipclient_list()
        if len(ipclient_list) > 0:
            for ip_position in ipclient_list:
                key = list(ip_position.keys())[0]
                ipclient_list_id = ip_position[key]['.id']
                try:
                    res = self.apiclient.talk(["/ip/firewall/address-list/remove", "=.id=" + ipclient_list_id, ])
                except:
                    self.mtlog.log_entry('Fail! cannot remove IP list entry for {}'.format(self.clientip))
                    self.mtlog.log_entry('EXCEPTION - {}'.format(res))
                    sys.stderr.write('Fail! cannot remove IP list entry for {} \n'.format(self.clientip))
                    sys.exit(1)
                else:
                    self.mtlog.log_entry('Info. IP list entry for {} was removed'.format(self.clientip))
                    print('Info. IP list entry for {} was removed'.format(self.clientip))
                    res_list.append(res)
            return res_list
        else:
            self.mtlog.log_entry('Warning! IP list entry for {} did not exist'.format(self.clientip))
            print('Warning! IP list entry for {} did not exist'.format(self.clientip))
            return ipclient_list


class MtCheckParams:
    def __init__(self, clientip, ul, dl, state, action):
        self.clientip = clientip
        self.clientip = list(filter(None, clientip.split(',')))
        for i in range(len(self.clientip)):
           if '/' not in self.clientip[i]:
                self.clientip[i] = self.clientip[i] + '/32'
        self.ul = ul
        self.dl = dl
        self.state = state
        self.action = action
        self.mtlog = MtLogger(clientip)

    def check_rate(self, rate):
        try:
            int(rate)
        except:
            self.mtlog.log_entry('Error! {} - wrong RATE format'.format(rate))
            sys.stderr.write('Error! {} - wrong RATE format \n'.format(rate))
            sys.exit(1)
        else:
            return True

    def check_ip(self, clientip):
        for addr in self.clientip:
            try:
                ipaddress.ip_network(addr)
            except:
                self.mtlog.log_entry('Error! IP/CIDR {} is not valid'.format(clientip))
                sys.stderr.write('Error! IP/CIDR {} is not valid \n'.format(clientip))
                sys.exit(1)
            else:
                return True

    def check_state(self, state):
        if state in mt_hydra_config.state_list:
            return True
        else:
            self.mtlog.log_entry('Error! {} - no such STATE available'.format(state))
            sys.stderr.write('Error! {} - no such STATE available \n'.format(state))
            sys.exit(1)

    def check_action(self, action):
        if action in mt_hydra_config.action_list:
            return True
        else:
            self.mtlog.log_entry('Error! {} - no such ACTION available'.format(action))
            sys.stderr.write('Error! {} - no such ACTION available \n'.format(action))
            sys.exit(1)