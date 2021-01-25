#!/bin/bash
# flush_logs.sh
#
# Delete contents of app/logs/
shopt -s nullglob
for file in app/logs/log.txt; do
    rm $file
    echo $file "removed"
done