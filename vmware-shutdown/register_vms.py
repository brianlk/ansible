#!/usr/bin/env python
#
# Written by Brian Leung
#
# Example script to register VMs after DR

from tools import cli, service_instance, tasks, pchelper
from pyVmomi import vim

from concurrent.futures import ThreadPoolExecutor, as_completed

import json
import time


def main():
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
        rp[str(x)] = x

    DATACENTER = pchelper.get_obj(content, [vim.Datacenter], args.datacenter_name)
    fds = {}
    all_folders = pchelper.get_all_obj(content, [vim.Folder], DATACENTER.vmFolder)

    for f in all_folders:
        fds[str(f)] = f

    #Read the VM names from hosts file
    with open("vm_list", "r") as file:
        file_content = file.read()
    vms = file_content.split('\n')

    print(DATACENTER.vmFolder)
    for d in data:
        for vm in vms:
            if vm == d['name']:
                esx_host = pchelper.get_obj(content, [vim.HostSystem], d['host'])
                if d['folder'] == str(DATACENTER.vmFolder):
                    # VM in datacenter root folder
                    DATACENTER.vmFolder.RegisterVM_Task(path=d['vm_path'], name=d['name'],
                                                    asTemplate=False, 
                                                    pool=rp[d['resource_pool']],
                                                    host=esx_host)
                else:
                    fds[d['folder']].RegisterVM_Task(path=d['vm_path'], name=d['name'],
                                                    asTemplate=False, 
                                                    pool=rp[d['resource_pool']],
                                                    host=esx_host)


if __name__ == '__main__':
    main()