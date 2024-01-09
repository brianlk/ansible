#!/usr/bin/env python
#
# Written by Brian Leung
#
# Example script to unmount datastores

from tools import cli, service_instance, tasks, pchelper
from pyVmomi import vim

from concurrent.futures import ThreadPoolExecutor, as_completed

import time
import csv
import json


def main():
    parser = cli.Parser()
    parser.add_required_arguments(cli.Argument.MOUNT)
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
    host_view = content.viewManager.CreateContainerView(content.rootFolder, [vim.HostSystem], True)
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
        print(f"{res['host']} unmount datastore {res['name']} {res['uuid']}")
        if args.mount == 'n':
            res['host'].configManager.storageSystem.UnmountVmfsVolume(vmfsUuid=res['uuid'])
        res['host'].configManager.storageSystem.MountVmfsVolume(vmfsUuid=res['uuid'])
        count += 1

    print(f"\n{count} datastores are unmounted.")

if __name__ == '__main__':
    main()