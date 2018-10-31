from mt_hydra_controller import MtHydra
from tikapyclients import TikapyClient

class MtHydraLogic():
    def __init__(self):
        print("INIT OK")

    def mt_create(self, apiclient, clientip, ul, dl, white_list):
        mt = MtHydra()
        mt.rmv_ipclient_list(apiclient, clientip)
        mt.add_ipclient_list(apiclient, clientip, white_list)
        mt.rmv_queue(apiclient, clientip)
        mt.add_queue(apiclient, clientip, ul, dl)

    def mt_modify_queue(self, apiclient, clientip, ul, dl):
        mt = MtHydra()
        mt.mod_queue(apiclient, clientip, ul, dl)

    def mt_modify_iplist(self, apiclient, clientip, list_name):
        mt = MtHydra()
        mt.mod_ipclient_list(apiclient, clientip, list_name)


    def mt_remove(self, apiclient, clientip):
        mt = MtHydra()
        mt.rmv_ipclient_list(apiclient, clientip)
        mt.rmv_queue(apiclient, clientip)




