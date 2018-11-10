ipmikrotik = "192.168.1.101"
#ipmikrotik = "91.228.118.4"
user = "nnk"
pwd = "Winter@2017"
white_list = "hydra_auth_list"
neg_bal_list = "hydra_negbal_list"
blocked_list = "hydra_blocked_list"
apiport = 8728
#log = "/home/nnk/scripts/mt_hydra.log"
log = "/var/log/hydra/hex/hydra-mikrotik.log"
state_list = ["SERV_STATE_NonPaySuspension", "SERV_STATE_TemporalSuspension",
              "SERV_STATE_InsufficientFunds", "SERV_STATE_Provision", "SERV_STATE_Restricted"]
action_list = ["on", "change", "off"]