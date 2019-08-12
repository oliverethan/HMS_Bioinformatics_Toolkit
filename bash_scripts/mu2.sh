#!/bin/bash
# ETHAN OLIVER

tumor_path=$1
echo $tumor_path
tumor_file="$(basename -- $tumor_path)"
echo $tumor_file
tumor_name="${tumor_file%%.*}"
echo "$tumor_name"

normal_path=$2
normal_file="$(basename -- $normal_path)"
normal_name="${normal_file%%.*}"
echo "$normal_name"
sample_name=$(echo $normal_name | cut -d'_' -f 1)  
echo "$sample_name"
sbatch -J mutect2 -p park --account=park_contrib -t 10-0:00:00 --mem=17G --wrap="gatk --java-options \"-Xmx16g\" Mutect2 -R /n/data1/hms/dbmi/park/jake/Resources/03_pcawg_ref/genome.fa -I $tumor_path -tumor $tumor_name -I $normal_path -normal $normal_name  -O $sample_name.mutect2.vcf.gz"
sleep 1