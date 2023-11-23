#!/bin/bash

#
# Run the script in standby node
#

function LogToFile() {
    exec 1>out.log 2>&1 
    date
    echo 
}

function ResetLog() {
    exec 1>$(tty) 2>&1 
}

function ChangeIP() {
    LogToFile
    ip addr
    nmcli -t conn show
    ResetLog
    echo -n "IP:"
    read masterip
    uuid=$(nmcli -t conn show|awk -F: '{print $2}')
    nmcli conn mod $uuid ipv4.addresses $masterip
    nmcli networking off; nmcli networking on
    DEFAULT_ROUTE=$(ip route show default | awk '/default/ {print $3}')
    ping -c 1 $DEFAULT_ROUTE
    if [ $? -ne 0 ]; then
        echo "ERROR: Cannot ping gateway. Exit!"
        exit
    fi
}

function ConvertToMaster() {
    mv /var/named/data /var/named/data.$D
    mv /etc/named.conf /etc/named.conf.$D
    cd /var/named
    ln -s standby data
    ln -s standby/named.conf /etc/named.conf
    systemctl restart named
}

function main() {
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
