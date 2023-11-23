#!/bin/bash

function ChangeIP() {
    echo "aaaa"
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
