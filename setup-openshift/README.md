## Setup the haproxy and bootstrap config for Openshift installation

# Edit the inventory

Update ip address of haproxy

# Edit the variables in vars.yml
Update variable domain

Update variable cluster_name

Update ip address in variables masters

Update ip address in variables workers

Update ip address in variables bootstrap

Update variable haproxy_ip

Update variable ocp_version

## Run the playbook to generate OCP config in httpd server before installation

source venv/bin/activate

ansible-playbook -i inventory main.yml

## Boot bootstrap, masters and workers with Red Hat Enterprise Linux CoreOS (RHCOS)

Boot up the nodes with RHCOS ISO

Run sudo nmtui to change ip addresses

In bootstrap node:

sudo coreos-installer install /dev/sda --insecure-ignition \
          --ignition-url=http://{{ haproxy_ip }}:8080/ocp/bootstrap.ign \
          --copy-network

sudo reboot

In master nodes:

sudo coreos-installer install /dev/sda --insecure-ignition \
          --ignition-url=http://{{ haproxy_ip }}:8080/ocp/master.ign \
          --copy-network

sudo reboot

In worker nodes:

sudo coreos-installer install /dev/sda --insecure-ignition \
          --ignition-url=http://{{ haproxy_ip }}:8080/ocp/worker.ign \
          --copy-network

sudo reboot

## Approve CSR

oc get csr -o go-template='{{range .items}}{{if not .status}}{{.metadata.name}}{{"\n"}}{{end}}{{end}}' | xargs oc adm certificate approve

## Result

export KUBECONFIG=~/installer/ocp/auth/kubeconfig

    [root@haproxy installer]# oc get nodes
    NAME                       STATUS   ROLES    AGE   VERSION
    master0.clus1.oc.example   Ready    master   52m   v1.23.17+26fdcdf
    master1.clus1.oc.example   Ready    master   51m   v1.23.17+26fdcdf
    master2.clus1.oc.example   Ready    master   45m   v1.23.17+26fdcdf
    worker0.clus1.oc.example   Ready    worker   42m   v1.23.17+26fdcdf
    worker1.clus1.oc.example   Ready    worker   28m   v1.23.17+26fdcdf
    worker2.clus1.oc.example   Ready    worker   17m   v1.23.17+26fdcdf

    [root@haproxy installer]# oc get route -A
    NAMESPACE                  NAME                HOST/PORT                                                      PATH   SERVICES            PORT    TERMINATION            WILDCARD
    openshift-authentication   oauth-openshift     oauth-openshift.apps.clus1.oc.example                                 oauth-openshift     6443    passthrough/Redirect   None
    openshift-console          console             console-openshift-console.apps.clus1.oc.example                       console             https   reencrypt/Redirect     None
    openshift-console          downloads           downloads-openshift-console.apps.clus1.oc.example                     downloads           http    edge/Redirect          None
    openshift-ingress-canary   canary              canary-openshift-ingress-canary.apps.clus1.oc.example                 ingress-canary      8080    edge/Redirect          None
    openshift-monitoring       alertmanager-main   alertmanager-main-openshift-monitoring.apps.clus1.oc.example   /api   alertmanager-main   web     reencrypt/Redirect     None
    openshift-monitoring       grafana             grafana-openshift-monitoring.apps.clus1.oc.example                    grafana             https   reencrypt/Redirect     None
    openshift-monitoring       prometheus-k8s      prometheus-k8s-openshift-monitoring.apps.clus1.oc.example             prometheus-k8s      web     reencrypt/Redirect     None
    openshift-monitoring       thanos-querier      thanos-querier-openshift-monitoring.apps.clus1.oc.example      /api   thanos-querier      web     reencrypt/Redirect     None

## Access the GUI console

https://console-openshift-console.apps.clus1.oc.example