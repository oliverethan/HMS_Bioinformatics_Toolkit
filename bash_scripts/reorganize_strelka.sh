#!/bin/bash
# ETHAN OLIVER


path=$(pwd)


for d in  .[^.]*; do
    echo $d
    IFS='.'
    read -ra ADDR <<< "$d"
    fnamer="${ADDR[1]}"
    IFS=' '

    cd "$d/.sh/results/variants"
    for e in *.gz; do
        echo $e
        echo "Name: $fnamer"
        new_name="$fnamer.$e"
        echo $new_name
        cp $e "$path/$new_name"
    done

    cd ../../../../
done









