# hydra-mikrotik-ps
Mikrotik provisioning script for Hydra Billing

rate parameters should be provided only for state 'SERV_STATE_Provision' and 'SERV_STATE_Restricted'.
rate should be provided in kbit/s

# usage

a. create subscriber example:
1) python3 mt_prov.py --action on --ip '3.3.3.3/32' --state SERV_STATE_Provision --rate_limit_in 128 --rate_limit_out 256
2) python3 mt_prov.py --action on --ip '3.3.3.3/32,10.20.30.0/24' --state SERV_STATE_InsufficientFunds

b. change subscriber example (new target, state, rate params for the example above):
1) python3 mt_prov.py --action change  --old_ip '3.3.3.3/32,10.20.30.0/24' --ip '3.3.3.3/32,10.20.30.0/24,4.3.2.0/25' --state  'SERV_STATE_Provision' --rate_limit_in '100' --rate_limit_out '900' 

c. remove subscriber:
1) python3 mt_prov.py --action off  --ip '3.3.3.3/32,10.20.30.0/24,4.3.2.0/25'


