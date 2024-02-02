# Setup MySQL replication

## Getting started

### Setup replication:

ansible-playbook main.yml

### Failover:

ansible-playbook failover.yml

### Failback:

ansible-playbook failback.yml

Branch "raw_mode": Since the RHEL 6 may not have compatible python, use raw module to implement the tasks

