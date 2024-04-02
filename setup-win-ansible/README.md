## Setup an ansible managed node to manage Windows clients

### Run the command in control node to configure kerberos for AD:

    ansible-playbook main.yml

### Inventory hosts.ini is generated and kerberos is configured

### Run the command in ansible control node to test ansible-win connection
    ansible -m win_ping -i inventory winhost

    win2016pdc.TEST.LOC | SUCCESS => {
        "changed": false,
        "ping": "pong"
    }

