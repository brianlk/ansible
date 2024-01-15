#!/usr/bin/env python
#
# Written by Brian Leung
#
# Example script to power off VMs


from tools import cli, service_instance, tasks, pchelper
from pyVmomi import vim

import json


def read_vm_list():
    #Read the VM names from hosts file
    with open("vm_list", "r") as file:
        file_content = file.read()
    return file_content.split('\n')


def run_cli(*args):
    parser = cli.Parser()
    for a in args:
        parser.add_required_arguments(a)
    args = parser.get_args()
    return args


def vm_config_backup(si, datacenter_name):
    content = si.RetrieveContent()
    DATACENTER = pchelper.get_obj(content, [vim.Datacenter], datacenter_name)
    
    results = []
    VM = pchelper.get_all_obj(content, [vim.VirtualMachine], DATACENTER.vmFolder)
    for v in VM:
        if not v.config.template:
            print(f"Storing config of {v.name} in results.json.")
            obj = {}
            obj['name'] = v.name
            obj['uuid'] = v.config.uuid
            obj['folder'] = str(v.parent)
            obj['host'] = v.summary.runtime.host.name
            obj['vm_path'] = v.summary.config.vmPathName
            obj['resource_pool'] = str(v.resourcePool)
            results.append(obj)

    # Write vm config to results.json
    with open("results.json", "w") as f:
        f.write(json.dumps(results))
        

def main():
    args = run_cli(cli.Argument.DATACENTER_NAME)
    si = service_instance.connect(args)
    vm_config_backup(si, args.datacenter_name)


if __name__ == '__main__':
    main()