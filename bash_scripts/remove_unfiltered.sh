#!/bin/bash
# ETHAN OLIVER


i=0
mkdir filtered

for d in *.gz ; do
        i=$((i+1))
        echo $d
        echo $i
        bcftools view $d -f PASS -G -Oz > "filtered/$d"
        bcftools index -t "filtered/$d"
done
 