#!/usr/bin/env python
#
# Written by Brian Leung
#
# Example script to unregister VMs

from tools import cli, service_instance, tasks, pchelper
from pyVmomi import vim
from concurrent.futures import ThreadPoolExecutor, as_completed

import time

def unregister(vm_name):
    parser = cli.Parser()
    parser.add_required_arguments(cli.Argument.DATACENTER_NAME)
    args = parser.get_args()
    si = service_instance.connect(args)
    content = si.RetrieveContent()
    DATACENTER = pchelper.get_obj(content, [vim.Datacenter], args.datacenter_name)
    VM = None
    try:
        VM = pchelper.get_all_obj(content, [vim.VirtualMachine], DATACENTER.vmFolder)
    except:
        pass

    if not VM:
        return False

    for key, value in VM.items():
        if key.runtime.powerState == "poweredOff" and value == vm_name:
            # key.UnregisterVM()
            print(f"{vm_name} is unregistered.")
            return True
    return False


def main():
    # Read the VM names from hosts file
    with open("vm_list", "r") as file:
        file_content = file.read()
    vms = file_content.split('\n')

    count = 0
    for vm in vms:
        if unregister(vm):
            count += 1
    print(f"\n{count} VMs are unregistered.")
    

if __name__ == '__main__':
    main()