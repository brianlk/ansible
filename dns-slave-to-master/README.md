# dns-slave-to-master

### Setup BIND master and slave
ansible-playbook -i hosts.ini setup.yml

### Promote 1 of slaves to master. Configure other slaves to use new master
ansible-playbook -i hosts_pro.ini promote-to-master.yml


