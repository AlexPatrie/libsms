#!/usr/bin/env bash

user="$1"

function check_ssh_health {
    user="$1"
    for i in {1..7}; do
        echo "mantis-sub-$i"
        ssh ${user}@mantis-sub-$i.cam.uchc.edu "squeue | head -1"
    done
}

check_ssh_health $user
