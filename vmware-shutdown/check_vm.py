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
    task = folder.RegisterVM_Task(path="[san-1] abc1/abc1.vmx", 
                                  name="new vm name", asTemplate=False, pool=None, host=esx_host)




def main():
    # Read the VM names from hosts file
    # with open("vm_list", "r") as file:
    #     file_content = file.read()
    # vms = file_content.split('\n')

    # with ThreadPoolExecutor(max_workers=10) as executor:
    #     processes = [executor.submit(shut_down, vm.strip()) for vm in vms]
    # count = 0
    # for task in as_completed(processes):
    #     print(task.done())
    parser = cli.Parser()
    args = parser.get_args()
    si = service_instance.connect(args)
    content = si.RetrieveContent()
    esx_host = pchelper.get_obj(content, [vim.HostSystem], "10.1.23.100")
    # print(esx_host)
    # rp = pchelper.search_for_obj(content, [vim.ResourcePool], "resgroup-8")
    # folder = content.searchIndex.FindByInventoryPath("/")
    # task = folder.RegisterVM_Task(path="[san-1] abc1/abc1.vmx", 
    #                               name="new vm name", asTemplate=False, pool=rp, host=esx_host)
    # view = pchelper.get_container_view(si, obj_type=[vim.ResourcePool])
    # print(view.type)
    datacenter = content.rootFolder.childEntity[0]
    view_manager = content.viewManager
    container_view = view_manager.CreateContainerView(datacenter, [vim.ResourcePool], True)
    largest_rp = None
    unreserved_for_vm = 0
    try:
        for resource_pool in container_view.view:
            if resource_pool.runtime.memory.unreservedForVm > unreserved_for_vm:
                largest_rp = resource_pool
                unreserved_for_vm = resource_pool.runtime.memory.unreservedForVm
    finally:
        container_view.Destroy()
    # content = si.RetrieveContent()
    # esx_host = pchelper.get_obj(content, [vim.HostSystem], "10.1.23.100")
    folder = pchelper.get_obj(content, [vim.Folder], "[san-1] abc1")
    # print(type(folder))
    task = folder.RegisterVM_Task(path="[san-1] abc1/abc1.vmx", 
                                    name="abc1", asTemplate=False, pool=largest_rp, host=esx_host)
    # datacenter = si.content.rootFolder.childEntity[0]
    # f = datacenter.vmFolder
    # print(type(f))

if __name__ == '__main__':
    main()