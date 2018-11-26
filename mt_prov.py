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

args = parser.parse_args()
clientip = args.ip
ul = args.rate_limit_out
dl = args.rate_limit_in
action = args.action
state = args.state
old_ip = args.old_ip

if len(clientip) < 2:
    sys.stderr.write("Info. Dummy call. Empty list of IP addresses. \n")
    sys.exit(0)

checker = MtCheckParams(clientip, ul, dl, state, action)
mtlog = MtLogger(clientip)

ip_list = neg_bal_list

if checker.check_action(action) and checker.check_ip(clientip):
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
            checker.check_rate(ul) and checker.check_rate(dl)
            if state in ['SERV_STATE_InsufficientFunds', 'SERV_STATE_NonPaySuspension',
                         'SERV_STATE_TemporalSuspension']:
                mt.mt_create(ul, dl, neg_bal_list)
            else:
                mt.mt_create(ul, dl, white_list)
        elif action == 'change':
            if old_ip is not None:
                mt.mt_modify_ip_set(old_ip)
            elif state in ['SERV_STATE_InsufficientFunds', 'SERV_STATE_NonPaySuspension',
                         'SERV_STATE_TemporalSuspension']:
                mt.mt_modify_iplist(neg_bal_list)
            elif state in ['SERV_STATE_Provision', 'SERV_STATE_Restricted']:
                if ul is not None and dl is not None:
                    if checker.check_rate(ul) and checker.check_rate(dl):
                        mt.mt_modify_queue(ul, dl)
                        mt.mt_modify_iplist(white_list)
                    else:
                        mtlog.log_entry("Error! queue params check failed")
                        sys.stderr.write("Error! queue params check failed \n")
                        sys.exit(1)
                else:
                    mt.mt_modify_iplist(white_list)
        elif action == 'off':
            mt.mt_remove()
else:
    mtlog.log_entry("Error! params check failed \n")
    sys.exit(1)
