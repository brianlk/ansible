#!/bin/bash

#
# Run the script in standby node
#
# function logToFile {
#     exec 1>>out.log 2>&1 
#     date
#     echo 
# }

# function resetLog {
#     exec 1>$(tty) 2>&1 
# }

# function checkIPFormat {
#     ip=$1
#     regexp="^([0-9]{1,3}.){3}[0-9]{1,3}\/[0-9]{1,2}$"
#     if [[ $ip =~ $regexp ]]; then
#         logToFile
#         echo "Master IP input: ${ip}"
#         resetLog
#     else
#         echo "Error: IP format error."
#         exit 1
#     fi
# }

# function changeIP {
#     logToFile
#     ip addr
#     nmcli -t conn show
#     resetLog
#     echo -n "Standby DNS IP (e.g. 10.1.23.100/16): "
#     read sip
#     checkIPFormat $sip
#     uuid=$(nmcli -t conn show|awk -F: '{print $2}')
#     nmcli conn mod $uuid ipv4.addresses $sip
#     nmcli networking off; nmcli networking on
#     sleep 3
#     ip addr
#     echo ""
#     echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
#     echo "!!!!! Please check the IP addresses !!!!!"
#     echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
#     echo ""
# }

function checkRight {
    s="/var/named/standby"
    # if file is not in standby, it is a new file
    test -e $s/$1 || { arrVar+=($1); return; }

    rmd5=$(md5sum $s/$1|awk '{print $1}')
    test $rmd5 == $2 || arrVar+=($1)
}

function convertToStandby {
    systemctl stop named
    s="/var/named/standby"
    # Compare files before copy to original master
    cd /var/named/data
    for f in `ls`
    do
        left=$(md5sum $f|awk '{print $1}')
        checkRight $f $left
    done
    enableCron
}

function enableCron {
    sed -i '/scp-from-master\.sh/s/^#//' /var/spool/cron/root
    systemctl restart crond
}

function disableFW {
    firewall-cmd --add-port=53/tcp --add-port=53/udp --permanent
    firewall-cmd --reload
}
 
function checkTTY {
    t=$(ps -q $$ | awk '{print $2}' | tail -1)
    if [[ $t =~ "pts" ]]; then
        echo "Error: it is not console."
        exit 1
    fi
}

function main {
    arrVar=()
    checkTTY
    trap "rm -rf /tmp/ctmxxx.lock; exit 1" SIGINT SIGKILL SIGTERM

    exec 200>/tmp/ctmxxx.lock
    flock -n 200 || { echo "Error: anthoer $0 is running."; exit 1; }

    clear
    D=$(date +"%Y%m%d-%H%M%S")
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
main

echo "new files ======================="
for a in ${arrVar[@]}
do
    echo $a
done
