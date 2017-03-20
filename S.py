#!/usr/bin/python -t

import sys
import re
import io
import getpass
import argparse

#File1='/usr/local/etc/ansible/hosts.test'
#File0='/etc/ansible/hosts.pve'
File1='/etc/ansible/hosts'

def joinf():
#	text0=open(File0, 'r' )
	text1=open(File1, 'r' )
#	full_text = text0.readlines() + text1.readlines()
	full_text = text1.readlines()
#	text0.close(); 
	text1.close()
	global list
	list = full_text
	return list


def checkperm(line):
	Args=dict(s.split("=") for s in line)
	user=getpass.getuser()
	global IP
	global PORT
	IP = Args['ansible_ssh_host']
	PORT = Args['ansible_ssh_port']
	if re.search( user, Args['users']) is None:
		return 1

def find():
	Count_Server=0
	CountNum=0
	Last_Group = "none"
	Group = "none"
	for line in list:
		parts = line.split()
		if len(parts) > 0:
			#if re.match( "^\[", parts[0]) is not None:
			#print parts[0]

			if re.match( "^#|^\[", parts[0]) is None:
				#perm = checkperm(parts[1:])
				Args=dict(s.split("=") for s in parts[1:])
				user=getpass.getuser()
				#print "Your user is "+ user
				Group = Args['group']
				if re.search( user, Args['users']) is None:
					continue
				#print parts[0]
				#if  perm == 1 :
				#	continue
				if len(sys.argv) > 1:
					Reg=sys.argv[1]
					if re.search(Reg, parts[0]):
						IP = Args['ansible_ssh_host']
						PORT = Args['ansible_ssh_port']
						CountNum = CountNum+1
						if Group != Last_Group:
							print "\n"
						print  parts[0] +"		IP: "+  IP	+" Group: "+ Group
						Count_Server = Count_Server+1
				else:
					IP = Args['ansible_ssh_host']
					PORT = Args['ansible_ssh_port']
					if Group != Last_Group:
						print "\n"
					print  parts[0] +"		IP: "+  IP	+" Group: "+ Group
					Count_Server = Count_Server+1
				
		Last_Group = Group
	print "\nNumber of servers: ", Count_Server
	if CountNum == 1:
		#print  "IP: "+  IP	+" Group: "+ Group
		connect(IP,PORT)

	exit(0)
	


def connect(ip,port):
	import os
	os.system('sudo ssh -p'+ port +' root@'+ip)
	#print "Your ip of server is "+ ip


def main():
	joinf()
	find()

	exit(0)
	
if __name__ == '__main__':
    main()

