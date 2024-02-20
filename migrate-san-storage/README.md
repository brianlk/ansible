# Migrate data to new SAN devices by LVM
## Define the new LUNs
Edit hosts.ini

Add the new LUNs is in variable new_luns

## Discover the new SAN devices
Edit the variable luns in hosts.ini and put the new LUN id in it

ansible-playbook -i hosts.ini check.yml

## Mirror the volumes to new SAN disks
Edit the variable luns in hosts.ini and put the new LUN id in it

ansible-playbook -i hosts.ini mirror.yml

## Unmirror the volumes and remove the PV from volume group

ansible-playbook -i hosts.ini unmirror.yml
