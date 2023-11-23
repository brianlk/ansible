#!/bin/bash


function ChangeIP() {
    exec 1>out.log 2>&1 
    ip addr
    exec &1- &2-
}

function ConvertToMaster() {
    echo "bbbbbbbbbb"
}


function main() {
    out=$(readlink /dev/fd/1)
    err=$(readlink /dev/fd/2)
    clear
    printf "\t\t\tMenu\n\n"
    printf "\t\t\t1. Change current IP to master IP\n\n"
    printf "\t\t\t2. Convert standby to master\n\n"
    echo -n "Choice? "
    read c
    case $c in
            1)
                ChangeIP
                exec 1>$out 2>&1
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
