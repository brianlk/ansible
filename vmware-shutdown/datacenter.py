#!/usr/bin/env python
#
# Written by Brian Leung
#
# Example script to power off VMs


from tools import cli, service_instance, tasks, pchelper
from pyVmomi import vim

from json import JSONEncoder


# subclass JSONEncoder
class EmployeeEncoder(JSONEncoder):
        def default(self, o):
            return o.__dict__


def config_snapshot(si, datacenter_name):
    content = si.RetrieveContent()
    DATACENTER = pchelper.get_obj(content, [vim.Datacenter], datacenter_name)
    obj_view = content.viewManager.CreateContainerView(DATACENTER.vmFolder, 
                                                       [vim.Folder], True)
    folder_list = obj_view.view
    results = []
    for folder in folder_list:
        if isinstance(folder.childEntity, list):
            for v in folder.childEntity:
                obj = Object()
                if isinstance(v, vim.VirtualMachine):
                    obj.name = v.name
                    obj.uuid = v.config.uuid
                    obj.folder = folder
                    obj.host = v.summary.runtime.host
                    obj.vm_path = v.summary.config.vmPathName
                    obj.resource_pool = v.resourcePool
                    results.append(obj)

    
print(results.toJSON)
    # esx_host = pchelper.get_obj(content, [vim.HostSystem], "10.1.23.100")
    # for obj in esx_host.vm:
    #     print(obj.config.uuid)


def main():
    parser = cli.Parser()
    parser.add_required_arguments(cli.Argument.DATACENTER_NAME)
    args = parser.get_args()
    si = service_instance.connect(args)
    config_snapshot(si, args.datacenter_name)


if __name__ == '__main__':
    main()