#!/bin/bash
# ETHAN OLIVER

mkdir prepped

for d in *.gz ; do
    #python3 /n/data1/hms/dbmi/park/alon/command_line_tools/PreProcessing/PreProcessing_new.py -in_dir "$d" -out "$d"
    #echo "DIRECTORY"mee
    echo $d
    zcat $d | awk '{if(/^##/) print; else if(/^#/) print "##FORMAT=<ID=GT,Number=1,Type=String,Description=\"Genotype\">\n"$0; else print $1"\t"$2"\t"$3"\t"$4"\t"$5"\t"$6"\t"$7"\t"$8"\tGT:"$9"\t./.:"$10"\t./.:"$11;}' - > ./prepped/$d
