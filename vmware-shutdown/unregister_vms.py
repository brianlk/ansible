#!/usr/bin/env python
#
# Written by Brian Leung
#
# Example script to unregister VMs

from tools import cli, service_instance, tasks, pchelper
from pyVmomi import vim
from concurrent.futures import ThreadPoolExecutor, as_completed
from datacenter import vm_config_backup, read_vm_list

import time

def unregister(vm_name, all_vms):
    if not all_vms:
        return False

    for key, value in all_vms.items():
        if key.runtime.powerState == "poweredOff" and value == vm_name:
            key.UnregisterVM()
            print(f"{vm_name} is unregistered.")
            return True
    return False


def main():
    parser = cli.Parser()
    parser.add_required_arguments(cli.Argument.DATACENTER_NAME)
    args = parser.get_args()
    si = service_instance.connect(args)
    # backup is used by registration process later
    vm_config_backup(si, args.datacenter_name)
    content = si.RetrieveContent()
    DATACENTER = pchelper.get_obj(content, [vim.Datacenter], args.datacenter_name)
    # Read the VM names from vm_list file
    vms = read_vm_list()

    count = 0
    for vm in vms:
        if unregister(vm, pchelper.get_all_obj(content, [vim.VirtualMachine], DATACENTER.vmFolder)):
            count += 1
    print(f"\n{count} VMs are unregistered.")
    

if __name__ == '__main__':
    main()