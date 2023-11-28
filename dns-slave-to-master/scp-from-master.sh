#!/bin/bash

#
# Run the script in standby node
#
trap "rm -rf /tmp/scpxxx.lock; exit 1" SIGINT SIGTERM

function Lock {
    exec 200>/tmp/scpxxx.lock
    echo $$ > /tmp/scpxxx.lock
    flock -n 200 || { echo "Error: anthoer $0 is running."; exit 1; }
}

function checkPrereq {
    ip=$1
    regexp="^([0-9]{1,3}.){3}[0-9]{1,3}$"
    if [[ $ip =~ $regexp ]]; then
        echo "Master IP input: ${ip}"
    else
        echo "Error: IP format error."
        exit 1
    fi
    rpm -qa | grep bind-9 > /dev/null 2>&1
    if [[ $? -ne 0 ]]; then
        echo "Error: no bind-9 installed."
        exit 1
    fi
    firewall-cmd --add-port=53/tcp --add-port=53/udp --permanent >/dev/null 2>&1
    firewall-cmd --reload > /dev/null 2>&1
}

function addCron {
    cronitem='*/60 * * * * '"$*"' >>/tmp/scpfm.log 2>&1'
    echo "$cronitem"
    rootcron="/var/spool/cron/root"
    grep "$0" $rootcron > /dev/null
    # if no cron job is found, add it
    if [[ $? -ne 0 ]]; then
        echo "$cronitem" >> $rootcron
        systemctl restart crond
    fi
}

function main {
    DEST="/var/named/standby"
    MIP=$1

    test -d $DEST || mkdir -p $DEST
    date
    scp -pr "$MIP":/var/named/data/* $DEST &&  echo success!  || { echo error!; exit 1; }
    scp -pr "$MIP":/etc/named.conf $DEST/named.conf && echo success! || { echo error!; exit 1; }
    chown -R named:named $DEST
    chown root:named $DEST/named.conf
}

## Main start

if [ $# -ne 1 ]; then
    echo "ERROR: No master ip is provided."
    echo "Usage: scp-from-master.sh x.x.x.x"
    exit 1
fi

scriptname=$0
ip=$1

Lock
checkPrereq "$ip"
addCron "$scriptname" "$ip"
main "$ip"
rm -f /tmp/scpxxx.lock

