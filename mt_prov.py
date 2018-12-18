from mt_hydra_logic import *
from mt_hydra_config import *
from mt_hydra_controller import MtCheckParams, MtLogger
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
parser.add_argument("--old_ip",
                    help="subscribers old ip list")
parser.add_argument("--nas_ip",
                    help="subscribers NAS ip")

args = parser.parse_args()
clientip = args.ip
ul = str(args.rate_limit_out)
dl = str(args.rate_limit_in)
action = args.action
state = args.state
old_ip = args.old_ip
ipmikrotik = args.nas_ip

if ul == dl == 'None':
    ul = dl = ''

checker = MtCheckParams(clientip, ul, dl, state, action)
mtlog = MtLogger(clientip)

try:
    mtlog.log_entry("Trying to connect")
    print("Trying to connect")
    apiclient = TikapyClient(ipmikrotik, apiport)
    apiclient.login(user, pwd)
except:
    mtlog.log_entry("Fail! no connection to IP or API. Either login failed.")
    sys.stderr.write("Fail! no connection to IP or API. Either login failed. \n")
    sys.exit(1)
else:
    mtlog.log_entry("Success. Login OK")
    print("Success. Login OK")
    mt = MtHydraLogic(apiclient, clientip)
    if action == 'on':
        if len(clientip) < 2:
            print("Info. Dummy call. Empty list of new addresses")
            sys.exit(0)
        else:
            if state in ['SERV_STATE_InsufficientFunds', 'SERV_STATE_Restricted']:
                mt.mt_create(ul, dl, neg_bal_list)
            elif state in ['SERV_STATE_NonPaySuspension', 'SERV_STATE_TemporalSuspension']:
                mt.mt_create(ul, dl, blocked_list)
            else:
                mt.mt_create(ul, dl, white_list)
    elif action == 'change':
        if state in ['SERV_STATE_InsufficientFunds', 'SERV_STATE_Restricted']:
            mt.mt_modify_ip_set(old_ip, neg_bal_list, ul, dl)
        elif state in ['SERV_STATE_NonPaySuspension', 'SERV_STATE_TemporalSuspension']:
            mt.mt_modify_ip_set(old_ip, blocked_list, ul, dl)
        else:
            mt.mt_modify_ip_set(old_ip, white_list, ul, dl)
    elif action == 'off':
        mt.mt_remove()