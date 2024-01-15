#!/usr/bin/env python
#
# Written by Brian Leung
#
# Example script to unmount/mount datastores

from datacenter import run_cli
from tools import cli, service_instance, tasks, pchelper
from pyVmomi import vim

from concurrent.futures import ThreadPoolExecutor, as_completed

import time
import csv
import json


def find_all_vcenter_ds(content, datacenter):
    # Connect to Vcenter and find all datastores
    uuids = []
    host_view = content.viewManager.CreateContainerView(datacenter, [vim.HostSystem], True)
    # Find all datastores in vcenter
    for host in host_view.view:
        # host.configManager.storageSystem.UnmountVmfsVolume(vmfsUuid="65976112-57b5c868-b7b1-005056af88ac")
        mount_arr = host.configManager.storageSystem.fileSystemVolumeInfo.mountInfo
        for m in mount_arr: 
            if m.volume.type == "VMFS":
                uuids.append({'uuid': m.volume.uuid, 'name': m.volume.name, 'host': host})
    return uuids


def read_ds_csv():
    csv_uuids = {}
    # Read .csv to get datastores being unmounted
    with open('datastore_list.csv') as csvfile:
        rows = csv.DictReader(csvfile)
        for row in rows:
            csv_uuids[row['datastore_name']] = row['datastore_uuid']
    return csv_uuids


def main():

    args = run_cli(cli.Argument.MOUNT, cli.Argument.DATACENTER_NAME)
    si = service_instance.connect(args)
    content = si.RetrieveContent()
    DATACENTER = pchelper.get_obj(content, [vim.Datacenter], args.datacenter_name)
       
    results = []
    # Match the csv uuid with Vcenter uuid
    for csv_name, csv_uuid in read_ds_csv().items():
        for u in find_all_vcenter_ds(content, DATACENTER):
            if u['uuid'] == csv_uuid and u['name'] == csv_name:
                results.append(u)
    
    # Unmount the datastores
    count = 0
    for res in results:
        
        if args.mount.lower() == 'n':
            res['host'].configManager.storageSystem.UnmountVmfsVolume(vmfsUuid=res['uuid'])
            state = "unmounted"
        elif args.mount.lower() == 'y':
            res['host'].configManager.storageSystem.MountVmfsVolume(vmfsUuid=res['uuid'])
            state = "mounted"
        else:
            raise Exception(f"Wrong mount state: {state}")
        print(f"{res['host']} {state} datastore {res['name']} {res['uuid']}")

        count += 1

    print(f"\n{count} datastores are {state}.")

if __name__ == '__main__':
    main()