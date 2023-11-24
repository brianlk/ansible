#!/bin/bash

#
# Run the script in standby node
#
function logToFile() {
    exec 1>>out.log 2>&1 
    date
    echo 
}

function resetLog() {
    exec 1>$(tty) 2>&1 
}

function checkIPFormat() {
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

function changeIP() {
    logToFile
    ip addr
    nmcli -t conn show
    resetLog
    echo -n "Master DNS IP (e.g. 10.1.23.100/16): "
    read masterip
    checkIPFormat $masterip
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

function convertToMaster() {
    systemctl stop named
    mv /var/named/data /var/named/data.$D
    mv /etc/named.conf /etc/named.conf.$D
    cd /var/named
    cp -pr standby data
    cp -pr /var/named/standby/named.conf /etc/named.conf
    systemctl restart named
    [[ $? -eq 0 ]] || { echo "Error: named start failed."; exit 1; }
    echo "Success: named started."
    chmod -x /etc/rc.local
}

function convertToStandby() {
    systemctl stop named
    cd /var/named
    diff -q data standby
}

function checkTTY() {
    t=$(ps -q $$ | awk '{print $2}' | tail -1)
    if [[ $t =~ "pts" ]]; then
        echo "Error: it is not console."
        exit 1
    fi
}

function main() {
    checkTTY
    trap "rm -rf /tmp/ctmxxx.lock; exit 1" SIGINT SIGKILL SIGTERM

    exec 200>/tmp/ctmxxx.lock
    flock -n 200 || { echo "Error: anthoer $0 is running."; exit 1; }

    clear
    D=$(date +"%Y%m%d-%H%M%S")
    printf "\t\t\tMenu\n\n"
    printf "\t\t\t1) Change current IP to master IP\n\n"
    printf "\t\t\t2) Convert standby to master\n\n"
    printf "\t\t\tq) Exit\n\n"
    echo -n "Choice? "
    read c
    case $c in
            1)
                changeIP
                ;;
            2)
                convertToMaster
                ;;
            q)
                exit 1
                ;;
            *)
                echo "Wrong option!"
                exit
    esac
}

main
