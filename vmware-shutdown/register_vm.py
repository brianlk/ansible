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
    parser = cli.Parser()
    args = parser.get_args()
    si = service_instance.connect(args)
    content = si.RetrieveContent()

    obj_view = content.viewManager.CreateContainerView(content.rootFolder, [vim.Folder], True)
    folder_list = obj_view.view
    xxx = None
    for folder in folder_list:
        if folder.name == "vm":
            xxx = folder

    esx_host = pchelper.get_obj(content, [vim.HostSystem], "10.1.23.100")
    view_manager = content.viewManager
    datacenter = content.rootFolder.childEntity[0]
    container_view = view_manager.CreateContainerView(datacenter, [vim.ResourcePool], True)
    for resource_pool in container_view.view:
        largest_rp = resource_pool
    # task = xxx.RegisterVM_Task(path="[san-1] abc1/abc1.vmx", name="abc1", asTemplate=False, pool=largest_rp, host=esx_host)
    # vm = pchelper.get_obj(content, [vim.VirtualMachine], "abc1")
    # print(vm.config)
    # aaa = pchelper.get_obj(content, [vim.vm.GuestInfo], "abc1")
    container = content.viewManager.CreateContainerView(
        content.rootFolder, [vim.VirtualMachine], True
    )
    for c in container.view:
        print(c.summary.runtime)
    

if __name__ == '__main__':
    main()