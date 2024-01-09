#!/usr/bin/env python
#
# Written by Brian Leung
#
# Example script to power off VMs

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
    esx_host = pchelper.get_obj(content, [vim.HostSystem], "10.1.5.3")
    print(esx_host)
    folder = si.content.searchIndex.FindByInventoryPath("Datacenter/vm/Brian/")
    print(dir(folder))
    task = folder.RegisterVM_Task(path="[V7000F_Temp] VMware-vCenter-Server-Appliance-6.7.0.12000-8832884_OVF10/VMware-vCenter-Server-Appliance-6.7.0.12000-8832884_OVF10.vmx", 
                                  name="new vm name", asTemplate=False, pool=None, host=esx_host)




def main():
    # Read the VM names from hosts file
    with open("vm_list", "r") as file:
        file_content = file.read()
    vms = file_content.split('\n')

    with ThreadPoolExecutor(max_workers=10) as executor:
        processes = [executor.submit(shut_down, vm.strip()) for vm in vms]
    count = 0
    for task in as_completed(processes):
        print(task.done())
    

if __name__ == '__main__':
    main()