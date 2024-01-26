#!/bin/bash

basic_auth_base64=$(echo -n 'administrator@vsphere.local:P@ssw0rd' | base64)
session_id=$(curl --silent -k -XPOST -H "Authorization: Basic ${basic_auth_base64}" https://10.1.5.44/rest/com/vmware/cis/session)
echo "$session_id"
