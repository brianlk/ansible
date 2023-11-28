#!/bin/bash

function logToFile {
    exec 1>>out.log 2>&1 
    date
    echo 
}

function resetLog {
    exec 1>$(tty) 2>&1 
}

function checkIPFormat {
    ip=$1
    regexp="^([0-9]{1,3}.){3}[0-9]{1,3}\/[0-9]{1,2}$"
    if [[ $ip =~ $regexp ]]; then
        logToFile
        echo "Master IP input: ${ip}"
        resetLog
    else
        echo "Error: IP format error."
        exit 1
    fi
}

function changeIP {
    logToFile
    ip addr
    nmcli -t conn show
    resetLog
    echo -n "Master DNS IP (e.g. 10.1.23.100/16): "
    read -r masterip
    checkIPFormat "$masterip"
    uuid=$(nmcli -t conn show|awk -F: '{print $2}')
    nmcli conn mod "$uuid" ipv4.addresses "$masterip"
    nmcli networking off; nmcli networking on
    sleep 3
    ip addr
    echo ""
    echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
    echo "!!!!! Please check the IP addresses !!!!!"
    echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
    echo ""
    echo "master:$masterip" | sed -e 's/\/[0-9]{2}$//' > /var/tmp/"$0.txt"
}

function checkTTY {
    t=$(ps -q $$ | awk '{print $2}' | tail -1)
    if [[ $t =~ "pts" ]]; then
        echo "Error: it is not console."
        exit 1
    fi
}