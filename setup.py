try:
    from setuptools import setup, find_packages

except ImportError:

    from distutils.core import setup, find_packages

setup(
    name='aws_toolkit',
    version='1.0.2',
    packages=find_packages(exclude=['tests*']),
    license='MIT',
    description='An AWS Provisioning Tool',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    install_requires=['IPy','boto3','paramiko','prettytable','Ansible'],
    url='https://github.com/cjaiwenwen/aws',
    author='Chen Jun',
    author_email='cjaiwenwen@gmail.com'
)
