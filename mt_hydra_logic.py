from mt_hydra_controller import MtHydra
import sys


class MtHydraLogic:
    def __init__(self, apiclient, clientip):
        self.mt = MtHydra(apiclient, clientip)

    def mt_create(self, ul, dl, ip_list):
        try:
            if all(len(item) == 0 for item in self.mt.get_ipclient_list()):
                self.mt.add_ipclient_list(ip_list)
            else:
                self.mt.mtlog.log_entry('Fail! cannot create new client - IP/CIDR {} already exist'.format(self.mt.clientip))
                sys.stderr.write('Fail! cannot create new client - IP/CIDR {} already exist \n'.format(self.mt.clientip))
                sys.exit(1)
            if len(ul) == len(ul) == 0:
                print('Info. No queue params. Queue was not created.')
                pass
            elif len(self.mt.get_queue()) == 0 and len(ul) > 0 and len(dl) > 0:
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

    def mt_modify_ip_set(self, old_ip, provided_list_name, ul, dl):
        new_ip_list = self.mt.clientip
        old_ip_list = list(filter(None, old_ip.split(',')))
        for i in range(len(old_ip_list)):
            if '/' not in old_ip_list[i]:
                old_ip_list[i] = str(old_ip_list[i]) + '/32'
        added_ip_list = list(set(self.mt.clientip) - set(old_ip_list))
        print('adding addresses list: ', added_ip_list, )
        removed_ip_list = list(set(old_ip_list) - set(self.mt.clientip))
        print('removing addresses list: ', removed_ip_list)
        # getting existing settings
        self.mt.clientip = old_ip_list
        print("MANGLE set clientip to OLD-IP", old_ip_list)
        old_queue_params = self.mt.get_queue()
        if len(old_queue_params) > 0:
            key = list(old_queue_params.keys())[0]
            queue_id = old_queue_params[key]['.id']
            queue_target = old_queue_params[key]['target']
            queue_max_limit = old_queue_params[key]['max-limit']
            print(queue_max_limit)
        else:
            queue_target = new_ip_list
            queue_max_limit = ul + '/' + dl
        old_ip_list_params = self.mt.get_ipclient_list()
        if len(old_ip_list_params) > 0:
            key = list(old_ip_list_params[0].keys())[0]
            ip_entry_id = old_ip_list_params[0][key]['.id']
            ip_entry_list = old_ip_list_params[0][key]['list']
        else:
            ip_entry_list = provided_list_name
        # performing actions with regards of result of comparing the lists
        if new_ip_list == old_ip_list:
            print('old IP list equals new IP list')
            try:
                if provided_list_name != ip_entry_list:
                    self.mt.mod_ipclient_list(provided_list_name)
                if queue_max_limit != (ul + '/' + dl) and len(old_queue_params)>0 and len(ul) > 0:
                    self.mt.mod_queue(ul, dl)
                elif len(ul) > 0:
                    self.mt.add_queue(ul, dl)
                else:
                    self.mt.rmv_queue()
            except:
                self.mt.mtlog.log_entry('Fail! cannot modify parameters for {}'.format(self.mt.clientip))
                sys.stderr.write('Fail! cannot modify parameters for {} \n'.format(self.mt.clientip))
            else:
                self.mt.mtlog.log_entry('Success. List name or max-limit was modified for {}'.format(self.mt.clientip))
                print('Success. List name or max-limit was modified for {}'.format(self.mt.clientip))
                return True

        elif added_ip_list and not removed_ip_list:
            try:
                print('trying to add new addresses')
                if provided_list_name != ip_entry_list:
                    self.mt.mod_ipclient_list(provided_list_name)
                if queue_max_limit != (ul + '/' + dl) and len(old_queue_params) > 0 and len(ul) > 0:
                    self.mt.mod_queue(ul, dl)
                self.mt.clientip = new_ip_list
                if len(new_ip_list) > 0 and len(old_ip_list) > 0 and len(old_queue_params) > 0 and len(ul) > 0:
                    self.mt.mod_queue_target(old_ip, ul, dl)
                elif len(new_ip_list) > 0 and len(old_queue_params) == 0 and len(ul) > 0:
                    self.mt.add_queue(ul, dl)
                else:
                    self.mt.rmv_queue()
                self.mt.clientip = added_ip_list
                self.mt.add_ipclient_list(provided_list_name)
            except:
                self.mt.mtlog.log_entry('Fail! cannot add new addresses: {}'.format(added_ip_list))
                sys.stderr.write('Fail! cannot add new addresses: {} \n'.format(added_ip_list))
                sys.exit(1)
            else:
                self.mt.mtlog.log_entry('Success. added new addresses: {}'.format(added_ip_list))
                print('Success. added new addresses: {}'.format(added_ip_list))
                return True

        elif not added_ip_list and removed_ip_list:
            try:
                print('trying to remove old addresses')
                if len(new_ip_list) > 0:
                    if provided_list_name != ip_entry_list:
                        self.mt.mod_ipclient_list(provided_list_name)
                    if queue_max_limit != (ul + '/' + dl) and len(old_queue_params) > 0 and len(ul) > 0:
                        self.mt.mod_queue(ul, dl)
                    if len(ul) == 0:
                        self.mt.rmv_queue()
                    else:
                        self.mt.clientip = new_ip_list
                        self.mt.mod_queue_target(old_ip, ul, dl)
                    self.mt.clientip = removed_ip_list
                    self.mt.rmv_ipclient_list()
                else:
                    self.mt.clientip = old_ip_list
                    self.mt.rmv_queue()
                    self.mt.rmv_ipclient_list()
            except:
                self.mt.mtlog.log_entry('Fail! cannot remove old addresses: {}'.format(removed_ip_list))
                sys.stderr.write('Fail! cannot remove old addresses: {}'.format(removed_ip_list))
                sys.exit(1)
            else:
                self.mt.mtlog.log_entry('Success. removed old addresses: {}'.format(removed_ip_list))
                print('Success. removed old addresses: {}'.format(removed_ip_list))


        elif added_ip_list and removed_ip_list:
            try:
                print('trying to replace target addresses')
                self.mt.clientip = new_ip_list

                #adding new addresses with provided LIST NAME
                self.mt.add_ipclient_list(provided_list_name)

                #changing queue limits, using OLD IP
                if queue_max_limit != (ul + '/' + dl) and len(old_queue_params) > 0 and len(ul) > 0:
                    self.mt.clientip = old_ip_list
                    self.mt.mod_queue(ul, dl)

                # changing queue IP target
                if len(old_queue_params) > 0 and len(ul) > 0:
                    self.mt.clientip = new_ip_list
                    self.mt.mod_queue_target(old_ip, ul, dl)
                elif len(ul) > 0:
                    self.mt.add_queue(ul, dl)
                else:
                    self.mt.clientip = old_ip_list
                    self.mt.rmv_queue()

                #removing OLD IP entries
                self.mt.clientip = removed_ip_list
                self.mt.rmv_ipclient_list()

            except:
                self.mt.mtlog.log_entry('Fail! cannot replace target addresses: {}'.format(removed_ip_list))
                sys.stderr.write('Fail! cannot replace target addresses: {}\n'.format(removed_ip_list))
                sys.exit(1)
            else:
                self.mt.mtlog.log_entry('Success. replaced target addresses with: {}'.format(added_ip_list))
                print('Success. replaced target addresses with: {}'.format(added_ip_list))





