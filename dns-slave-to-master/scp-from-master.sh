#!/bin/bash

if [ $# -ne 1 ]; then
    echo "ERROR: No master ip is provided."
    exit 1
fi

DEST="/var/named/standby"
MIP=$1

test -d $DEST || ( mkdir -p $DEST && chown named:named $DEST )
scp -pr $MIP:/var/named/data/* $DEST
scp -pr $MIP:/etc/named.conf /etc/named.conf
