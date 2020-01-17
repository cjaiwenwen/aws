#!/usr/bin/env python

from __future__ import print_function
import boto3
import time
import re
from prettytable import PrettyTable
from IPy import IP
from awspackage import network
import os
import socket
from os.path import expanduser
from awspackage import provisioner

class AWS(network.Network, provisioner.Provisioner):


    def __init__(self, DOMAIN, PEM_LOCATION, Module_Path, USERNAME):
        self.__initialized = True
        self.__domain = DOMAIN
        self.__pem_location = PEM_LOCATION
        provisioner.Provisioner.__init__(self, Module_Path, PEM_LOCATION, USERNAME)
        network.Network.__init__(self, PEM_LOCATION)


    def ssh_connect(self, server):
        # self.__network.ssh_connect(server)
        super(AWS, self)._ssh_connect(server)


    def ping(self, server):
        # self.__network.ping(server)
        super(AWS, self)._ping(server)


    def provision(self, ymlfile):
        super(AWS, self)._provision(ymlfile)


    def retr_section(self):
        home = expanduser("~")
        for file in os.listdir("%s/.aws/" % home):
            if file == 'credentials':
                with open('%s/.aws/credentials' % home) as f:
                    cre_list = f.readlines()
                    sec_list = [item.strip('\n') for item in cre_list if '[' in item]
                    return str(sec_list)


    def retr_credential(self, section):
        home = expanduser("~")
        with open('%s/.aws/credentials' % home) as f:
            cre_list = f.readlines()
            i = [index for index in range(len(cre_list)) if section in cre_list[index]][0]
            access_id = cre_list[i + 1].split('=')[1].strip('\n')
            access_key = cre_list[i + 2].split('=')[1].strip('\n')
        return access_id, access_key


    def get_access(self, region, section):
        access_id = self.retr_credential(section)[0]
        access_key = self.retr_credential(section)[1]
        session = boto3.session.Session(aws_access_key_id=access_id, aws_secret_access_key=access_key)
        # client = boto3.client('ec2', region_name='ap-southeast-1', aws_access_key_id=AWS_ID, aws_secret_access_key=AWS_KEY)
        client = session.client('ec2', region_name=region)
        resource = session.resource('ec2', region_name=region)
        dns = session.client('route53', region_name=region)
        elb = session.client('elb', region_name=region)
        return client, resource, dns, elb


    def ip_validation(self, value):
        try:
            IP(value)
            return True
        except:
            return False


    def create_a_record(self, hostname, value, region, section):
        client = self.get_access(region, section)[2]
        try:
            response = client.change_resource_record_sets(
                HostedZoneId='Z3CKPSB9SW1K42',
                ChangeBatch={
                    'Comment': 'creat a test record',
                    'Changes': [
                        {
                            'Action': '%s' % "CREATE",
                            'ResourceRecordSet': {
                                'Name': "{0}.{1}".format(hostname, self.__domain),
                                'Type': 'CNAME',
                                'SetIdentifier': value,
                                'TTL': 60,
                                # 'GeoLocation': {'ContinentCode':'%s'%region},
                                'Region': region,
                                'ResourceRecords': [
                                    {
                                        'Value': '%s' % value
                                    },
                                ],
                            }
                        },
                    ]
                }
            )
            if response['ResponseMetadata']['HTTPStatusCode'] == 200:
                print("[*] {0}.{1}".format(hostname, self.__domain) + " is successfully created")
            else:
                print("Create record failed")
        except Exception as e:
            if "it already exists" in str(e):
                print("the record has already exist")




    def delete_a_record(self, hostedZoneId, action, hostname, region, value, section):
        client = self.get_access(region, section)[2]
        try:
            response = client.change_resource_record_sets(
                HostedZoneId=hostedZoneId,
                ChangeBatch={
                    'Comment': 'Delete a record',
                    'Changes': [
                        {
                            'Action': '%s' % action,
                            'ResourceRecordSet': {
                                'Name': '%s.%s' % (hostname, self.__domain),
                                'Type': 'A',
                                'SetIdentifier': 'test',
                                'TTL': 60,
                                # 'GeoLocation': {'ContinentCode':'%s'%region},
                                'ResourceRecords': [
                                    {
                                        'Value': '%s' % value
                                    },
                                ],
                            }
                        },
                    ]
                }
            )
            if response['ResponseMetadata']['HTTPStatusCode'] == 200:
                print('%s.%s' % (hostname, self.__domain) + " is successfully deleted")
        except Exception as e:
            if "not match" in str(e):
                print("Value provided mismatch")
            if "not found" in str(e):
                print ("record not found")


    def get_amis(self, region, section):
        amis_list = []
        resource = self.get_access(region, section)[1]
        for item in resource.images.filter(
                Filters=[{'Name': 'name', 'Values': ['ubuntu/images/hvm-ssd/ubuntu-xenial-16.04-amd64-server-*']},
                         {'Name': 'virtualization-type', 'Values': ['hvm']}]).all():
            amis_list.append(re.match(r".\w+\.\w+.\w+..(.*?)'", str(item)).group(1))
        return amis_list


    def choose_img_size(self):
        image_sizing = "t1.micro|'t2.nano'|'t2.micro'|'t2.small'|'t2.medium'|'t2.large'|'t2.xlarge'|'t2.2xlarge'|'m1.small'|'m1.medium'|'m1.large'|'m1.xlarge'|'m3.medium'|'m3.large'|'m3.xlarge'|'m3.2xlarge'|'m4.large'|'m4.xlarge'|'m4.2xlarge'|'m4.4xlarge'|'m4.10xlarge'|'m4.16xlarge'|'m2.xlarge'|'m2.2xlarge'|'m2.4xlarge'|'cr1.8xlarge'|'r3.large'|'r3.xlarge'|'r3.2xlarge'|'r3.4xlarge'|'r3.8xlarge'|'r4.large'|'r4.xlarge'|'r4.2xlarge'|'r4.4xlarge'|'r4.8xlarge'|'r4.16xlarge'|'x1.16xlarge'|'x1.32xlarge'|'x1e.xlarge'|'x1e.2xlarge'|'x1e.4xlarge'|'x1e.8xlarge'|'x1e.16xlarge'|'x1e.32xlarge'|'i2.xlarge'|'i2.2xlarge'|'i2.4xlarge'|'i2.8xlarge'|'i3.large'|'i3.xlarge'|'i3.2xlarge'|'i3.4xlarge'|'i3.8xlarge'|'i3.16xlarge'|'hi1.4xlarge'|'hs1.8xlarge'|'c1.medium'|'c1.xlarge'|'c3.large'|'c3.xlarge'|'c3.2xlarge'|'c3.4xlarge'|'c3.8xlarge'|'c4.large'|'c4.xlarge'|'c4.2xlarge'|'c4.4xlarge'|'c4.8xlarge'|'c5.large'|'c5.xlarge'|'c5.2xlarge'|'c5.4xlarge'|'c5.9xlarge'|'c5.18xlarge'|'cc1.4xlarge'|'cc2.8xlarge'|'g2.2xlarge'|'g2.8xlarge'|'g3.4xlarge'|'g3.8xlarge'|'g3.16xlarge'|'cg1.4xlarge'|'p2.xlarge'|'p2.8xlarge'|'p2.16xlarge'|'p3.2xlarge'|'p3.8xlarge'|'p3.16xlarge'|'d2.xlarge'|'d2.2xlarge'|'d2.4xlarge'|'d2.8xlarge'|'f1.2xlarge'|'f1.16xlarge'|'m5.large'|'m5.xlarge'|'m5.2xlarge'|'m5.4xlarge'|'m5.12xlarge'|'m5.24xlarge'|'h1.2xlarge'|'h1.4xlarge'|'h1.8xlarge'|'h1.16xlarge"
        base_sizes = []
        image_options = []
        for sizing in image_sizing.split("|"):
            image_size = sizing.strip('\'')[0:2]
            base_sizes.append(image_size)
        print(list(set(base_sizes)))
        usr_input_base_size = input('[*] Pls choose the base image: ')
        for item in image_sizing.split("|"):
            item = item.strip('\'')
            if usr_input_base_size in item:
                image_options.append(item)
        print(image_options)
        img = input('[*] Choose the wanted image size: ')
        return img


    def get_initizing_serverlist(self, region, server_type, vpcid, section):
        home = os.path.expanduser("~")
        file = "%s/inventory" % home
        server_list = []
        client = self.get_access(region, section)[0]
        request = client.describe_instances(Filters=[
            {
                'Name': 'vpc-id',
                'Values': [
                    vpcid,
                ]
            },
        ], )
        # print request
        reservation = request[u'Reservations']
        metadata = request[u'ResponseMetadata']
        if metadata['HTTPStatusCode'] == 200:
            for item in reservation:
                with open(file, 'w+') as f:
                    f.writelines('[servers]\n')
                    for server in item['Instances']:
                        if server['State']['Name'] != 'running' and server['State']['Name'] != 'terminated' and \
                                server['State']['Name'] != 'stopped':
                            if server['PublicDnsName'] != "":
                                if server_type == 'db':
                                    server_list.append(server['PublicDnsName'])
                                    print("[*] Written %s to hosts file for Ansible to use" % server['PublicDnsName'])
                                    f.writelines('{0}\n'.format(server['PublicDnsName']))
                                if server_type == 'web':
                                    server_list.append(server['PublicDnsName'])
                                    print("[*] Written %s to hosts file for Ansible to use" % server['PublicDnsName'])
                                    f.writelines('{0}\n'.format(server['PublicDnsName']))
                            elif server['PrivateDnsName'] != "":
                                server_list.append(server['PrivateDnsName'])
        return server_list


    def get_region(self, section):
        access_id = self.retr_credential(section)[0]
        access_key = self.retr_credential(section)[1]
        client = boto3.client('ec2', aws_access_key_id=access_id, aws_secret_access_key=access_key)
        regions = [region['RegionName'] for region in client.describe_regions()['Regions']]
        return regions


    def get_vpc_subnets(self, region, section):
        a = {}
        ec2 = self.get_access(region, section)[1]
        for vpc in ec2.vpcs.all():
            # print vpc
            for az in ec2.meta.client.describe_availability_zones()["AvailabilityZones"]:
                for subnet in vpc.subnets.filter(Filters=[{"Name": "availabilityZone", "Values": [az["ZoneName"]]}]):
                    # z = (vpc, az["ZoneName"], "filter:", subnet)
                    vpc_raw = re.match(r".\w+\.\w+.\w+='(.*?)'", str(vpc))
                    vpc_id = vpc_raw.groups(1)
                    vpc_id = str(str(vpc_id).strip('()')[:-1]).strip("'")
                    subnet_raw = re.match(r".\w+\.\w+.\w+='(.*?)'", str(subnet))
                    subnet_id = subnet_raw.group(1)
                    a.setdefault(vpc_id, [])
                    a[vpc_id].append(subnet_id)
        return a


    def get_vpcid(self, region, subnet_id, section):
        ec2 = self.get_access(region, section)[0]
        response = ec2.describe_subnets(
            SubnetIds=[
                subnet_id,
            ],
            DryRun=False
        )
        result = response['Subnets']
        for item in result:
            return item['VpcId']


    def get_security_group(self, region, vpcid, section):
        srcgroups_dict = {}
        srcgroups_list = []
        ec2 = self.get_access(region, section)[0]
        # print ec2.describe_security_groups()['SecurityGroups'][1]
        # print len(ec2.describe_security_groups(Filters=[{"Name": "vpc-id", "Values": [vpcid]}])['SecurityGroups'])
        if len(ec2.describe_security_groups(Filters=[{"Name": "vpc-id", "Values": [vpcid]}])['SecurityGroups']) > 1:
            for i in range(0, len(
                    ec2.describe_security_groups(Filters=[{"Name": "vpc-id", "Values": [vpcid]}])['SecurityGroups'])):
                securitygroups = ec2.describe_security_groups(Filters=[
                    {
                        'Name': 'vpc-id',
                        'Values': [
                            vpcid,
                        ]
                    },
                ], )['SecurityGroups'][i]
                if securitygroups['GroupName'] != 'default':
                    sec_group = PrettyTable(['Direction', 'Subnets', 'Port', 'Protocol'])
                    grpname = securitygroups['GroupName']
                    grpid = securitygroups['GroupId']
                    srcgroups_list.append(grpname)
                    srcgroups_dict[grpname] = grpid
                    # print "[*] Print Outgoing Rule for %s, the Group ID is %s"%(grpname, grpid)
                    # for group in securitygroups['IpPermissionsEgress']:
                    # print group
                    # print "[*] Print Incoming Rule for %s, the Group ID is %s"%(grpname, grpid)
                    # for group in securitygroups['IpPermissions']:
                    # print group
                    for item in securitygroups['IpPermissionsEgress']:
                        if "FromPort" in item:
                            for cidr in item['IpRanges']:
                                sec_group.add_row(['Outgoing', cidr['CidrIp'], item['FromPort'], item['IpProtocol']])
                    for item in securitygroups['IpPermissions']:
                        if "ToPort" in item:
                            for cidr in item['IpRanges']:
                                sec_group.add_row(['Incoming', cidr['CidrIp'], item['ToPort'], item['IpProtocol']])
                    print("[*] Firewall rules for %s " % grpname)
                    print(sec_group)
                i += 1
            # print "[*] Pls chose the correct Group ID %s"%str(srcgroups_list)
            print(srcgroups_dict)
            return srcgroups_dict
        else:
            print("[*] There is no security group, Pls create a new security group. ")
            groupname = input('[*] Pls key-in the security groupname: ')
            response = ec2.create_security_group(
                Description='test',
                GroupName=groupname,
                VpcId=vpcid,
                DryRun=False
            )
            for i in range(0, len(
                    ec2.describe_security_groups(Filters=[{"Name": "vpc-id", "Values": [vpcid]}])['SecurityGroups'])):
                securitygroups = ec2.describe_security_groups(Filters=[
                    {
                        'Name': 'vpc-id',
                        'Values': [
                            vpcid,
                        ]
                    },
                ], )['SecurityGroups'][i]
                print(securitygroups)
                if securitygroups['GroupName'] != 'default':
                    sec_group = PrettyTable(['Direction', 'Subnets', 'Port', 'Protocol'])
                    grpname = securitygroups['GroupName']
                    grpid = securitygroups['GroupId']
                    srcgroups_list.append(grpname)
                    srcgroups_dict[grpname] = grpid
                    # print "[*] Print Outgoing Rule for %s, the Group ID is %s"%(grpname, grpid)
                    # for group in securitygroups['IpPermissionsEgress']:
                    # print group
                    # print "[*] Print Incoming Rule for %s, the Group ID is %s"%(grpname, grpid)
                    # for group in securitygroups['IpPermissions']:
                    # print group
                    for item in securitygroups['IpPermissionsEgress']:
                        if "FromPort" in item:
                            for cidr in item['IpRanges']:
                                sec_group.add_row(['Outgoing', cidr['CidrIp'], item['FromPort'], item['IpProtocol']])
                    for item in securitygroups['IpPermissions']:
                        if "ToPort" in item:
                            for cidr in item['IpRanges']:
                                sec_group.add_row(['Incoming', cidr['CidrIp'], item['ToPort'], item['IpProtocol']])
                    print("[*] Firewall rules for %s " % grpname)
                    print(sec_group)
                i += 1
            # print "[*] Pls chose the correct Group ID %s"%str(srcgroups_list)
            print(srcgroups_dict)
            return srcgroups_dict


    def security_group_rules(self, region, secgrp_id, section):
        ec2 = self.get_access(region, section)[1]
        security_group = ec2.SecurityGroup(secgrp_id)
        print(security_group)
        secgrp_chg_input_outbound = input("[*] Do you need to modify outbound rule? yes or no? ")
        if "yes" in secgrp_chg_input_outbound:
            num_of_outbound_rules = int(input("[*] Number of the outbound rules?"))
            for rule in range(0, (num_of_outbound_rules)):
                protocol = input('[*] Key-in the protocol, tcp or udp: ')
                cidrip = input('[*] Key-in outbound Destination IP Prefixes, eg, 0.0.0.0/0: ')
                fromport = int(input('[*] Key-in the source port number: '))
                toport = int(input('[*] Key-in the destination port number: '))
                try:
                    response = security_group.authorize_egress(
                        DryRun=False,
                        IpPermissions=[
                            {
                                'FromPort': fromport,
                                'IpProtocol': protocol,
                                'IpRanges': [
                                    {
                                        'CidrIp': cidrip,
                                        'Description': 'test'
                                    },
                                ],
                                'ToPort': toport,
                            },
                        ],
                    )
                    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
                        print('[*] Rule Added')
                except:
                    print("[*] Outbound rule injected failed")
            else:
                pass
        else:
            pass
        secgrp_chg_input_inbound = input("[*] Do you need to modify inbound rule? yes or no? ")
        if "yes" in secgrp_chg_input_inbound:
            num_of_inbound_rules = int(input("[*] Number of the inbound rules?"))
            for rule in range(0, (num_of_inbound_rules)):
                protocol = input('[*] Key-in the protocol, tcp or udp: ')
                cidrip = input('[*] Key-in outbound Destination IP Prefixes, eg, 0.0.0.0/0: ')
                fromport = int(input('[*] Key-in the source port number: '))
                toport = int(input('[*] Key-in the destination port number: '))
                try:
                    response = security_group.authorize_ingress(
                        DryRun=False,
                        IpPermissions=[
                            {
                                'FromPort': fromport,
                                'IpProtocol': protocol,
                                'IpRanges': [
                                    {
                                        'CidrIp': cidrip,
                                        'Description': 'test'
                                    },
                                ],
                                'ToPort': toport,
                            },
                        ],
                    )
                    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
                        print('[*] Rule Added')
                except:
                    print("[*] Inbound rule injected failed")
            else:
                pass
        else:
            pass


    def get_key(self, region, section):
        key_list = []
        ec2 = self.get_access(region, section)[0]
        response = ec2.describe_key_pairs()
        for keypair in response['KeyPairs']:
            key_list.append(keypair['KeyName'])
        print(key_list)


    def create_instance(self, count, region, server_type, subnetid, secgrp, imageid, vpcid, keyname, section):
        # image_list = get_amis(region)
        # imageid = 'ami-68097514'
        img = self.choose_img_size()
        client = self.get_access(region, section)[1]
        # print client.get_caller_identity()['Account']
        client.create_instances(ImageId=imageid, MinCount=1, MaxCount=count, KeyName=keyname, SubnetId=subnetid,
                                InstanceType=img, SecurityGroupIds=[secgrp])
        print('[*] Creating Instances, Pls wait....')
        time.sleep(1)
        print("[*] Getting the Instance List")
        servers = self.get_initizing_serverlist(region, server_type, vpcid, section)
        time.sleep(2)
        print("[*] Created %d servers are %s" % (len(servers), servers))
        return servers


    def create_cname(self, region, servers, section):
        for server in servers:
            print("[*] Assign Alias for %s" % server)
            alias_cname = input('[*] Key-in the CNAME: ')
            try:
                print ("[*] Route53 API Connected, Creating Alias.")
                self.create_a_record(alias_cname, server, region, section)
            except:
                print ("[ERROR] API Connection failed ")

    def srv_post_test(self, servers):
        for server in servers:
            if socket.gethostbyname(server):
                connected = False
                while connected == False:
                    if self._ping(server) == True:
                        print("[*] Trying to SSH to the server %s" % server)
                        time.sleep(30)
                        try:
                            if self._ssh_connect(server) == True:
                                print("[*] Host %s is connected" % server)
                                connected = True
                                return True
                        except Exception as e:
                            print("[*] The servers are still booting, i will try again")
                            time.sleep(15)
                            continue
                    else:
                        continue
            else:
                print ('[*] The server %s is not public resolvable.' % server)


    def main(self):
        print(self.retr_section())
        section = input('[*] Pls input the authentication section for this task: ')
        try:
            print("[*] Retrieving Region Lists")
            # region_invalid_input = True
            region_list = self.get_region(section)
            region_ref = PrettyTable(['Region_List'])
            for region in region_list:
                region_ref.add_row([region])
            region = input("%s\n[*] Choose the region from the table Above: " % region_ref).lower()
            try:
                try:
                    subnet_ref = self.get_vpc_subnets(region, section)
                    if subnet_ref != "":
                        count = input("[*] How Many instances You like to provision, maximum 5: ")
                        try:
                            print(self.get_amis(region, section))
                            imageid = input("[*] Pls the close the image to boot from: ")
                            server_type = input("[*] Key-in the server type, web or db: ")
                            subnet_id = input('%s\n[*] Pls select the subnet: ' % subnet_ref).lower()
                            try:
                                # print self.get_vpc_subnets(region)
                                vpcid = self.get_vpcid(region, subnet_id, section)
                                group_dict = self.get_security_group(region, vpcid, section)
                                try:
                                    secgrp_name = input("[*] Pls In-put the Security Group: ")
                                    secgrp = group_dict[secgrp_name]
                                    rule_change = input('[*] Do you want to change the rules? yes or no? ')
                                    if 'yes' in rule_change:
                                        self.security_group_rules(region, secgrp, section)
                                    else:
                                        pass
                                    try:
                                        self.get_key(region, section)
                                        keyname = input("[*] Pls select the keypair: ")
                                        #keyname = 'singtel'
                                        try:
                                            self.create_instance(int(count), region, server_type, subnet_id, secgrp,
                                                                 imageid, vpcid, keyname, section)
                                            time.sleep(2)
                                            servers = self.get_initizing_serverlist(region, server_type, vpcid, section)
                                            try:
                                                srv_post_test_input = input(
                                                    "[*] Do you want to test the access to the VM? yes or no?: ")
                                                if 'yes' in srv_post_test_input:
                                                    self.srv_post_test(servers)
                                                else:
                                                    print("%s Provision Done" % servers)
                                                dns_user_input = input(
                                                    "[*] Do you want create DNS Alias? yes or no?: ")
                                                if dns_user_input == "yes":
                                                    try:
                                                        self.create_cname(region, servers, section)
                                                    except:
                                                        print("Assign CNAME Failed")
                                                else:
                                                    pass
                                                provision = input(
                                                    '[*] Do you want to provision the server? yes or no? ')
                                                if 'yes' in provision:
                                                    if self.srv_post_test(servers):
                                                        self._provision('/etc/ansible/test.yml')
                                                    else:
                                                        print("Test Failed")
                                            except:
                                                print("[*] Addtional Services Failed")
                                        except Exception as e:
                                            print(e)
                                            print("Initiate instance failed")
                                    except:
                                        print("[*] Failed to Retrieve the key")
                                except:
                                    print("[*] Failed to retrieve the security group")
                            except Exception as e:
                                print("[*] Retrieve Security Group List failed")
                        except Exception as e:
                            print("[*] Retrieve AMI list failed")
                    else:
                        print("[Error] No VPC available in this Region")
                except Exception as e:
                    print(e)
            except Exception as e:
                print("[Error] Retrieving Subnets Failed")
        except:
            print("[Error] Retrieving Regions Failed")
