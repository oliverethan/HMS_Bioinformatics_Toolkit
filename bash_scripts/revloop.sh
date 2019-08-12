#!/bin/bash
# ETHAN OLIVER


for d in  .[^.]*; do
    echo $d
    IFS='.'
    read -ra ADDR <<< "$d"
    fnamer="${ADDR[1]}"
    IFS=' '

    cd "$d/.sh/results/variants"
    pwd
    for e in *.gz; do
        echo $e
        echo "Name: $fnamer"
        new_name="$fnamer.$e"
        echo $new_name
        cp $e "/n/data1/hms/dbmi/park/jake/Chromoplexy/05_Breast_Jones/02_Strelka2/$new_name"
    done

    cd ../../../../
done









