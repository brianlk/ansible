## Setup the haproxy and bootstrap config for Openshift installation

# Edit vars.yml
Update variable domain

Update variable cluster_name

Update ip address in variables masters

Update ip address in variables workers

Update ip address in variables bootstrap

Update variable haproxy_ip

Update variable ocp_version (Optional)

## Run the playbook

source venv/bin/activate

ansible-playbook -i inventory main.yml

## Boot bootstrap, masters and workers with Red Hat Enterprise Linux CoreOS (RHCOS)

Boot up the nodes with RHCOS ISO

Run sudo nmtui to change ip addresses

In bootstrap node:

sudo coreos-installer install /dev/sda --insecure-ignition \
          --ignition-url=http://{{ haproxy_ip }}:8080/ocp/bootstrap.ign \
          --copy-network

In master nodes:

sudo coreos-installer install /dev/sda --insecure-ignition \
          --ignition-url=http://{{ haproxy_ip }}:8080/ocp/master.ign \
          --copy-network

In worker nodes:

sudo coreos-installer install /dev/sda --insecure-ignition \
          --ignition-url=http://{{ haproxy_ip }}:8080/ocp/worker.ign \
          --copy-network

## Approve CSR

oc get csr -o go-template='{{range .items}}{{if not .status}}{{.metadata.name}}{{"\n"}}{{end}}{{end}}' | xargs oc adm certificate approve