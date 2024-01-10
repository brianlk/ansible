#!/usr/bin/env python
#
# Written by Brian Leung
#
# Example script to shut down VMs

from tools import cli, service_instance, tasks, pchelper
from get_all_vm_names import get_vms_in_dc
from pyVmomi import vim

from concurrent.futures import ThreadPoolExecutor, as_completed

import time


def check_vm_in_dc(content, datacenter_name, uuid):
    DC = pchelper.get_obj(content, [vim.Datacenter], datacenter_name)
    SI = content.searchIndex.FindByUuid(DC, uuid, True)
    if isinstance(SI, vim.VirtualMachine):
        return True
    return False


def shut_down(vm_name, ans = 'n'):
    print("xxxxxxxxxxx")
    parser = cli.Parser()
    parser.add_required_arguments(cli.Argument.DATACENTER_NAME)
    args = parser.get_args()
    si = service_instance.connect(args)
    print("xxxxxxxxxxx")
    VM = None
    content = si.RetrieveContent()
    try:
        VM = pchelper.get_obj(content, [vim.VirtualMachine], vm_name)
    except:
        print("eeeeeeeeee")
    print("xxxxxxxxxxx")
    print(VM)
    if VM is None:
        raise SystemExit("Unable to locate VirtualMachine.")
    if not check_vm_in_dc(content, args.datacenter_name, VM.config.uuid):
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
    if len(get_vms_in_dc()) > 0:
        raise Exception("Duplicaed VM name in VCenter.")
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