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
    args = parser.get_args()
    si = service_instance.connect(args)

    VM = None
    content = si.RetrieveContent()
    VM = pchelper.get_obj(content, [vim.VirtualMachine], vm_name)

    if VM is None:
        raise SystemExit("Unable to locate VirtualMachine.")


    if VM.runtime.powerState == "poweredOff":
        VM.UnregisterVM()


def main():
    # Read the VM names from hosts file
    with open("vm_list", "r") as file:
        file_content = file.read()
    vms = file_content.split('\n')

    with ThreadPoolExecutor(max_workers=10) as executor:
        processes = [executor.submit(unregister, vm.strip()) for vm in vms if not vm.startswith('#')]
    count = 0
    for task in as_completed(processes):
        if task.done() == True:
            count += 1
    print(f"\n\n\nUnregister process completed: {count}")
    

if __name__ == '__main__':
    main()