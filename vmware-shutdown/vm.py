#!/usr/bin/env python
#
# Written by Brian Leung
#
# Example script to shut down VMs

from datacenter import run_cli, read_vm_list, read_result_json
from tools import cli, service_instance, tasks, pchelper
from pyVmomi import vim
from concurrent.futures import ThreadPoolExecutor, as_completed

import time


MAX_WORKERS_NUM = 10


def power_on(vm_name, si, datacenter_name):
    content = si.RetrieveContent()
    DATACENTER = pchelper.get_obj(content, [vim.Datacenter], datacenter_name)
    dc_all_vm = None
    try:
        dc_all_vm = pchelper.get_all_obj(content, [vim.VirtualMachine], DATACENTER.vmFolder)
    except:
        pass

    if not dc_all_vm:
        return False
    
    count = 0
    for key, value in dc_all_vm.items():
        # if key.runtime.powerState == "poweredOff" and value == vm_name:
        if value == vm_name:
            # try:
            print(f"Powering on: {value}")
            esx_host = pchelper.get_obj(content, [vim.HostSystem], 
                                        key.summary.runtime.host.name)
            count += 1
            raise Exception("")
            # task = key.PowerOnVM_Task(esx_host)
            # tasks.wait_for_tasks(si, [task])
            # except:
            #     print(f"Error: failed to power on {vm_name}")

    
    return count
        

def shut_down(vm_name, si, datacenter_name):
    content = si.RetrieveContent()
    DATACENTER = pchelper.get_obj(content, [vim.Datacenter], datacenter_name)
    dc_all_vm = None
    try:
        dc_all_vm = pchelper.get_all_obj(content, [vim.VirtualMachine], DATACENTER.vmFolder)
    except:
        pass
    
    if not dc_all_vm:
        return False
        
    count = 0
    for key, value in dc_all_vm.items():
        if key.runtime.powerState != "poweredOff" and value == vm_name:
            try:
                print(f"Shutting down: {value}")
                count += 1
                task = key.ShutdownGuest()
                tasks.wait_for_tasks(si, [task])
            except:
                key.PowerOffVM_Task()
    
    return count


def start_workers(action, si, args):
    count = 0
    VM_LIST = read_vm_list()
    # Parallel shutdown the VMs
    with ThreadPoolExecutor(max_workers=MAX_WORKERS_NUM) as executor:
        results = [executor.submit(action, vm.strip(), si, args.datacenter_name) 
                   for vm in VM_LIST if vm and not vm.startswith('#')]
        for result in as_completed(results):
            print(vars(result))
            if result._result:
                count += result._result
    print(f"\n{count} VMs are powered {args.power}.")
    

def main():
    args = run_cli(cli.Argument.DATACENTER_NAME, cli.Argument.POWER)
    si = service_instance.connect(args)
    if args.power == "on":
        start_workers(power_on, si, args)
    else:
        start_workers(shut_down, si, args)
    

if __name__ == '__main__':
    main()