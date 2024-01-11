#!/usr/bin/env python
#
# Written by Brian Leung
#
# Example script to unmount/mount datastores

from tools import cli, service_instance, tasks, pchelper
from pyVmomi import vim

from concurrent.futures import ThreadPoolExecutor, as_completed

import time
import csv
import json


def main():
    parser = cli.Parser()
    parser.add_required_arguments(cli.Argument.MOUNT, cli.Argument.DATACENTER_NAME)
    args = parser.get_args()
    csv_uuids = {}
    # Read .csv to get datastores being unmounted
    with open('datastore_list.csv') as csvfile:
        rows = csv.DictReader(csvfile)
        for row in rows:
            csv_uuids[row['datastore_name']] = row['datastore_uuid']

    # Connect to Vcenter and find all datastores
    uuids = []
    si = service_instance.connect(args)
    content = si.RetrieveContent()
    DATACENTER = pchelper.get_obj(content, [vim.Datacenter], args.datacenter_name)
    host_view = content.viewManager.CreateContainerView(DATACENTER, [vim.HostSystem], True)
    # Find all datastores in vcenter
    for host in host_view.view:
        # host.configManager.storageSystem.UnmountVmfsVolume(vmfsUuid="65976112-57b5c868-b7b1-005056af88ac")
        mount_arr = host.configManager.storageSystem.fileSystemVolumeInfo.mountInfo
        for m in mount_arr: 
            if m.volume.type == "VMFS":
                uuids.append({'uuid': m.volume.uuid, 'name': m.volume.name, 'host': host})
    
    results = []
    # Match the csv uuid with Vcenter uuid
    for csv_name, csv_uuid in csv_uuids.items():
        for u in uuids:
            if u['uuid'] == csv_uuid and u['name'] == csv_name:
                results.append(u)
    
    # Unmount the datastores
    count = 0
    for res in results:
        
        if args.mount == 'n':
            res['host'].configManager.storageSystem.UnmountVmfsVolume(vmfsUuid=res['uuid'])
            state = "unmounted"
        else:
            res['host'].configManager.storageSystem.MountVmfsVolume(vmfsUuid=res['uuid'])
            state = "mounted"
        print(f"{res['host']} {state} datastore {res['name']} {res['uuid']}")

        count += 1

    print(f"\n{count} datastores are {state}.")

if __name__ == '__main__':
    main()