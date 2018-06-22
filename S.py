#!/usr/bin/python -t
# Copyright (c) 2017 Ruslan Variushkin,  ruslan@host4.biz
# Version 0.1.5

log_file='/var/log/multyssh/S.log'


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
            from colorama import Fore, Back, Style
            #if re.match( "^\[", parts[0]) is not None:
            if re.match( "^#|^\[", parts[0]) is None:
                try:
                    Args=dict(s.split("=") for s in parts[1:])
                    user=getpass.getuser()
                    #print "Your user is "+ user
                    Group = Args['group']
                except:
                    continue
                if re.search( user, Args['users']) is None:
                    continue
                if len(sys.argv) > 1:
                    Reg=sys.argv[1]
                    if re.search(Reg, parts[0]) or re.search(Reg,  parts[1]):
                        Host=parts[0]
                        IP = Args['ansible_ssh_host']
                        PORT = Args['ansible_ssh_port']
                        USER = Args['ansible_ssh_user']
                        CountNum = CountNum+1
                        if Group != Last_Group:
                            print "\n"
                        Hostprint(parts[0], IP, Group)
                        Count_Server = Count_Server+1
                else:
                    Host=parts[0]
                    IP = Args['ansible_ssh_host']
                    PORT = Args['ansible_ssh_port']
                    if Group != Last_Group:
                        print "\n"
                    Hostprint(parts[0], IP, Group)
                    Count_Server = Count_Server+1                        
        Last_Group = Group
    print "\nNumber of servers: ", Count_Server
    if CountNum == 1:
        #print  "IP: "+  IP	+" Group: "+ Group
        connect(Host,IP,PORT,USER)
    exit(0)

def Hostprint(host, ip, group):
    from colorama import Fore, Back, Style
    print  (Fore.WHITE  + host + Fore.CYAN+"      IP: "+Fore.RESET +  ip +	 Fore.CYAN+"        Group: "+Fore.RESET + group )


def connect(host,ip,port,user):
    import os
    import getpass
    import datetime
    directory = os.path.dirname(log_file)
    DateTime=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        os.stat(directory)
    except:
        os.mkdir(directory)
    logf=open(log_file,  'a')
    logdata="User: "+getpass.getuser()+" Date Time:["+DateTime+"] Host: "+ host+ " IP: "+ip+" Port: "+port+"\n"
    logf.write(logdata)
    logf.close()
    os.system('sudo ssh -p'+ port +' '+user+'@'+ip)



def main():
	joinf()
	find()

	exit(0)
	
if __name__ == '__main__':
    main()

