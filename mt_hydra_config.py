ipmikrotik = "192.168.1.101"
#ipmikrotik = "174.138.1.242"
user = "nnk"
pwd = "Winter@2017"
white_list = "hydra_auth_list"
neg_bal_list = "hydra_negbal_list"
blocked_list = "hydra_blocked_list"
apiport = 8728
log = "/var/log/hydra/hex/hydra-mikrotik.log"
#log = "/home/nnk/scripts/mt_hydra.log"
state_list = ["SERV_STATE_NonPaySuspension", "SERV_STATE_TemporalSuspension",
              "SERV_STATE_InsufficientFunds", "SERV_STATE_Provision", "SERV_STATE_Restricted"]
action_list = ["on", "change", "off"]