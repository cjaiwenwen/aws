# Project Title

This project this target to automate the AWS provisioning process for ec2 and route53

### Prerequisites

This code is tested with python2.7.14, addtional modules (prettytable, boto3, paramiko) are required which will be installed automaticlly.


### Installing

sudo pip install git+git://github.com/cjaiwenwen/aws.git#egg=aws-0.1-py2.7.egg

## How to use it

from awspackage import aws

myaws = aws.AWS("AWS_ID",
        	"AWS_KEY",
        	"ROUTE53_Domain",
        	"VM Access KEY full path")

myaws.main()

AWS_ID refer to the AWS console ID
AWS_KEY refer to the aws console secrect key
ROUTE53_Domain refer to the domain name that registered to the AWS under the same account, eg. cjaiwenwen.com
VM ACCESS KEY full path refer to the local pem key path eg, /Users/cjaiwenwen/Desktop/chenjun.pem 

## Authors

* **Chen Jun** - *Initial work* - [CJAIWENWEN](https://github.com/cjaiwenwen)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details






