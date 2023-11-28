#!/bin/bash

#
# Run the script in standby node
#

function convertToMaster {
    disableCron
    systemctl stop named
    mv /var/named/data "/var/named/data.$D"
    mv /etc/named.conf "/etc/named.conf.$D"
    cd /var/named || { echo "Error: /var/named errors."; exit; }
    cp -pr standby data
    cp -pr /var/named/standby/named.conf /etc/named.conf
    systemctl restart named || { echo "Error: named start failed."; exit 1; }
    echo "Success: named started."
}

function convertToStandby {
    systemctl stop named
    cd /var/named || { echo "Error: /var/named errors."; exit; }
    diff -q data standby
}

function disableCron {
    sed -i '/scp-from-master\.sh/s/^/#/' /var/spool/cron/root
    systemctl restart crond
}

function disableFW {
    firewall-cmd --add-port=53/tcp --add-port=53/udp --permanent
    firewall-cmd --reload
}
 
function main {
    checkTTY
    trap "rm -rf /tmp/ctmxxx.lock; exit 1" SIGINT SIGTERM

    exec 200>/tmp/ctmxxx.lock
    flock -n 200 || { echo "Error: anthoer $0 is running."; exit 1; }

    clear
    D=$(date +"%Y%m%d-%H%M%S")
    printf "\t\t\tMenu\n\n"
    # printf "\t\t\t1) Change current IP to master IP\n\n"
    printf "\t\t\t1) Convert standby to master\n\n"
    printf "\t\t\tq) Exit\n\n"
    echo -n "Choice? "
    read c
    case $c in
            # 1)
            #     changeIP
            #     ;;
            1)
                changeIP
                convertToMaster
                disableFW
                ;;
            q)
                exit 1
                ;;
            *)
                echo "Wrong option!"
                exit
    esac
}

###############
# Main starts
###############
source ./common-func.sh
main
