# dns-slave-to-master

## Appoach 1
On standby host,
1. start background job
    chmod +x /etc/rc.local
    cd /root
    nohup ./scp-from-master.sh 10.1.23.4 > /tmp/xxx.log 2>&1 &


1. Login as root in VM console
2. Execute convert-to-master.sh


## Appoach 2
### Promote 1 of slaves to master. Configure other slaves to use new master
ansible-playbook -i hosts_pro.ini promote-to-master.yml

## Optional
### Setup BIND master and slave
ansible-playbook -i hosts.ini setup.yml