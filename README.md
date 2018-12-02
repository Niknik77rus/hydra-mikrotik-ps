# hydra-mikrotik-ps
Mikrotik provisioning script for Hydra Billing

rate parameters should be provided only for state 'SERV_STATE_Provision' and 'SERV_STATE_Restricted'.
rate should be provided in kbit/s

# usage

create subscriber example:
python3 mt_prov.py --action on --ip '3.3.3.3/32' --state SERV_STATE_Provision --rate_limit_in 128 --rate_limit_out 256
or
python3 mt_prov.py --action on --ip '3.3.3.3/32,10.20.30.0/24' --state SERV_STATE_InsufficientFunds

change subscriber example (new target, state, rate params for the example above):
python3 mt_prov.py --action change  --old_ip '3.3.3.3/32,10.20.30.0/24' --ip '3.3.3.3/32,10.20.30.0/24,4.3.2.0/25' --state  'SERV_STATE_Provision' --rate_limit_in '100' --rate_limit_out '900' 

remove subscriber:
python3 mt_prov.py --action off  --ip '3.3.3.3/32,10.20.30.0/24,4.3.2.0/25'


