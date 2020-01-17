try:
    from setuptools import setup, find_packages

except ImportError:

    from distutils.core import setup, find_packages

setup(
    name='aws_toolkit',
    version='1.0.1',
    packages=find_packages(exclude=['tests*']),
    license='MIT',
    description='An AWS Provisioning Tool',
    long_description=open('README.md').read(),
    install_requires=['IPy','boto3','paramiko','prettytable'],
    url='https://github.com/cjaiwenwen/aws',
    author='Chen Jun',
    author_email='cjaiwenwen@gmail.com'
)
