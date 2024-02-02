# Installation k8s by ansible

## 1. edit inventory  
    [nodes]
    10.1.23.250 ansible_user=root
    10.1.23.251 ansible_user=root
    10.1.23.252 ansible_user=root
    10.1.23.253 ansible_user=root
    10.1.23.254 ansible_user=root

    [masters]
    10.1.23.250 ansible_user=root
    10.1.23.254 ansible_user=root


    [workers]
    10.1.23.251 ansible_user=root
    10.1.23.252 ansible_user=root
    10.1.23.253 ansible_user=root

## 2. ansible-playbook -i inventory main.yml

