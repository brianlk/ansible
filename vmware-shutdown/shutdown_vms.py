#!/usr/bin/env python
#
# Written by Brian Leung
#
# Example script to shut down VMs

from tools import cli, service_instance, tasks, pchelper
from pyVmomi import vim

from concurrent.futures import ThreadPoolExecutor, as_completed

import time

def shut_down(vm_name, ans = 'n'):
    parser = cli.Parser()
    args = parser.get_args()
    si = service_instance.connect(args)

    VM = None
    content = si.RetrieveContent()
    VM = pchelper.get_obj(content, [vim.VirtualMachine], vm_name)

    if VM is None:
        raise SystemExit("Unable to locate VirtualMachine.")

    while VM.runtime.powerState != "poweredOff":
        try:
            VM.ShutdownGuest()
        except:
            TASK = VM.PowerOffVM_Task()
            tasks.wait_for_tasks(si, [TASK])
        finally:
            print(f"Shutting down: {vm_name}")
            time.sleep(5)
    print(f"{vm_name} is in {VM.runtime.powerState}")
    return True
    

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
    print(f"\n\n{count} VMs are powered off.")
    

if __name__ == '__main__':
    main()