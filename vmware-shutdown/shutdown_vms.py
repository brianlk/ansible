#!/usr/bin/env python
#
# Written by Brian Leung
#
# Example script to shut down VMs

from tools import cli, service_instance, tasks, pchelper
from pyVmomi import vim
from concurrent.futures import ThreadPoolExecutor, as_completed


import time


def shut_down(vm_name):
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
        if key.runtime.powerState != "poweredOff" and value == vm_name:
            try:
                task = key.ShutdownGuest()
                tasks.wait_for_tasks(si, [task])
            except:
                key.PowerOffVM_Task()
            finally:
                print(f"{value} is in {key.runtime.powerState}")
                return True
    return False
    

def main():
    # Read the VM names from hosts file
    with open("vm_list", "r") as file:
        file_content = file.read()
    vms = file_content.split('\n')
    count = 0

    with ThreadPoolExecutor(max_workers=10) as executor:
        results = [executor.submit(shut_down, vm.strip()) for vm in vms if not vm.startswith('#')]
        for result in as_completed(results):
            if result._result:
                count += 1
    print(f"\n{count} VMs are powered off.")
    

if __name__ == '__main__':
    main()