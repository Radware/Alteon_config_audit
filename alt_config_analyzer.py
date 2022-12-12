import csv
import os
from tokenize import group

if not os.path.exists('Config'):
	os.makedirs('Config')

if not os.path.exists('Report'):
	os.makedirs('Report')

if not os.path.exists('./Config/1line/'):
	os.makedirs('./Config/1line/')

config_path = "./Config/"
oneline_path = "./Config/1line/"
report_path = "./Report/"

###########################Create headers for the report ##################################################
with open(report_path + 'altconfig_report.csv', mode='w', newline="") as altconfig_report:
		bdos_writer = csv.writer(altconfig_report, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		bdos_writer.writerow(['Alteon Name' , 'Alteon IP' ,	'Virt' , 'Group' , 'Real' , 'Filter', 'Recommendation', 'Priority', 'CLI Command'])


def VIP_to_VRRP(mode_vrrp,vips_dic,vrrp_dic,althost,altip): #Checks if VIP has corresponding VRRP

	if mode_vrrp:
		
		for vip_key,vip_val in vips_dic.items():
			vip_vrrp = False
			# print(vip_val['vip'])

			for vr_key, vr_val in vrrp_dic.items():
				# print(vr_val['addr'])

				if vip_val['vip'] == vr_val['addr']:
					vip_vrrp = True

			if not vip_vrrp:
				with open(report_path + 'altconfig_report.csv', mode='a', newline="") as altconfig_report:
					bdos_writer = csv.writer(altconfig_report, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
					bdos_writer.writerow([f'{althost}' , f'{altip}' , f'{vip_key.split()[1]}' , f'N/A' , f'N/A' , f'N/A', f'Virt "{vip_key.split()[1]}" has no corresponding VRRP configured. It is recommended to configure VRRP for every Virt.' , f'High', f'N/A'])


def PIP_to_VRRP(mode_vrrp,pips_dic_glob,vrrp_dic,vips_dic,althost,altip): #Checks if VIP has corresponding VRRP

	if mode_vrrp:
		
		for pip_ip,pip_vlan in pips_dic_glob.items(): #Check if every global pip has VRRP
			pip_vrrp = False
			# print(vip_val['vip'])

			for vr_key, vr_val in vrrp_dic.items():
				# print(vr_val['addr'])

				if pip_ip == vr_val['addr']:
					pip_vrrp = True

			if not pip_vrrp:
				# print(f'{althost}' , f'{altip}' , f'N/A' , f'N/A' , f'N/A' , f'N/A', f'Global PIP "{pip_ip}" has no corresponding VRRP configured. It is recommended to configure VRRP for every global PIP.' , f'High', f'N/A')
				with open(report_path + 'altconfig_report.csv', mode='a', newline="") as altconfig_report:
					bdos_writer = csv.writer(altconfig_report, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
					bdos_writer.writerow([f'{althost}' , f'{altip}' , f'N/A' , f'N/A' , f'N/A' , f'N/A', f'Global PIP "{pip_ip}" has no corresponding VRRP configured. It is recommended to configure VRRP for every global PIP(only applicable if Master and Standby share the same PIP IP)' , f'High', f'N/A'])

		for vip_key,vip_val in vips_dic.items():
			# print(vip_val['vip'])
			for vip_attr_key, vip_attr_val in vip_val['Services'].items():
				virt_group = vip_attr_val['group']
				for srvc_attr_key, srvc_attr_val in vip_attr_val.items():

					if srvc_attr_key == 'pip' and srvc_attr_val["mode"] == 'address':
						vip_pip_vrrp = False

						vip_pip_ip = srvc_attr_val["addr"].split()[1]

						for vr_key, vr_val in vrrp_dic.items():
							vrrp_ip = vr_val['addr']
	
							if vip_pip_ip == vrrp_ip:
								vip_pip_vrrp = True		

						if not vip_pip_vrrp:
							# print(f'{althost}' , f'{altip}' , f'{vip_key}' , f'{virt_group}' , f'N/A' , f'N/A', f'Virt PIP "{vip_pip_ip}" has no corresponding VRRP configured. It is recommended to configure VRRP for every Virt PIP')
							with open(report_path + 'altconfig_report.csv', mode='a', newline="") as altconfig_report:
								bdos_writer = csv.writer(altconfig_report, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
								bdos_writer.writerow([f'{althost}' , f'{altip}' , f'{vip_key}' , f'{virt_group}' , f'N/A' , f'N/A', f'Virt PIP "{vip_pip_ip}" has no corresponding VRRP configured. It is recommended to configure VRRP for every Virt PIP' , f'High', f'N/A'])


def VRRP_track(vrrp_dic,althost,altip): #Check if each VRRP has Tracking enabled
	for vr_key, vr_val in vrrp_dic.items():
		if 'VRRP Tracking' not in vr_val:
			# print(f'{althost}' , f'{altip}' , f'N/A' , f'N/A' , f'N/A' , f'N/A', f'VRRP "{vr_key}" has no VRRP Tracking configured. It is recommended to configure VRRP Tracking for every VRRP' , f'High', f'N/A')
			with open(report_path + 'altconfig_report.csv', mode='a', newline="") as altconfig_report:
				bdos_writer = csv.writer(altconfig_report, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
				bdos_writer.writerow([f'{althost}' , f'{altip}' , f'N/A' , f'N/A' , f'N/A' , f'N/A', f'VRRP "{vr_key}" has no VRRP Tracking configured. It is recommended to configure VRRP Tracking for every VRRP' , f'High', f'N/A'])


def Config_to_one_line(file,root_dir):
	##########Normalize config file to one line############
	with open(root_dir + '/'+ file, 'r') as f:
		config = f.read()
	
		config = config.replace("\n\t",'/') #Normalize splitted lines (\\\r\n)

	with open(oneline_path + file + f'_1line', 'w') as f:
		f.write(config) #Write updated lines

def parseAltConfigParse(file, root_dir):
	print(file)
	############ Vars ##########	
	althost = 'N/A'
	altip = 'N/A'		
	rcomm = False #SNMPv1/v2 read community
	wcomm = False #SNMPv1/v2 write community
	snmpv1v2_dis = False #SNMPv1/v2 disabled
	radius_mgmt = False
	tacacs_mgmt = False
	syslog_mgmt = False
	snmp_mgmt = False
	ftp_tftp_scp_mgmt = False
	dns_mgmt = False
	ntp_mgmt = False
	mode_vrrp = False
	vrrp_track = False

	vips_dic = {}
	vrrp_dic = {}
	pips_dic_glob = {}


	############# Set Alteon Host and IP and global variables (must have them before running everything else) ################################################

	with open(oneline_path + file + f'_1line') as f:
		for line in f: #parse config file line by line

			if "/c/sys/ssnmp/name" in line:
				althost = line.split()[1].split("/")[0].strip('"')

			if line.startswith('/c/sys/mmgmt/net') and "addr" in line: # standalone configs
				altip = line.split()[2].split("/")[0]

			if line.startswith('/c/sys/mmgmt/dhcp') and "addr" in line: # VA configs
				altip = line.split()[2].split("/")[0]

			if line.startswith('/c/sys/mmgmt/addr'): # vadc configs
				altip = line.split()[1].split("/")[0]

			if '/c/l3/hamode vrrp' in line: # Detect if HA mode is VRRP
				mode_vrrp = True

		f.close() # Need to alteon host before other lines

	#########Parsing config line by line #################
	
	with open(oneline_path + file + f'_1line') as f:
		for line in f: #parse config file line by line

			############# Set Alteon Host and IP ####################################################################
			if "/c/sys/ssnmp/name" in line:
				althost = line.split()[1].split("/")[0].strip('"')

			if line.startswith('/c/sys/mmgmt/net') and "addr" in line: # standalone configs
				altip = line.split()[2].split("/")[0]

			if line.startswith('/c/sys/mmgmt/addr'): # vadc configs
				altip = line.split()[1].split("/")[0]

			############# Map VIPs to dictionary ##################################################################################

			if line.startswith('/c/slb/virt'):

				if line.split()[0].split("/")[3] + ' ' + line.split()[1].split("/")[0] not in vips_dic: #if no vip key value - create it
					
					vips_dic[line.split()[0].split("/")[3] + ' ' + line.split()[1].split("/")[0]] = {} #creaate 
					for i in line.split("/")[4:]:
						if ' ' in i:
							vips_dic[line.split()[0].split("/")[3] + ' ' + line.split()[1].split("/")[0]][i.split()[0]] = ' '.join(map(str, i.split()[1:]))
							# print(i.split()[0] , i.split()[1])
						else: #corner case for "ena" key without value setting value to True
							vips_dic[line.split()[0].split("/")[3] + ' ' + line.split()[1].split("/")[0]][i] = True
				



					
					vips_dic[line.split()[0].split("/")[3] + ' ' + line.split()[1].split("/")[0]]['Services'] = {}


					# vips_dic[line.split()[0].split("/")[3] + ' ' + line.split()[1].split("/")[0]]['Services'][line.split()[2].split("/")[0]] = {}

				elif line.split()[1].split("/")[1] == "service" and  "/group" in line: #for loop for service/s

					vip_service_attr = {}
					for i in line.split("/")[4:]:
							if ' ' in i:
								vip_service_attr[i.split()[0]] = ' '.join(map(str, i.split()[1:]))
							
							else:
								vip_service_attr[i.split()[0]] = True


					vips_dic[line.split()[0].split("/")[3] + ' ' + line.split()[1].split("/")[0]]['Services'][line.split()[2].split("/")[0]] = vip_service_attr


				elif line.split()[1].split("/")[1] == "service" and  "/appshape/" in line: #for loop for service/s
					vips_dic[line.split()[0].split("/")[3] + ' ' + line.split()[1].split("/")[0]]['Services'][line.split()[2].split("/")[0]]['appshape'] = {}
					vip_service_attr = {}
					for i in line.split("/")[5:]:
							if ' ' in i:
								vip_service_attr[i.split()[0]] = ' '.join(map(str, i.split()[1:]))
							
							else:
								vip_service_attr[i.split()[0]] = True


					vips_dic[line.split()[0].split("/")[3] + ' ' + line.split()[1].split("/")[0]]['Services'][line.split()[2].split("/")[0].split("/")[0]]['appshape'] = vip_service_attr


				elif line.split()[1].split("/")[1] == "service" and  "/pip/" in line: #for loop for service/s
					vips_dic[line.split()[0].split("/")[3] + ' ' + line.split()[1].split("/")[0]]['Services'][line.split()[2].split("/")[0]]['pip'] = {}
					vip_service_attr = {}
					for i in line.split("/")[5:]:
							if ' ' in i:
								vip_service_attr[i.split()[0]] = ' '.join(map(str, i.split()[1:]))
							
							else:
								vip_service_attr[i.split()[0]] = True


					vips_dic[line.split()[0].split("/")[3] + ' ' + line.split()[1].split("/")[0]]['Services'][line.split()[2].split("/")[0]]['pip'] = vip_service_attr

				else:
						print(f'Else line if starts with "/c/slb/virt" and is "/service" not in line. Line is: {line}')


			############# Map PIPs to dictionary ##################################################################################
 

			if line.startswith('/c/slb/pip/add'):
				pips_dic_glob[line.split()[1]] = line.split()[2]


			############# Map VRID's ##################################################################################

			if line.startswith('/c/l3/vrrp/vr'):
				if line.split()[0].split("/")[4] + ' ' + line.split()[1].split("/")[0] not in vrrp_dic: #if no vip key value - create it
					vrrp_dic[line.split()[0].split("/")[4] + ' ' + line.split()[1].split("/")[0]] = {}
					for i in line.split("/")[5:]:
						if ' ' in i:
							vrrp_dic[line.split()[0].split("/")[4] + ' ' + line.split()[1].split("/")[0]][i.split()[0]] = ' '.join(map(str, i.split()[1:]))
						else: #corner case for "ena" key without value setting value to True
							vrrp_dic[line.split()[0].split("/")[4] + ' ' + line.split()[1].split("/")[0]][i] = True


				elif line.split()[1].split("/")[1] == "track": # VRRP tracking line

					if 'VRRP Tracking' not in vrrp_dic:
						vrrp_dic[line.split()[0].split("/")[4] + ' ' + line.split()[1].split("/")[0]]['VRRP Tracking'] = {}

					track_attr = {}
					for i in line.split("/")[5:]:
						if ' ' in i:
							track_attr[i.split()[0]] = ' '.join(map(str, i.split()[1:]))
						else: #corner case for "ena" key without value setting value to True
							track_attr[i.split()[0]] = True
					
					vrrp_dic[line.split()[0].split("/")[4] + ' ' + line.split()[1].split("/")[0]]['VRRP Tracking'] = track_attr


			if line.startswith('/c/slb/sync/peer') and 'ena' not in line:
				with open(report_path + 'altconfig_report.csv', mode='a', newline="") as altconfig_report:
					bdos_writer = csv.writer(altconfig_report, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
					bdos_writer.writerow([f'{althost}' , f'{altip}' , f'N/A' , f'N/A' , f'N/A' , f'N/A', f'Config sync is disabled. It is recommended to configure configuration synchronization between the Alteon pair.' , f'High'])
	
			############# Check if non ICMP healthcheck is configured on the server group #############################
			if "/c/slb/group" in line and "add " in line:
				if "health icmp" in line:
					# print(f'Group "{str(line.split()[1].split("/")[0])}" has healtcheck ICMP- line --> {line}')
					with open(report_path + 'altconfig_report.csv', mode='a', newline="") as altconfig_report:
						bdos_writer = csv.writer(altconfig_report, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
						bdos_writer.writerow([f'{althost}' , f'{altip}' , f'N/A' , str(line.split()[1].split("/")[0]) , f'N/A' , f'N/A', f'Group "{str(line.split()[1].split("/")[0])}" has a healtcheck type "ICMP". The recommended healthcheck types are TCP, Web Page, UDP' , f'Medium'])

			############ Check if NTP is set up ###############################################################################
			if "/c/sys/ntp/" in line and "prisrv" not in line:
				# print(line)
				with open(report_path + 'altconfig_report.csv', mode='a', newline="") as altconfig_report:
					bdos_writer = csv.writer(altconfig_report, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
					bdos_writer.writerow([f'{althost}' , f'{altip}' , f'N/A' , f'N/A' , f'N/A' , f'N/A', f'No NTP server is configured. It is recommended to set up NTP' , f'Medium'])

			############ Check if Telnet management access is disabled #########################################################
			if "/c/sys/access/" in line:
				if "tnet ena" in line or "/telnet/on" in line:
					with open(report_path + 'altconfig_report.csv', mode='a', newline="") as altconfig_report:
						bdos_writer = csv.writer(altconfig_report, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
						bdos_writer.writerow([f'{althost}' , f'{altip}' , f'N/A' , f'N/A' , f'N/A' , f'N/A', f'Telnet management access is enabled. It is recommended to disable it' , f'High', f'/c/sys/access/tnet dis'])

			############ Check if HTTP management access is disabled ###########################################################
			if "/c/sys/access/" in line:
				if "http ena"in line or "/http/on" in line:
					with open(report_path + 'altconfig_report.csv', mode='a', newline="") as altconfig_report:
						bdos_writer = csv.writer(altconfig_report, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
						bdos_writer.writerow([f'{althost}' , f'{altip}' , f'N/A' , f'N/A' , f'N/A' , f'N/A', f'HTTP management access is enabled. It is recommended to disable it' , f'High', f'/c/sys/access/http dis'])

			############ Check if SSHv1 management access is disabled ###########################################################

			if "/c/sys/access/" in line:
				if "sshv1 ena" in line:
					with open(report_path + 'altconfig_report.csv', mode='a', newline="") as altconfig_report:
						bdos_writer = csv.writer(altconfig_report, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
						bdos_writer.writerow([f'{althost}' , f'{altip}' , f'N/A' , f'N/A' , f'N/A' , f'N/A', f'SSHv1 management access is enabled. It is recommended to disable it' , f'High', f'/c/sys/access/sshv1 dis'])

			############ Check if rtsmac (Return to Last Hop) is enabled under the VIP ###########################################################

			if line.startswith('/c/slb/virt') and '/vip' in line:
				if 'rtsrcmac ena' not in line:
					with open(report_path + 'altconfig_report.csv', mode='a', newline="") as altconfig_report:
						bdos_writer = csv.writer(altconfig_report, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
						bdos_writer.writerow([f'{althost}' , f'{altip}' , f'{line.split()[1].split("/")[0]}' , f'N/A' , f'N/A' , f'N/A', f'"Return to Last Hop" is disabled. It is recommended to enable to prevent asymmetric routing back which may occur' , f'High', f'/cfg/slb/virt {line.split()[1].split("/")[0]}/rtsrcmac e'])


			############ Check if VRID has "share dis" set ###########################################################

			if mode_vrrp and line.startswith('/c/l3/vrrp/vr') and 'ipver v4' in line:
				if 'share dis' not in line:
					with open(report_path + 'altconfig_report.csv', mode='a', newline="") as altconfig_report:
						bdos_writer = csv.writer(altconfig_report, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
						bdos_writer.writerow([f'{althost}' , f'{altip}' , f'N/A' , f'N/A' , f'N/A' , f'N/A', f'"share dis" is not set for vr "{line.split()[1].split("/")[0]}". It is recommended to configure "share dis" so only prmary Alteon will process the the vrid matching traffic. In case the traffic destined to vrid enters the secondary Alteon, it will silently drop it.' , f'High', f'/c/l3/vrrp/vr {line.split()[1].split("/")[0]}/share dis'])

			############ Detect if DNS, NTP are routed through management interface ###########################################################

			if line.startswith('/c/sys/mmgmt'):
				if 'radius mgmt' in line:
					radius_mgmt = True
				if 'tacacs mgmt' in line:
					tacacs_mgmt = True
				if 'syslog mgmt' in line:
					syslog_mgmt = True
				if 'snmp mgmt' in line:
					snmp_mgmt = True
				if 'tftp mgmt' in line:
					ftp_tftp_scp_mgmt = True		
				if 'dns mgmt' in line:
					dns_mgmt = True	
				if 'ntp mgmt' in line:
					ntp_mgmt = True						
			

			############ Detect if SNMPv1/v2 read/write communies are not set to default "public"/"private" #######################################

			if "/c/sys/ssnmp/snmpv3/v1v2 dis" in line:
				snmpv1v2_dis = True

			############ Detect if SNMPv1/v2 is enabled" #######################################

			if "/c/sys/ssnmp/" in line:
				if "rcomm" in line:
					rcomm = True
				if "wcomm" in line:
					wcomm = True

		################ Report if SNMPv1/v2 read community is not set to default "public" ###########################################################

		if not rcomm:

			with open(report_path + 'altconfig_report.csv', mode='a', newline="") as altconfig_report:
				bdos_writer = csv.writer(altconfig_report, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
				bdos_writer.writerow([f'{althost}' , f'{altip}' , f'N/A' , f'N/A' , f'N/A' , f'N/A', f'SNMPv1/v2 read community is set to default "public". It is recommended to use SNMPv3 or set it to a unique value', f'High'])

		if not wcomm:

			with open(report_path + 'altconfig_report.csv', mode='a', newline="") as altconfig_report:
				bdos_writer = csv.writer(altconfig_report, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
				bdos_writer.writerow([f'{althost}' , f'{altip}' , f'N/A' , f'N/A' , f'N/A' , f'N/A', f'SNMPv1/v2 write community is set to default "private". It is recommended to use SNMPv3 or set it to a unique value', f'High'])

		################ Report if SNMPv1/v2 is enabled ###########################################################

		if not snmpv1v2_dis:
			with open(report_path + 'altconfig_report.csv', mode='a', newline="") as altconfig_report:
				bdos_writer = csv.writer(altconfig_report, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
				bdos_writer.writerow([f'{althost}' , f'{altip}' , f'N/A' , f'N/A' , f'N/A' , f'N/A', f'SNMPv1v2 protocol is enabled. It is recommended to disable SNMPv1v2 and use SNMPv3 instead', f'Medium'])

		################ Report if protocols are not routed through management interface ###########################################################

		if not radius_mgmt:
			with open(report_path + 'altconfig_report.csv', mode='a', newline="") as altconfig_report:
				bdos_writer = csv.writer(altconfig_report, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
				bdos_writer.writerow([f'{althost}' , f'{altip}' , f'N/A' , f'N/A' , f'N/A' , f'N/A', f'Radius protocol is not routed through management interface. If Radius is in use, it is recommended to use mangement interface for Radius communication', f'Low', f'/cfg/sys/mmgmt/radius mgmt'])

		if not tacacs_mgmt:
			with open(report_path + 'altconfig_report.csv', mode='a', newline="") as altconfig_report:
				bdos_writer = csv.writer(altconfig_report, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
				bdos_writer.writerow([f'{althost}' , f'{altip}' , f'N/A' , f'N/A' , f'N/A' , f'N/A', f'Tacacs+ protocol is not routed through management interface. If Tacacs+ protocol is in use, it is recommended to use mangement interface for Tacacs+ communication', f'Low', f'/cfg/sys/mmgmt/tacacs mgmt'])

		if not syslog_mgmt:
			with open(report_path + 'altconfig_report.csv', mode='a', newline="") as altconfig_report:
				bdos_writer = csv.writer(altconfig_report, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
				bdos_writer.writerow([f'{althost}' , f'{altip}' , f'N/A' , f'N/A' , f'N/A' , f'N/A', f'Syslog protocol is not routed through management interface. It is recommended to use mangement interface for sending syslog.', f'Low', f'/cfg/sys/mmgmt/syslog mgmt'])

		if not snmp_mgmt:
			with open(report_path + 'altconfig_report.csv', mode='a', newline="") as altconfig_report:
				bdos_writer = csv.writer(altconfig_report, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
				bdos_writer.writerow([f'{althost}' , f'{altip}' , f'N/A' , f'N/A' , f'N/A' , f'N/A', f'SNMP Traps are not routed through management interface. It is recommended to use mangement interface for sending SNMP Traps.', f'Low', f'/cfg/sys/mmgmt/snmp mgmt'])

		if not ftp_tftp_scp_mgmt:
			with open(report_path + 'altconfig_report.csv', mode='a', newline="") as altconfig_report:
				bdos_writer = csv.writer(altconfig_report, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
				bdos_writer.writerow([f'{althost}' , f'{altip}' , f'N/A' , f'N/A' , f'N/A' , f'N/A', f'FTP, TFTP, SCP protocols are not routed through management interface. It is recommended to use mangement interface for FTP, TFTP, SCP communication', f'Low', f'/cfg/sys/mmgmt/tftp mgmt'])

		if not dns_mgmt:
			with open(report_path + 'altconfig_report.csv', mode='a', newline="") as altconfig_report:
				bdos_writer = csv.writer(altconfig_report, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
				bdos_writer.writerow([f'{althost}' , f'{altip}' , f'N/A' , f'N/A' , f'N/A' , f'N/A', f'DNS communication is not routed through management interface. It is recommended to use mangement interface for DNS communication', f'Low', f'/cfg/sys/mmgmt/dns mgmt'])

		if not ntp_mgmt:
			with open(report_path + 'altconfig_report.csv', mode='a', newline="") as altconfig_report:
				bdos_writer = csv.writer(altconfig_report, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
				bdos_writer.writerow([f'{althost}' , f'{altip}' , f'N/A' , f'N/A' , f'N/A' , f'N/A', f'NTP communication is not routed through management interface. It is recommended to use mangement interface for NTP communication', f'Low', f'/cfg/sys/mmgmt/ntp mgmt'])



	
	############ Detect if VIP has corresponding VRRP ##############
	VIP_to_VRRP(mode_vrrp,vips_dic,vrrp_dic,althost,altip)
	################################################################
	PIP_to_VRRP(mode_vrrp,pips_dic_glob,vrrp_dic,vips_dic,althost,altip)
	############ Detect if VRRP Tracking is enabled ################
	VRRP_track(vrrp_dic,althost,altip)


	# print(vips_dic)
	# print(vrrp_dic)
	# print(pips_dic_glob)

for root, dirs, files in os.walk(config_path):
	if "1line" in dirs: 
		dirs.remove("1line") #exclude 1line folder
	for file in files:
		Config_to_one_line(file,root)
		parseAltConfigParse(file,root)









