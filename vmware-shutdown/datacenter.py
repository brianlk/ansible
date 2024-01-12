#!/usr/bin/env python
#
# Written by Brian Leung
#
# Example script to power off VMs


from tools import cli, service_instance, tasks, pchelper
from pyVmomi import vim

import json

def config_snapshot(si, datacenter_name):
    content = si.RetrieveContent()
    DATACENTER = pchelper.get_obj(content, [vim.Datacenter], datacenter_name)
    obj_view = content.viewManager.CreateContainerView(DATACENTER.vmFolder, 
                                                       [vim.Folder], True)
    folder_list = obj_view.view
    results = []
    for folder in folder_list:
        print(folder.name)
        # if isinstance(folder.childEntity, list):
        #     for v in folder.childEntity:
        #         if isinstance(v, vim.VirtualMachine) and not v.config.template:
        #             obj = {}
        #             obj['name'] = v.name
        #             obj['uuid'] = v.config.uuid
        #             obj['folder'] = str(folder)
        #             obj['host'] = str(v.summary.runtime.host)
        #             obj['vm_path'] = v.summary.config.vmPathName
        #             obj['resource_pool'] = str(v.resourcePool)
        #             print(folder.name)
        #             results.append(obj)
        #             print(v.datastore)

    with open("results.json", "w") as f:
        f.write(json.dumps(results))
        

def main():
    parser = cli.Parser()
    parser.add_required_arguments(cli.Argument.DATACENTER_NAME)
    args = parser.get_args()
    si = service_instance.connect(args)
    config_snapshot(si, args.datacenter_name)


if __name__ == '__main__':
    main()