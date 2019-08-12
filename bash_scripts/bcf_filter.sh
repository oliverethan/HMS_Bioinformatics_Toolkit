#!/bin/bash
# ETHAN OLIVER




for d in *.vcf.gz ; do
    echo $d
        # bcftools view $d -H -G -i 'FORMAT/AD[0:0] > 10  && FORMAT/AD[1-:1] > 4'
        # bcftools view $d -h  > gerburg_10_vaf_4/$d
        # bcftools view $d -H -i 'FORMAT/AD[1-:1] > 4' >> gerburg_lower/$d
        bcftools view $d  -i 'FORMAT/AD[0:0] > 10 && FORMAT/AD[1-:0] + FORMAT/AD[1-:1] > 10 && FORMAT/AD[1-:1] > 4' > gerburg_10_vaf_4/$d
        # bcftools concat -a -D  "$d"  "/n/data1/hms/dbmi/park/ethan/GERBURG/PON_MUTECT/filtered/gerburg_10_vaf_4/$d" -o "../COMMON_PON/$d"
        # bgzip $d
        # bcftools sort "$d" -o "../$d"
        # bcftools index "$d.gz"
done