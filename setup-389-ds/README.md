# Setup 389 Directory server

## Install 389 directory and create instance

	ansible-playbook -i inventory main.yml

## Delete instance

	ansible-playbook -i inventory delete_instance.yml

## Reference

https://access.redhat.com/documentation/en-us/red_hat_directory_server/12/html-single/installing_red_hat_directory_server/index#proc_starting-and-stopping-a-directory-server-instance-using-the-command-line_assembly_starting-and-stopping-instance
