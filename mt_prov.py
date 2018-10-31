from mt_hydra_logic import MtHydraLogic
from tikapyclients import TikapyClient
from mt_hydra_config import *
import argparse


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

try:
    print("Trying to connect")
    apiclient = TikapyClient(ipmikrotik, apiport)
except:
    print("WARNING! no connection to the router! Check IP-address reachability and API status on the router")

else:
    try:
        apiclient.login(user, pwd)
    except:
        print("WARNING! Login unsucsessful. Please, check your credentials and restart the script.")
    else:
        print("\nLogin successful")
        mt = MtHydraLogic()
        if action == 'on':
            mt.mt_create(apiclient, clientip, ul, dl, white_list)
        elif action == 'change':
            pass
        #NNK WARNING! completely delete sub from NAS!
        elif action == 'off':
            mt.mt_remove(apiclient, clientip)

        #print(mt.get_ipclient_list(apiclient, "1.1.1.0/24"))
        #print(mt.add_queue(apiclient, "3.2.2.2/32", "1M", "2M"))
        #print(mt.add_ipclient_list(apiclient, "3.2.2.2/32", white_list))
        #print(mt.rmv_queue(apiclient, "3.2.2.2/32"))
        #print(mt.rmv_ipclient_list(apiclient, "3.2.2.2"))
        #print(mt.mod_queue(apiclient, "1.1.1.1/32", "1M", "3M"))
        #mt.mt_modify_iplist(apiclient, "7.7.7.7", 'test')
        #mt.mt_remove(apiclient, "7.7.7.7/32")

