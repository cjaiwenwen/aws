#!/usr/bin/python
import paramiko
from platform import system as system_name
from os import system as system_call
import time
from IPy import IP


class Network(object):


    def __init__(self, PEM_LOCAITON):
        self.__pem_location = PEM_LOCAITON


    def _ssh_connect(self, server):
        k = paramiko.RSAKey.from_private_key_file("%s" % self.__pem_location)
        c = paramiko.SSHClient()
        c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        print "[*] Connecting to %s" % server
        try:
            c.connect(server, username='ec2-user', pkey=k, timeout=30)
            print "[*] %s is Succesfully Connected: " % server
            time.sleep(1)
            print "[*] Issuing command line <uptime>"
            stdin, stdout, stderr = c.exec_command("uptime")
            stdin.flush()
            data = stdout.read().splitlines()
            for line in data:
                print line
            c.close()
            return True
        except:
            print "[*] Server is still initializing"
            return False


    def _ping(self, server):
        print "[*] Start to ping server %s" % server
        # Ping parameters as function of OS
        parameters = "-n 1" if system_name().lower() == "windows" else "-c 1"
        # Pinging
        time.sleep(1)
        try:
            if system_call("ping " + parameters + " " + server) == 0:
                print "[*] Ping is reachable to server %s" % server
                return True
        except:
            pass

    def _ip_validation(self, value):
        ip = IP(value)
        if ip.iptype() == 'PUBLIC':
            return True
        else:
            return False