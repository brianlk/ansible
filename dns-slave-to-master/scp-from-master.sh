#!/bin/bash

exec 1>>/tmp/scp-from-master.log 
exec 2>&1


if [ $# -ne 1 ]; then
    echo "ERROR: No master ip is provided."
    exit 1
fi

DEST="/var/named/standby"
MIP=$1

test -d $DEST || mkdir -p $DEST
date
scp -pr $MIP:/var/named/data/* $DEST
scp -pr $MIP:/etc/named.conf /etc/named.conf
chown -R named:named $DEST
