#!/bin/bash

vcenter_ip="10.1.5.44"
basic_auth_base64=$(echo -n 'administrator@vsphere.local:P@ssw0rd' | base64)
session_id_json=$(curl --silent -k -XPOST -H "Authorization: Basic ${basic_auth_base64}" https://$vcenter_ip/rest/com/vmware/cis/session)
session_id=$(echo "$session_id_json" | jq '.value')
x=$(echo "$session_id" | sed -e 's/\"//g')
#curl --silent -k -XGET -H 'vmware-api-session-id: '"$x"  https://$vcenter_ip/rest/vcenter/vm # list vm internal name

curl --silent -k -XGET -H 'vmware-api-session-id: '"$x"  https://$vcenter_ip/rest/vcenter/vm/vm-97 # get specific vm details

# curl -k -c cookies.txt -i -X PUT -H "Content-Type: application/vnd.ibm.powervm.web+xml; type=LogonRequest" -H "Accept: application/vnd.ibm.powervm.web+xml; type=LogonResponse" -H "X-Audit-Memento: hmc_test" -d@x.xml https://10.1.4.33/rest/api/web/Logon 
#  curl -k -X GET -H "Content-Type: application/vnd.ibm.powervm.uom+xml; Type=ManagedSystem" -H "X-API-Session: NxHhMafg9RipO_8ERqZxVghS-uay7HRJhbrAFAuQDxQNXytBSjD6LtaAZgxBeizVLLBbojcCt7zmPKJwU1P60KW-TPmGXMQIUiq047Q6sipFjCcdaUiOWlu74B0QLJe8r4UlYQJAArVWC398-2s7UAL6ugsQKEVHlEQayxhqgI1s2iTUtKo_o8y6g_eGUuYZLe1rPW4jI6McrhhH2jid3yWek0PCfA0T6Eq69TjZRS4=" https://10.1.4.33/rest/api/uom/ManagedSystem