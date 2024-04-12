# Setup 389 Directory server

## Set the variables in vars.yml

## Install 389 directory server and create instance

	ansible-playbook -i inventory install_server.yml

## LDAP client setup

	ansible-playbook -i inventory add_client.yml

## Delete LDAP instance

	ansible-playbook -i inventory delete_instance.yml

## Configure single supplier replication

	ansible-playbook -i inventory configure-single-supplier-replication.yml

## Reference

https://access.redhat.com/documentation/en-us/red_hat_directory_server/12/html-single/installing_red_hat_directory_server/index#proc_starting-and-stopping-a-directory-server-instance-using-the-command-line_assembly_starting-and-stopping-instance

https://access.redhat.com/solutions/4356441
