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

args = parser.parse_args()
clientip = args.ip
ul = args.rate_limit_out
dl = args.rate_limit_in
action = args.action
state = args.state


checker = MtCheckParams(clientip, ul, dl, state, action)
mtlog = MtLogger(clientip)


def check_params():
    if checker.check_action(action) and \
       checker.check_state(state) and \
       checker.check_ip(clientip):
        return True


ip_list = neg_bal_list

if check_params():
    try:
        mtlog.log_entry("Trying to connect")
        apiclient = TikapyClient(ipmikrotik, apiport)
        apiclient.login(user, pwd)
    except:
        mtlog.log_entry("WARNING! no connection to IP or API. Either login failed.")
        sys.exit(1)
    else:
        mtlog.log_entry("Success. Login OK")
        mt = MtHydraLogic(apiclient, clientip)
        if action == 'on':
            checker.check_rate(ul) and checker.check_rate(dl)
            mt.mt_create(ul, dl, ip_list)
        elif action == 'change':
            if state in ['SERV_STATE_InsufficientFunds', 'SERV_STATE_NonPaySuspension',
                         'SERV_STATE_Restricted', 'SERV_STATE_TemporalSuspension']:
                mt.mt_modify_iplist(neg_bal_list)
            if state == 'SERV_STATE_Provision':
                if ul is not None and dl is not None:
                    if checker.check_rate(ul) and checker.check_rate(dl):
                        mt.mt_modify_queue(ul, dl)
                    else:
                        mtlog.log_entry("WARNING! queue params check failed")
                        sys.exit(1)
                else:
                    mt.mt_modify_iplist(white_list)
        elif action == 'off':
            mt.mt_remove()
else:
    mtlog.log_entry("WARNING! params check failed")
    sys.exit(1)
