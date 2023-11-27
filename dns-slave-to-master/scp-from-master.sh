#!/bin/bash

#
# Run the script in standby node
#
trap "rm -rf /tmp/scpxxx.lock; exit 1" SIGINT SIGKILL SIGTERM

function Lock() {
    exec 200>/tmp/scpxxx.lock
    flock -n 200 || { echo "Error: anthoer $0 is running."; exit 1; }
}

function checkIPFormat() {
    ip=$1
    regexp="^([0-9]{1,3}.){3}[0-9]{1,3}$"
    if [[ $ip =~ $regexp ]]; then
        echo "Master IP input: ${ip}"
    else
        echo "Error: IP format error."
        exit 1
    fi
}

function main() {
    DEST="/var/named/standby"
    MIP=$1

    test -d $DEST || mkdir -p $DEST
    date
    scp -pr $MIP:/var/named/data/* $DEST && echo success! || { echo error!; exit 1; } 
    scp -pr $MIP:/etc/named.conf $DEST/named.conf && echo success! || { echo error!; exit 1; } 
    chown -R named:named $DEST
    chown root:named $DEST/named.conf
}

## Main start

if [ $# -ne 1 ]; then
    echo "ERROR: No master ip is provided."
    echo "Usage: scp-from-master.sh x.x.x.x"
    exit 1
fi

Lock
checkIPFormat $1
main $1