#!/usr/bin/env bash

function error_msg() {
    local MSG="${1}"
    echo "${MSG}"
    exit 1
}

function check_root() {
    if [ "$(id -u)" != "0" ]; then
        usage
        exit 1
    fi
}

function check_virt_win_reg() {
    which virt-win-reg &>/dev/null || apt-get install libguestfs-tools
}

function usage() {
    echo "Usage: sudo ${0} WINDOWS_IMAGE"
    echo 
    echo "This script applies the mergeide.reg to a kvm compatible image."
    echo "It uses libguestfs-tools internally to do that."
    echo
    echo "If the control set of the registry hive is not 001, "
    echo "mergeide_create_reg.py can create the prober one." 
}

OPTSTRING=h
while getopts ${OPTSTRING} OPT
do
    case ${OPT} in
        h) usage;;
    esac
done

check_virt_win_reg
check_root

if [ -z "$1" ]; then
    usage
    exit 1
fi

SCRIPT=`readlink -e $0`
SCRIPTDIR=`dirname $SCRIPT`
IMG=`readlink -e $1`

cd $SCRIPTDIR

# Maybe extract the currentcontrolset from windows registry
# ./mergeide_create_reg.py "$IMG"

virt-win-reg --merge "$IMG" $SCRIPTDIR/mergeide.reg
