## Deploy the BIND DNS

edit vars.yml

ansible-playbook -i inventory deploy-dns.yml

## Add Zone in DNS

edit vars.yml

ansible-playbook -i inventory add.yml

## Add record in DNS
ansible-playbook -i inventory -e "domain=td.test" -e "alias=www2" -e "ip=10.1.23.160" addrecord.yml