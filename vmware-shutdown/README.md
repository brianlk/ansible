# VMware DR scripts

## Requirements:

1. python 3.9 with virtual environment

2. pyvmomi module

pip install pyvmomi

## Getting started

**_Activate python virtual env_**

source ~/venv/bin/activate

## DR steps

**_List all VMs_**

./get_all_vm_names.py -s _vcenter-ip_ -u '_administrator@vsphere.local_' -p '_password_' -nossl

**_edit hostlist_**

Add the vm names into file vm_list

**_Shut down VMs in Vcenter_**

./shutdown_vms.py -s _vcenter-ip_ -u '_administrator@vsphere.local_' -p '_password_' -nossl

**_Unregister VMs in Vcenter_**

./unregister_vms.py -s _vcenter-ip_ -u '_administrator@vsphere.local_' -p '_password_' -nossl

**_Edit datastore_list.csv_**

Add the datastores being umounted

**_Unmount datastores in Vcenter_**

./unmount_datastore.py -s _vcenter-ip_ -u '_administrator@vsphere.local_' -p '_password_' -nossl