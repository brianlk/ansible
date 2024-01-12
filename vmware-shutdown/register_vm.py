#!/usr/bin/env python
#
# Written by Brian Leung
#
# Example script to power off VMs

from tools import cli, service_instance, tasks, pchelper
from pyVmomi import vim

from concurrent.futures import ThreadPoolExecutor, as_completed

import json
import time

# def shut_down(vm_name, ans = 'n'):
#     parser = cli.Parser()
#     parser.add_required_arguments(cli.Argument.DATACENTER_NAME)
#     args = parser.get_args()
#     si = service_instance.connect(args)

#     VM = None
#     content = si.RetrieveContent()
#     esx_host = pchelper.get_obj(content, [vim.HostSystem], "10.1.5.3")
#     print(esx_host)
#     folder = si.content.searchIndex.FindByInventoryPath("Datacenter/vm/Brian/")
#     print(dir(folder))
#     task = folder.RegisterVM_Task(path="[san-1] abc1/abc1.vmx", 
#                                   name="new vm name", asTemplate=False, pool=None, host=esx_host)

def register():
    parser = cli.Parser()
    parser.add_required_arguments(cli.Argument.DATACENTER_NAME)
    args = parser.get_args()
    si = service_instance.connect(args)
    content = si.RetrieveContent()
    with open("results.json", "r") as j:
        data = json.load(j)

    rp = {}
    all_folders = pchelper.get_all_obj(content, [vim.ResourcePool])
    for x in all_folders:
        # print(x)
        rp[str(x)] = x

    DATACENTER = pchelper.get_obj(content, [vim.Datacenter], args.datacenter_name)
    fds = {}
    all_folders = pchelper.get_all_obj(content, [vim.Folder], DATACENTER.vmFolder)
    for f in all_folders:
        fds[str(f)] = f
    esx_host = pchelper.get_obj(content, [vim.HostSystem], "10.1.5.3")
    for d in data:
        print(fds[d['folder']].parent.name)
        print(rp[d['resource_pool']].name)
        print(d['name'])
        a=pchelper.get_obj(content, [vim.ResourcePool], rp[d['resource_pool']].name)
        print(fds[d['folder']].childEntity)
        fds[d['folder']].RegisterVM_Task(path='[san-1] xxx/abc1/abc1.vmx', name="abc1",asTemplate=False, pool=a,host=esx_host)
        # tasks.wait_for_tasks(si, [TASK])
        # fds[d['folder']].RegisterVM_Task(path=d['vm_path'], name=d['name'], 
        #                                  asTemplate=False, 
        #                                  pool=rp[d['resource_pool']], 
        #                                  host=esx_host)
        # xxx[d['folder']].RegisterVM_Task(path=d['vm_path'], name=d['name'], asTemplate=False, pool=pl[d['resource_pool']], host=esx_host)
        break

def recurring_loop(item):
    if isinstance(item, vim.Folder):
        recurring_loop(item.childEntity)

    if isinstance(item, list):
        for i in item:
            if isinstance(i, vim.VirtualMachine):
                return i
            recurring_loop(i.childEntity)


def main():
    parser = cli.Parser()
    parser.add_required_arguments(cli.Argument.DATACENTER_NAME)
    args = parser.get_args()
    si = service_instance.connect(args)
    content = si.RetrieveContent()
    DATACENTER = pchelper.get_obj(content, [vim.Datacenter], args.datacenter_name)


    obj_view = content.viewManager.CreateContainerView(DATACENTER.vmFolder, [vim.Folder], True)
    folder_list = obj_view.view
    xxx = None
    for folder in folder_list:
        if isinstance(folder.childEntity, list):
            for v in folder.childEntity:
                if isinstance(v, vim.VirtualMachine):
                    print(folder, v.name)

    esx_host = pchelper.get_obj(content, [vim.HostSystem], "10.1.23.100")
    for obj in esx_host.vm:
        print(obj.config.uuid)
    # view_manager = content.viewManager
    # datacenter = content.rootFolder.childEntity[0]
    # container_view = view_manager.CreateContainerView(datacenter, [vim.ResourcePool], True)
    # for resource_pool in container_view.view:
    #     largest_rp = resource_pool
    # # Register vm
    # TASK = xxx.RegisterVM_Task(path="[san-1] abc1/abc1.vmx", name="abc1", asTemplate=False, pool=largest_rp, host=esx_host)
    # tasks.wait_for_tasks(si, [TASK])
    # # Show host of guest OS
    # container = content.viewManager.CreateContainerView(
    #     content.rootFolder, [vim.VirtualMachine], True
    # )
    # for c in container.view:
    #     print(c.runtime.host.name)
    

if __name__ == '__main__':
    register()