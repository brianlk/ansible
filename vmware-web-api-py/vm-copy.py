#!/usr/bin/env python
#
# Written by Brian Leung
#
# Example script to shut down VMs

from datacenter import run_cli, read_vm_list
from tools import cli, service_instance, tasks, pchelper
from pyVmomi import vim
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Union

import time


def main():
    args = run_cli(cli.Argument.DATACENTER_NAME)
    si = service_instance.connect(args)
    content = si.RetrieveContent()
    DATACENTER = pchelper.get_obj(content, [vim.Datacenter], args.datacenter_name)
    abc1 = pchelper.get_obj(content, [vim.VirtualMachine], "abc1", DATACENTER.vmFolder)
    spec = vim.vm.ConfigSpec()
    # get all disks on a VM, set unit_number to the next available
    unit_number = 0
    controller = None
    disk_size = 5
    disk_type = "thin"
    for device in abc1.config.hardware.device:
        print(device)
        if hasattr(device.backing, 'fileName'):
            unit_number = int(device.unitNumber) + 1
            # unit_number 7 reserved for scsi controller
            if unit_number == 7:
                unit_number += 1
            if unit_number >= 16:
                print("we don't support this many disks")
                return -1
        if isinstance(device, vim.vm.device.VirtualSCSIController):
            controller = device
    if controller is None:
        print("Disk SCSI controller not found!")
        return -1
    # add disk here
    dev_changes = []
    new_disk_kb = int(disk_size) * 1024 * 1024
    disk_spec = vim.vm.device.VirtualDeviceSpec()
    disk_spec.fileOperation = "create"
    disk_spec.operation = vim.vm.device.VirtualDeviceSpec.Operation.add
    disk_spec.device = vim.vm.device.VirtualDisk()
    disk_spec.device.backing = \
        vim.vm.device.VirtualDisk.FlatVer2BackingInfo()
    if disk_type == 'thin':
        disk_spec.device.backing.thinProvisioned = True
    disk_spec.device.backing.diskMode = 'persistent'
    disk_spec.device.unitNumber = unit_number
    disk_spec.device.capacityInKB = new_disk_kb
    disk_spec.device.controllerKey = controller.key
    dev_changes.append(disk_spec)
    spec.deviceChange = dev_changes
    abc1.ReconfigVM_Task(spec=spec)
    

if __name__ == '__main__':
    main()