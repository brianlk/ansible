Installation k8s:

1. edit inventory  
    [nodes]  
    10.1.4.x  ansible_node=10.1.4.x ansible_user=root  
    10.1.4.x  ansible_node=10.1.4.x ansible_user=root  
    10.1.4.x  ansible_node=10.1.4.x ansible_user=root  
    10.1.4.x  ansible_node=10.1.4.x ansible_user=root

2. ansible-playbook -i inventory main.yml

