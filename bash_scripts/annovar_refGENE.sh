#!/bin/bash
# ETHAN OLIVER


for d in *.vcf ; do
    echo "$d"
    tumor_name="${d%%.*}"
    sbatch -J ANNOTATE -p priopark --account=park_contrib -t 1-0:00:00 -c 1 --mem=2G --wrap="/home/mk446/bin/annovar/table_annovar.pl $d  /home/mk446/bin/annovar/humandb/ -buildver hg19 -out anno_$tumor_name -protocol refGene -operation g  -vcfinput -polish"

done