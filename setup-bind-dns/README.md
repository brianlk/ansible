## Deploy the BIND DNS

edit vars.yml

ansible-playbook -i inventory main.yml

## Add Zone in DNS

edit vars.yml

ansible-playbook -i inventory add.yml
