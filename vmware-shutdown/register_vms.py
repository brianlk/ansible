#!/usr/bin/env python
#
# Written by Brian Leung
#
# Example script to register VMs after DR

from concurrent.futures import ThreadPoolExecutor, as_completed
from datacenter import run_cli
from tools import cli, service_instance, tasks, pchelper
from pyVmomi import vim

import json


def get_all_folders(content, DATACENTER):
    fds = {}
    all_folders = pchelper.get_all_obj(content, [vim.Folder], DATACENTER.vmFolder)

    for f in all_folders:
        fds[str(f)] = f
    # return a map fds['folder_name'] = folder object        
    return fds


def get_all_resource_pools(content):
    rps = {}
    all_folders = pchelper.get_all_obj(content, [vim.ResourcePool])
    for x in all_folders:
        rp[str(x)] = x
    # return a map rp['pool_name'] = pool object
    return rps


def read_vm_list():
    #Read the VM names from hosts file
    with open("vm_list", "r") as file:
        file_content = file.read()
    return file_content.split('\n')


def read_result_json():
    with open("results.json", "r") as j:
        data = json.load(j)
    return data


def register_vm(content, DATACENTER, vms, fds, rps):
    for vm in vms:
        for d in read_result_json():
            if vm == d['name']:
                esx_host = pchelper.get_obj(content, [vim.HostSystem], d['host'])
                if d['folder'] == str(DATACENTER.vmFolder):
                    # VM in datacenter root folder
                    DATACENTER.vmFolder.RegisterVM_Task(path=d['vm_path'], name=d['name'],
                                                    asTemplate=False, 
                                                    pool=rps[d['resource_pool']],
                                                    host=esx_host)
                else:
                    fds[d['folder']].RegisterVM_Task(path=d['vm_path'], name=d['name'],
                                                    asTemplate=False, 
                                                    pool=rps[d['resource_pool']],
                                                    host=esx_host)


def main():
    args = run_cli(cli.Argument.DATACENTER_NAME)
    si = service_instance.connect(args)
    content = si.RetrieveContent()

    rps = get_all_resource_pools(content)

    DATACENTER = pchelper.get_obj(content, [vim.Datacenter], args.datacenter_name)
    fds = get_all_folders(content, DATACENTER)

    vms = read_vm_list()
    register_vm(content, DATACENTER, vms, fds, rps)


if __name__ == '__main__':
    main()