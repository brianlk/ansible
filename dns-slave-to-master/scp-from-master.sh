#!/bin/bash

#
# Run the script in standby node
#
trap "rm -rf /tmp/scpxxx.lock" SIGINT SIGKILL SIGTERM

function Lock() {
    exec 200>/tmp/scpxxx.lock
    flock -n 200 || { echo "Error: anthoer $0 is running."; exit 1; }
}

function main() {
    Lock
    #exec 1>>/tmp/scp-from-master.log
    #exec 2>&1

    DEST="/var/named/standby"
    MIP=$1

    test -d $DEST || mkdir -p $DEST
    date
    scp -pr $MIP:/var/named/data/* $DEST && echo success!
    scp -pr $MIP:/etc/named.conf $DEST/named.conf && echo success!
    chown -R named:named $DEST
    chown root:named $DEST/named.conf
}

if [ $# -ne 1 ]; then
    echo "ERROR: No master ip is provided."
    exit 1
fi

main
# while true
# do
#     main
#     sleep 60
# done