from tools import cli, service_instance, tasks, pchelper
from pyVmomi import vim


def check_vm_in_dc(content, datacenter_name, uuid):
    DC = pchelper.get_obj(content, [vim.Datacenter], datacenter_name)
    SI = content.searchIndex.FindByUuid(DC, uuid, True)
    if isinstance(SI, vim.VirtualMachine):
        return True
    return False