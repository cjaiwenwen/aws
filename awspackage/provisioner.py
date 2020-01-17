#!/usr/bin/env python


import shutil
from collections import namedtuple
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.inventory.manager import InventoryManager
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager
import ansible.constants as C
from ansible.plugins.callback import CallbackBase
from ansible import context
import yaml
import glob
from os.path import expanduser
import os
import json
from ansible.module_utils.common.collections import ImmutableDict


class ResultCallback(CallbackBase):
    """A sample callback plugin used for performing an action as results come in

    If you want to collect all results into a single object for processing at
    the end of the execution, look into utilizing the ``json`` callback plugin
    or writing your own custom callback plugin
    """
    def v2_runner_on_ok(self, result, **kwargs):
        """Print a json representation of the result

        This method could store the result in an instance attribute for retrieval later
        """
        host = result._host
        print(json.dumps({host.name: result._result}, indent=4))


class Provisioner(object):

    def __init__(self, Module_Path, PEM_LOCATION):
        self.__module_path = Module_Path
        self.__inventory = "%s/inventory" % expanduser("~")
        self.__pem_location = PEM_LOCATION


    def _list_roles(self, role_dir):
        roles_lst = []
        roles = os.listdir(role_dir)
        for role in roles:
            roles_lst.append(role)
        return roles_lst


    def _provision(self, yaml_file):
        context.CLIARGS = ImmutableDict(remote_user='ubuntu', connection='ssh', module_path=[self.__module_path], forks=10, become='yes', verbosity=10,
                                        become_method='sudo', become_user='root', check=False, diff=False, private_key_file='/Users/cjaiwenwen/Downloads/jun.pem', ansible_python_interpreter='/usr/local/Cellar/python3/3.7.5/bin/python3')

        # initialize needed objects
        loader = DataLoader() # Takes care of finding and reading yaml, json and ini files

        #passwords = dict(password=secret)

        inventory = InventoryManager(loader=loader, sources=self.__inventory)

        variable_manager = VariableManager(loader=loader, inventory=inventory)

        results_callback = ResultCallback()
        configs = map(lambda x: yaml.load_all(open(x)), glob.glob(yaml_file))
        for config in configs:
            for item in config:
                play_source = item[0]
                play = Play().load(play_source, variable_manager=variable_manager, loader=loader)
                tqm = None
                try:
                    tqm = TaskQueueManager(
                              inventory=inventory,
                              variable_manager=variable_manager,
                              loader=loader,
                              passwords=None,
                              #stdout_callback=ResultCallback(),  # Use our custom callback instead of the ``default`` callback plugin, which prints to stdout
                          )
                    tqm.run(play) # most interesting data for a play is actually sent to the callback's methods

                except Exception as e:
                    print(e)
                finally:
                    # we always need to cleanup child procs and the structres we use to communicate with them
                    if tqm is not None:
                        tqm.cleanup()
                        shutil.rmtree(C.DEFAULT_LOCAL_TMP, True)
