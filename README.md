# AWS Provisioning Tool

This project this target to automate the AWS provisioning process for ec2 and route53

### Prerequisites

This code is tested with python2.7.14, addtional modules (prettytable, boto3, paramiko) are required which will be installed automaticlly.


### Installing

* I have only tested the installation on Mac

* I am still working on Windows, sorry new to packaging :(

* sudo pip install git+git://github.com/cjaiwenwen/aws.git#egg=aws-0.1-py2.7.egg


## How to use it

```
from awspackage import aws

myaws = aws.AWS("AWS_ID",
        	"AWS_KEY",
        	"ROUTE53_Domain",
        	"VM Access KEY full path")

myaws.main()

```

* AWS_ID refer to the AWS console ID
* AWS_KEY refer to the aws console secrect key
* ROUTE53_Domain refer to the domain name that registered to the AWS under the same account, eg. cjaiwenwen.com
* VM ACCESS KEY full path refer to the local pem key path eg, /Users/cjaiwenwen/Desktop/chenjun.pem 

## What can the library could achieve

* Create instance on any region if the VPC has been already created
* Control the number of the VMs could provisioned
* Choose the AMI image
* Choose the subnets
* Choose the security group
* Modify the security group rules if need to be
* Choose the size of the VM
* Assign CNAME for the provisioned VM

## Authors

* **Chen Jun** - *Initial work* - [CJAIWENWEN](https://github.com/cjaiwenwen)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details






