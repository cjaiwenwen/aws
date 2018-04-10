This is an aws provisioning tool.

How to use it

Install pip install aws

import aws

myaws = aws.AWS("AWS_ID",
        "AWS_KEY",
        "ROUTE53_Domain",
        "VM Access KEY full path")

myaws.main()




