# AWS Provisioning Tool

This project this target to automate the AWS provisioning process for ec2 and route53

### Prerequisites

This code is tested with python 2.7, addtional modules (IPy, prettytable, boto3, paramiko) are required which will be installed automaticlly.

Need to configure following at home directory.

#### For Linux and Mac.
```
~/.aws/config
~/.aws/credentials
```

#### For Windows.
```
"%UserProfile%"/.aws/config
"%UserProfile%"/.aws/credentials
```

#### config file details
```
[default]
region=ap-southeast-1
output=json
```
#### credentials file details
```
[account1]
aws_access_key_id=AKIAIOSFODNN7EXAMPLE
aws_secret_access_key=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY

[account2]
aws_access_key_id=AKIAIOSFODNN7TEST
aws_secret_access_key=wJalrXUtnFEMI/K7MDENG/bPxRfiCYTESTKEY
```

### Installing

* I have tested working on Mac and Linux

* sudo pip install aws_toolkit==1.0.2

## How to use it

```
from awspackage import aws

myaws = aws.AWS(DOMAIN="abc.com #Hosted at Route53",
        	PEM_LOCATION="/path/to/pem",
                Module_Path="/path/to/ansible/playbook",
                USERNAME="EC2_Username")

myaws.main()
```

## Parameters to take note

* "Domain" refer to the domain name that registered to the AWS under the same account, eg. cjaiwenwen.com (Put dummy data if you dont have route53 service)
* "PEM_LOCATION" refer to the local pem key path eg, /Users/cjaiwenwen/Desktop/chenjun.pem 
* "Module_Path" is exact location where the ansible yaml file is located, and the server is under [servers]
* "USERNAME" is the username to access the remote server 

## What can the library could achieve

* Could select the account to provision based on the section by select the account1 and account2
* Create instance on any region if the VPC has been already created
* Control the number of the VMs could provisioned
* Choose the AMI image
* Choose the subnets
* Choose the security group
* Modify the security group rules if need to be
* Choose the size of the VM
* Assign CNAME for the provisioned VM
* Continue ping the provisioned host
* SSH to the host to confirm accessible (need to add ssh incoming rule)
* Deploy

## Authors

* **Chen Jun** - *Initial work* - [CJAIWENWEN](https://github.com/cjaiwenwen)

## Connect with me on Linkedin

[Chen Jun](https://www.linkedin.com/in/cjaiwenwen/) 

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details






