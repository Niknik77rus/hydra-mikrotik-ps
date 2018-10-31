class MtHydra:

    def __init__(self):
        #self.ipmikrotik = ipmikrotik
        #self.ul = ul
        #self.dl = dl
        print("INIT OK")

    def get_queue(self, apiclient, clientip):
        res = apiclient.talk(["/queue/simple/print", "?target=" + clientip, "=.proplist=.id"])
        return res

    def get_ipclient_list(self, apiclient, clientip):
        if clientip[-3:] == '/32':
            clientip = clientip[:-3]
        res = apiclient.talk(["/ip/firewall/address-list/print", "?address=" + clientip, "=.proplist=.id"])
        clientip = clientip + '/32'
        return res

    def add_queue(self, apiclient, clientip, ul, dl):
        res = apiclient.talk(["/queue/simple/add", "=target=" + clientip, "=max-limit=" + ul + "/" + dl, "=.proplist=.id"])
        return res

    def add_ipclient_list(self, apiclient, clientip, list_name):
        res = apiclient.talk(["/ip/firewall/address-list/add", "=address=" + clientip, "=list=" + list_name, "=.proplist=.id"])
        return res

    def mod_queue(self, apiclient, clientip, ul, dl):
        queue = self.get_queue(apiclient, clientip)
        key = list(queue.keys())[0]
        queue_id = queue[key]['.id']
        res = apiclient.talk(["/queue/simple/set", "=max-limit=" + ul + "/" + dl, "=.id=" + queue_id, ])
        return res

    def mod_ipclient_list(self, apiclient, clientip, list_name):
        ipclient_list = self.get_ipclient_list(apiclient, clientip)
        if len(ipclient_list) > 0:
            key = list(ipclient_list.keys())[0]
            ipclient_list_id = ipclient_list[key]['.id']
        res = apiclient.talk(["/ip/firewall/address-list/set", "=list=" + list_name, "=.id=" + ipclient_list_id, ])
        return res


    def rmv_queue(self, apiclient, clientip):
        queue = self.get_queue(apiclient, clientip)
        if len(queue) > 0:
            key = list(queue.keys())[0]
            queue_id = queue[key]['.id']
            res = apiclient.talk(["/queue/simple/remove", "=.id=" + queue_id, ])
        else:
            print("no such QUEUE")
            res = 'NoQUEUE'
        return res

    def rmv_ipclient_list(self, apiclient, clientip):
        ipclient_list = self.get_ipclient_list(apiclient, clientip)
        if len(ipclient_list) > 0:
            key = list(ipclient_list.keys())[0]
            ipclient_list_id= ipclient_list[key]['.id']
            res = apiclient.talk(["/ip/firewall/address-list/remove", "=.id=" + ipclient_list_id, ])
        else:
            print("no such IP")
            res = 'NoIP'
        return res