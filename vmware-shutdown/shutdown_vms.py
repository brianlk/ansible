#!/usr/bin/env python
#
# Written by Brian Leung
#
# Example script to shut down VMs

from datacenter import run_cli, read_vm_list
from tools import cli, service_instance, tasks, pchelper
from pyVmomi import vim
from concurrent.futures import ThreadPoolExecutor, as_completed

import time


MAX_WORKERS_NUM = 10


def shut_down(content, DATACENTER, vm_name):
    # args = run_cli(cli.Argument.DATACENTER_NAME)
    # si = service_instance.connect(args)
    # content = si.RetrieveContent()
    # DATACENTER = pchelper.get_obj(content, [vim.Datacenter], args.datacenter_name)
    dc_all_vm = None
    try:
        dc_all_vm = pchelper.get_all_obj(content, [vim.VirtualMachine], DATACENTER.vmFolder)
    except:
        pass
    
    if not dc_all_vm:
        return False
    
    for key, value in dc_all_vm.items():
        if key.runtime.powerState != "poweredOff" and value == vm_name:
            try:
                print(f"Shutting down: {value}")
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
    args = run_cli(cli.Argument.DATACENTER_NAME)
    si = service_instance.connect(args)
    content = si.RetrieveContent()
    DATACENTER = pchelper.get_obj(content, [vim.Datacenter], args.datacenter_name)
    VM_LIST = read_vm_list()
    count = 0
    # Parallel shutdown the VMs
    with ThreadPoolExecutor(max_workers=MAX_WORKERS_NUM) as executor:
        results = [executor.submit(shut_down, content, DATACENTER, vm.strip()) for vm in VM_LIST if not vm.startswith('#')]
        for result in as_completed(results):
            if result._result:
                count += 1
    print(f"\n{count} VMs are powered off.")
    

if __name__ == '__main__':
    main()