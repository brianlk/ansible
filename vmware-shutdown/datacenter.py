#!/usr/bin/env python
#
# Written by Brian Leung
#
# Example script to power off VMs


from tools import cli, service_instance, tasks, pchelper
from pyVmomi import vim

import json


def run_cli(*arg):
    parser = cli.Parser()
    for x in arg:
        parser.add_required_arguments(x)
    args = parser.get_args()
    return args

def config_snapshot(si, datacenter_name):
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


    with open("results.json", "w") as f:
        f.write(json.dumps(results))
        

def main():
    # parser = cli.Parser()
    # parser.add_required_arguments(cli.Argument.DATACENTER_NAME)
    # args = parser.get_args()
    args = run_cli(cli.Argument.MOUNT, cli.Argument.DATACENTER_NAME)
    si = service_instance.connect(args)
    # config_snapshot(si, args.datacenter_name)


if __name__ == '__main__':
    main()