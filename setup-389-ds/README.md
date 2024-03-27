# Setup 389 Directory server

## Install 389 directory and create instance

	ansible-playbook -i inventory main.yml

## Delete instance

	ansible-playbook -i inventory delete_instance.yml
