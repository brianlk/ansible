#!/bin/bash

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
}

function ConvertToMaster() {
    echo "bbbbbbbbbb"
}


function main() {
    clear
    printf "\t\t\tMenu\n\n"
    printf "\t\t\t1. Change current IP to master IP\n\n"
    printf "\t\t\t2. Convert standby to master\n\n"
    echo -n "Choice? "
    read c
    case $c in
            1)
                ChangeIP
                ls -l
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
