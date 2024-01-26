#!/bin/bash

basic_auth_base64=$(echo -n 'administrator@vsphere.local:abcd1234' | base64)
session_id_json=$(curl --silent -k -XPOST -H "Authorization: Basic ${basic_auth_base64}" https://10.1.5.44/rest/com/vmware/cis/session)
session_id=$(echo "$session_id_json" | jq '.value')
x=$(echo "$session_id" | sed -e 's/\"//g')
curl -k -XGET -H 'vmware-api-session-id: '"$x"  https://10.1.5.44/rest/vcenter/vm