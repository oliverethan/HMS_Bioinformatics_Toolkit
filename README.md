# Bioinformatics Toolkit (WIP)
## Created during a summer internship at the Park Lab in the Department of Biomedical Informatics (DBMI) at Harvard Medical School

Summer 2019

Various tools and scripts to help prep and analyze genomics data for research purposes. Some of the scripts have not been fully tested and may require slight modification to function correctly in your workspace.

## Languages
* Python
* R
* bash

## Main Frameworks/Tools used
* Slurm
* GATK
* Tibanna
* AWS
* Docker
* Picard
* bcftools
* samtools

### Mutect2
These scripts create and submit custom slurm jobs to run GATK Mutect2 in its various modes. They setup the output files and shell script and can accept a single file or an entire folder and create multiple slurm jobs seamlessly. Mutect modes supported: Normal Mutect, Mutect tumor-only mode and PON creation, FilterMutectCalls.

PYTHON -> SLURM -> GATK -> MUTECT2


### Amazon Web Service (AWS) scripts
Scripts to run Mutect2 on AWS EC2 instances using the Tibanna framework and Docker images. Easily customizable and can run Mutect2 in multiple ways. Used to create a Panel of Normals of 1000 WES patients for use in the lab. Also features scripts to programmatically download large amounts of files from the Genomics Data Commons into AWS.

### Sequenza
These scripts aid in running Sequenza through slurm. Generate WIGGLE file and run Sequenza. Also features an R script to run further analysis on the Sequenza output.

### SigMA
R script pipeline that goes from VCFs to SigMA output. R scripts to create plots of various types based on SigMA output

### VCF Manipulation
Various Scripts to automate slurm jobs creation for popular VCF manipulation tools: CombineVariants, DepthOfCoverage, MergeVcfs, SelectVariants (Removal of filtered variants), RenameSampleInVcf, SplitVcfs (indel, snp)

### Multilane Preproccessing Scripts
Scripts to go from FASTQ to mapped BAM of multilane sequencing data using GATK best practices and slurm to automate job creation.

### Bash Scripts
Random bash scripts and bits of code that were useful throughout the whole research process. For reference only.




