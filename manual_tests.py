# -*- coding: utf-8 -*-
from mt_hydra_logic import *
from mt_hydra_controller import MtCheckParams
from tikapyclients import TikapyClient
import argparse
import sys


parser = argparse.ArgumentParser()
parser.add_argument("--action",
                    help="create/change/delete subscriber")
parser.add_argument("--ip",
                    help="subscribers ip or subnet")
parser.add_argument("--state",
                    help="subscribers state in terms of Hydra")
parser.add_argument("--rate_limit_in",
                    help="subscribers rate-limit-in")
parser.add_argument("--rate_limit_out",
                    help="subscribers rate-limit-out")

args = parser.parse_args()
clientip = args.ip
ul = args.rate_limit_out
dl = args.rate_limit_out
action = args.action
state = args.state

ipmikrotik = ""
user = "nnk"
pwd = ""
white_list = "hydra_auth_list"
neg_bal_list = "hydra_negbal_list"
blocked_list = "hydra_blocked_list"
apiport = 8728
log = "/home/nnk/scripts/mt_hydra.log"
state_list = ["SERV_STATE_NonPaySuspension", "SERV_STATE_TemporalSuspension",
              "SERV_STATE_InsufficientFunds", "SERV_STATE_Provision", "SERV_STATE_Restricted"]
action_list =  ["on", "modify", "off"]



#chk = MtCheckParams(clientip, ul, dl, state, action)
#chk.check_state("off", "1.2.2.2")
#chk.check_rate("250k", "1.2.2.2")
#chk.check_ip("off")


try:
    print("Trying to connect")
    apiclient = TikapyClient(ipmikrotik, apiport)
except:
    print("WARNING! no connection to the router! Check IP-address reachability and API status on the router")
    sys.exit(1)

else:
    try:
        apiclient.login(user, pwd)
    except:
        print("WARNING! Login unsucsessful. Please, check your credentials and restart the script.")
    else:
        print("\nLogin successful")
        #res = apiclient.talk(["/queue/simple/print", "?target=" + clientip, ])
        #mt = MtHydraLogic()
        if action == 'on':
            #mt.mt_create(apiclient, clientip, ul, dl, white_list)
            pass

        elif action == 'change':
            pass
        #NNK WARNING! completely delete sub from NAS!
        elif action == 'off':
            pass
            #mt.mt_remove(apiclient, clientip)
        else:
            pass

        mth = MtHydraLogic(apiclient, "8.8.8.8,2.2.2.0/28,3.2.2.0/28")
        #mth.mt_create(500,700, white_list)
        #mth.mt_remove()
        #mth.mt_modify_queue(800,9000)
        #mth.mt_modify_iplist(neg_bal_list)
        #mth.mt_modify_ip_set("1.1.1.1,2.2.2.0/28,3.2.2.0/28")

        #mth = MtHydra(apiclient, "4.4.4.4/32,2.2.2.0/28,3.2.2.0/28")
        #mth.add_ipclient_list(white_list)
        #mth.add_queue('100', '200')
        #mth.get_ipclient_list()
        #mth.get_queue()
        #mth.mod_queue(500,700)
        #mth.mod_ipclient_list(neg_bal_list)
        #mth.rmv_queue()
        #mth.rmv_ipclient_list()
        #mth.get_list_name("1.1.1.1,2.2.2.0/28,3.2.2.0/28")
        #mth.mod_queue_target("1.1.1.1/32,2.2.2.0/28,3.2.2.0/28")