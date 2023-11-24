# dns-slave-to-master

## Method 1
On standby host,
1. Login as root in console
2. Execute convert-to-master.sh


## Method 2
### Promote 1 of slaves to master. Configure other slaves to use new master
ansible-playbook -i hosts_pro.ini promote-to-master.yml

## Optional
### Setup BIND master and slave
ansible-playbook -i hosts.ini setup.yml