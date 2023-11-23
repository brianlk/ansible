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
    nmcli conn show
    ResetLog
    read masterip
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
