#!/bin/bash
# ETHAN OLIVER

for d in *.vcf  ; do
    #python3 /n/data1/hms/dbmi/park/alon/command_line_tools/PreProcessing/PreProcessing_new.py -in_dir "$d" -out "$d"
    echo "$d"
    echo
    grep -i $1 $d
    echo
done