
sbatch -J PON_AWS -p park --account=park_contrib -t 1-0:00:00 --mem=20G --wrap="java -jar /n/data1/hms/dbmi/park/alon/software/gatk/GenomeAnalysisTK-3.8-0-ge9d806836/GenomeAnalysisTK.jar -T CombineVariants -R /n/data1/hms/dbmi/park/ethan/GRCh38/GRCh38.d1.vd1.fa --variant vcf.list  -minN 2 --setKey \"null\" --filteredAreUncalled --filteredrecordsmergetype KEEP_IF_ANY_UNFILTERED -o PON_100.vcf.gz"

sbatch -J WIGGLE -p park --account=park_contrib -t 1-0:00:00 --mem=4G --wrap="sequenza-utils gc_wiggle -f /n/data1/hms/dbmi/park/jake/Resources/03_pcawg_ref/genome.fa -o WIGGLE"


sbatch -J PON -p priopark --account=park_contrib -t 5-0:00:00 -c 8 --mem=16G --wrap="java  -jar /n/data1/hms/dbmi/park/alon/software/gatk/GenomeAnalysisTK-3.8-0-ge9d806836/GenomeAnalysisTK.jar -nt 8 -T CombineVariants -R /n/data1/hms/dbmi/park/jake/Resources/03_pcawg_ref/genome.fa --variant vcf.list -minN 2 --setKey \"null\" --filteredAreUncalled --filteredrecordsmergetype KEEP_IF_ANY_UNFILTERED  -o PONBETTER_GERBURG.vcf.gz"

sbatch -J PON -p priopark --account=park_contrib -t 5-0:00:00 -c 8 --mem=16G --wrap="gatk CreateSomaticPanelOfNormals --vcfs vcf.list  -O PON_GERBURG.vcf.gz"


sbatch -J MERGE -p priopark --account=park_contrib -t 1-0:00:00 -c 8 --mem=10G --wrap="java -jar /n/data1/hms/dbmi/park/alon/software/picard.jar MergeSamFiles I=NA12891_30x.bam  I=NA12892_30x.bam O=NA12891_NA12892_MERGED.bam"

sbatch -J UPDATE -p priopark --account=park_contrib -t 2-0:00:00 -c 4 --mem=20G --wrap="CrossMap.py bam  GRCh37_to_GRCh38.chain.gz bam/hide/12878_30x_simulated.right.bam Updated.bam"


sbatch -J HEADER -p priority  -t 1-0:00:00 -c 8 --mem=10G --wrap="java -jar /n/data1/hms/dbmi/park/alon/software/picard.jar ReplaceSamHeader I=/n/data1/hms/dbmi/park/ethan/NEW_PROJECT/bam/hide/12878_30x_simulated.right.bam  HEADER=/n/data1/hms/dbmi/park/ethan/NEW_PROJECT/bam/TCGA-FA-A82F-10A-01D-A385-10_Illumina_gdc_realn.bam O=HEADER_FIX12878.bam"

sbatch -J INDEX -p priopark --account=park_contrib -t 2-0:00:00 -c 4 --mem=20G --wrap="samtools sort  12878_UPDATED.bam -o  12878_UPDATED_SORTED.bam"


sbatch -J CROSSMAP -p priority -t 2-0:00:00 -c 1 --mem=20G --wrap="CrossMap.py vcf ~/filelink/hg19ToGRCh37.over.chain.gz PON_LIFTOVER.vcf /n/data1/hms/dbmi/park/jake/Resources/03_pcawg_ref/genome.fa PON_FINAL.vcf"

sbatch -J CHAIN -p priority -t 2-0:00:00 -c 1 --mem=20G --wrap="java -jar /n/data1/hms/dbmi/park/alon/software/picard.jar LiftoverVcf I=PON_LIFTOVER.vcf  CHAIN=/home/eo72/filelink/hg19ToGRCh37.over.chain.gz REJECT=REJECT_DIRECT.vcf O=PON_LIFTOVER_DIRECT.vcf R=/n/data1/hms/dbmi/park/jake/Resources/03_pcawg_ref/genome.fa"
