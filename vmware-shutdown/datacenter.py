#!/usr/bin/env python
#
# Written by Brian Leung
#
# Example script to power off VMs


from tools import cli, service_instance, tasks, pchelper
from pyVmomi import vim


def config_snapshot(si, datacenter_name):
    content = si.RetrieveContent()
    DATACENTER = pchelper.get_obj(content, [vim.Datacenter], datacenter_name)
    obj_view = content.viewManager.CreateContainerView(DATACENTER.vmFolder, [vim.Folder], True)
    folder_list = obj_view.view
    xxx = None
    for folder in folder_list:
        if isinstance(folder.childEntity, list):
            for v in folder.childEntity:
                if isinstance(v, vim.VirtualMachine):
                    print(v.name, v.config.uuid, folder, v.summary.runtime.host, v.summary.config.vmPathName)

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