#!/bin/bash

#
# Run the script in standby node
#
function LogToFile() {
    exec 1>>out.log 2>&1 
    date
    echo 
}

function ResetLog() {
    exec 1>$(tty) 2>&1 
}

function Lock() {
    exec 200>/tmp/$0.lock
    flock -n 200
    if [[ $? -ne 0 ]]; then
        echo "Error: anthoer $0 is running."
        exit 1
    fi
}

function CheckIPFormat() {
    ip=$1
    regexp="^([0-9]{1,3}.){3}[0-9]{1,3}\/[0-9]{1,2}$"
    if [[ $ip =~ $regexp ]]; then
        LogToFile
        echo "Master IP input: ${ip}"
        ResetLog
    else
        echo "Error: IP format error."
        exit 1
    fi
}

function ChangeIP() {
    LogToFile
    ip addr
    nmcli -t conn show
    ResetLog
    echo -n "IP:"
    read masterip
    CheckIPFormat $masterip
    uuid=$(nmcli -t conn show|awk -F: '{print $2}')
    nmcli conn mod $uuid ipv4.addresses $masterip
    nmcli networking off; nmcli networking on
    sleep 3
    ip addr
    echo ""
    echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
    echo "!!!!! Please check the IP addresses !!!!!"
    echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
    echo ""
}

function ConvertToMaster() {
    systemctl stop named
    mv /var/named/data /var/named/data.$D
    mv /etc/named.conf /etc/named.conf.$D
    cd /var/named
    cp -pr standby data
    cp /var/named/standby/named.conf /etc/named.conf
    systemctl restart named
    echo "/var/named/data.$D" > /var/tmp/cm.txt
    echo "/etc/named.conf.$D" >> /var/tmp/cm.txt
}

function CheckTTY() {
    t=$(ps -q $$ | awk '{print $2}' | tail -1)
    if [[ $t =~ "pts" ]]; then
        echo "Error: it is not console."
        exit 1
    fi
}

function main() {
    # CheckTTY
    Lock
    clear
    D=$(date +"%Y%m%d-%H%M%S")
    printf "\t\t\tMenu\n\n"
    printf "\t\t\t1. Change current IP to master IP\n\n"
    printf "\t\t\t2. Convert standby to master\n\n"
    echo -n "Choice? "
    read c
    case $c in
            1)
                ChangeIP
                ;;
            2)
                ConvertToMaster
                ;;
            *)
                echo "Wrong option!"
                exit
    esac
}

main
