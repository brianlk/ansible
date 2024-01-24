#!/usr/bin/env python
#
# Written by Brian Leung
#
# Example script to shut down VMs

from datacenter import run_cli, read_vm_list
from tools import cli, service_instance, tasks, pchelper
from pyVmomi import vim
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Union

import time


def main():
    args = run_cli(cli.Argument.DATACENTER_NAME)
    si = service_instance.connect(args)
    content = si.RetrieveContent()
    DATACENTER = pchelper.get_obj(content, [vim.Datacenter], args.datacenter_name)
    abc1 = pchelper.get_obj(content, [vim.VirtualMachine], "abc1")
    print(abc1.config)
    # xxx = vim.vm.ConfigSpec()
    # xxx.memoryMB = 1000
    # xxx.annotation = "Sample"
    # xxx.guestId = "otherGuest"
    # xxx.name = "abc1"
    # xxx.numCPUs = 1
    # print(xxx)
    

if __name__ == '__main__':
    main()