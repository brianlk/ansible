# Migrate data to new SAN devices by LVM
## Check the new SAN devices before mirror
Edit the variable luns in hosts.ini and put the new LUN id in it

ansible-playbook -i hosts.ini check.yml

## Mirror the volumes to new SAN disks
Edit the variable luns in hosts.ini and put the new LUN id in it

ansible-playbook -i hosts.ini mirror.yml

## Unmirror the volumes and remove the PV from volume group

ansible-playbook -i hosts.ini unmirror.yml
