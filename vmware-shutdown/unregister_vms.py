#!/usr/bin/env python
#
# Written by Brian Leung
#
# Example script to unregister VMs

from tools import cli, service_instance, tasks, pchelper
from get_all_vm_names import get_vms_in_dc
from pyVmomi import vim
from datacenter import check_vm_in_dc
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
        VM = pchelper.get_obj(content, [vim.VirtualMachine], vm_name, DATACENTER.vmFolder)
    except:
        pass

    if VM is None:
        return False
    # if not check_vm_in_dc(content, args.datacenter_name, VM.config.uuid):
    #     return False

    if VM.runtime.powerState == "poweredOff":
        VM.UnregisterVM()
        print(f"{vm_name} is unregistered.")
        return True


def main():
    if len(get_vms_in_dc()) > 0:
        raise Exception("Duplicaed VM name in VCenter.")
    # Read the VM names from hosts file
    with open("vm_list", "r") as file:
        file_content = file.read()
    vms = file_content.split('\n')

    count = 0
    with ThreadPoolExecutor(max_workers=10) as executor:
        processes = [executor.submit(unregister, vm.strip()) for vm in vms if not vm.startswith('#')]
        for result in as_completed(processes):
            if result._result:
                count += 1
    print(f"\n{count} VMs are unregistered.")
    

if __name__ == '__main__':
    main()