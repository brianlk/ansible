## Setup the haproxy and bootstrap for Openshift installation

source venv/bin/activate

ansible-playbook -i inventory main.yml

## Approve CSR

oc get csr -o go-template='{{range .items}}{{if not .status}}{{.metadata.name}}{{"\n"}}{{end}}{{end}}' | xargs oc adm certificate approve