# Alteon_config_audit

# Owner/Maintainer

	Egor Egorov egore@radware.com

# About

	The script parses Alteon configuration file and creates a csv report which includes recommendations for the best-practice recommendations.

	Input: \Config\<<<Alteon config file>>>
	Output: \Report\altconfig_report.csv

# Version control

V1.1 Fixed two bugs
	- Alteon VA - fixed missing management IP
	- Alteon VA - fixed wrong identification of routing management protocols through management/data port

V1.2 Added redirect service handling

V1.3 (7/6/2023)
	- Added "Category" column to the report

V1.3.1 (8/3/2023)
	- Added notes for VRRP recommendations for VIPs and PIPs
		f'Virt "{vip_key.split()[1]}" has no corresponding VRRP configured. It is recommended to configure VRRP for every Virt. (Only applicable for Virts belonging to the same subnet of an Alteon Interface).'

		f'Virt PIP "{vip_pip_ip}" has no corresponding VRRP configured. It is recommended to configure VRRP for every Virt PIP(only applicable if Master and Standby share the same PIP IP)'
		
# How to run

	1. Place Alteon config file or files under \Config\ path
	2. Run the script
		python alt_config_analyzer.py
	3. Get report under \Report\altconfig_report.csv path




# Config audit checks scope

	1. Alert if healtcheck is ICMP or no healtcheck. Use TCP or HTTP page HC.
	2. Validate NTP is set up
	3. Hardening recommendations
		- Disable HTTP, telnet, SSHv1 managment access
		- Do not use SNMPv2
		- Do not use default SNMP communities
	4. If dbind force proxy, recommendation to enable rtsrcmac under the virt (respond back to the same host MAC from which the packet has been received to prevent asymmetric backrouting issues)
	5. Point DNS/NTP/SNMP/Syslog/Tacacs to management port (default DATA)
	6. If VRRP is in use, “share dis” should be set up under each vrid (with this setting - if the traffic reaches backup Alteon, it won't process the traffic and will drop it ilently)
	7. Interface tracking should be enabled
	8. HA config proper set up
		- 	Every VIP and PIP should have VR (otherwise both Alteons even stnadby will respond on ARP req)



# Limitations
- 5/2/2022 - no VX config support, vADC only or physical appliance configs only
- 5/2/2022 - Telnet recommendation line in report has no Alteon host defined since it is defined later in the CLI
