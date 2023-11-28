# dns-slave-to-master

## Appoach 1
On standby host,
    
    Run the job: /root/scp-from-master.sh 10.1.23.4

    Cronjob is added:

    */60 * * * * /root/scp-from-master.sh 10.1.23.4 >>/tmp/scpfm.log 2>&1

When master DNS is down,
    
    Login the VM console of standby host

    Run the script: ./convert-to-master.sh

    Change ip address and convert it to master

When master DNS is resumed,

    Login the VM console of standby host

    Run the script: ./convert-to-standby.sh

    Change ip address and convert it to standby

## Appoach 2
### Promote 1 of slaves to master. Configure other slaves to use new master
ansible-playbook -i hosts_pro.ini promote-to-master.yml

## Optional
### Setup BIND master and slave
ansible-playbook -i hosts.ini setup.yml