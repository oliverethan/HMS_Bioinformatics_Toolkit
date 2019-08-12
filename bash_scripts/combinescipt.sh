#!/bin/bash
# ETHAN OLIVER


for d in *.vcf ; do
    # echo $d
    # mv $d indels/$d

    # echo $d
    IFS='.'
    read -ra ADDR <<< "$d"
    fnamer="${ADDR[0]}"
    echo $fnamer
    IFS=' '
    mutect_address="/n/data1/hms/dbmi/park/jake/Chromoplexy/03_Prostate_Baca/MERGE/Mutect/filtered/indels/$fnamer.mutect2_filtered.vcf.gz_indel.vcf"
    strelka_address="/n/data1/hms/dbmi/park/jake/Chromoplexy/03_Prostate_Baca/MERGE/Strelka/filtered/prepped/indels/${fnamer}_tumor.somatic.indels.vcf"

    echo "$mutect_address"
    echo "$strelka_address"
        java -jar /n/data1/hms/dbmi/park/alon/software/gatk/GenomeAnalysisTK-3.8-0-ge9d806836/GenomeAnalysisTK.jar -T CombineVariants \
        -R /n/data1/hms/dbmi/park/jake/Resources/03_pcawg_ref/genome.fa -genotypeMergeOptions PRIORITIZE --rod_priority_list mutect,strelka \
        --variant:mutect "$mutect_address"  \
        --variant:strelka "$strelka_address" \
        -o "/n/data1/hms/dbmi/park/jake/Chromoplexy/03_Prostate_Baca/MERGE/indels/${fnamer}_PRIO_indel.vcf"
done
