#!/bin/bash

#
# Run the script in standby node
#

function scpToOrigMaster {
    ip=$1
    echo "new files ======================="
    for a in "${arrVar[@]}"
    do
        if [[ $a == "named.conf" ]]; then
            scp /etc/named.conf "$ip:/etc/named.conf"
        else
            scp "$a" "$ip:/var/named/data/$a"
        fi
    done
}

function compareNamedFiles {
    filename=$1
    leftMD5=$2
    s="/var/named/standby"
    if [[ $filename == "/etc/named.conf" ]]; then
        filename=$(echo "$filename"|sed -e 's/^\/[a-z]*\///')
    fi
    # if file is not in standby, it is a new file
    test -e "$s/$filename" || { arrVar+=("$filename"); return; }

    rightMD5=$(md5sum "$s/$filename"|awk '{print $1}')
    test "$rightMD5" == "$leftMD5" || arrVar+=("$filename")
}

function convertToStandby {
    systemctl stop named
    s="/var/named/standby"
    # Compare files before copy to original master
    cd /var/named/data || { echo "Error: /var/named errors."; exit; }
    for f in * "/etc/named.conf"
    do
        left=$(md5sum "$f"|awk '{print $1}')
        compareNamedFiles "$f" "$left"
    done
    scpToOrigMaster "$(cat /tmp/scpxxx.lock)"
    enableCron
}

function enableCron {
    sed -i '/scp-from-master\.sh/s/^#//' /var/spool/cron/root
    systemctl restart crond
}

function main {
    arrVar=()
    checkTTY
    trap "rm -rf /tmp/ctmxxx.lock; exit 1" SIGINT SIGTERM

    exec 200>/tmp/ctmxxx.lock
    flock -n 200 || { echo "Error: anthoer $0 is running."; exit 1; }

    clear

    printf "\t\t\tMenu\n\n"
    printf "\t\t\t1) Change current IP to standby IP\n\n"
    printf "\t\t\t2) Convert master to standby\n\n"
    printf "\t\t\tq) Exit\n\n"
    echo -n "Choice? "
    read c
    case $c in
            1)
                changeIP
                ;;
            2)
                convertToStandby
                ;;
            q)
                exit 1
                ;;
            *)
                echo "Wrong option!"
                exit
    esac
}

#############
# Main starts
#############
source ./common-func.sh
main

