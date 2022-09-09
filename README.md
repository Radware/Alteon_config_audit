# Alteon_config_audit

# Owner/Maintainer

	Egor Egorov egore@radware.com

# About

	The script parses Alteon configuration file and creates a csv report which includes recommendations for the best-practice recommendations.

	Input: \Config\<<<Alteon config file>>>
	Output: \Report\altconfig_report.csv

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
