# Ethan Oliver
# Harvard Medical School
# Department of Biomedical Informatics
# Park Lab
# 2019

import boto3
import json
from tibanna.core import API

bucket = "eo72-4dn"

output = "PON_1000_5"
options = " -minN 5 --setKey \"null\" --filteredAreUncalled --filteredrecordsmergetype KEEP_IF_ANY_UNFILTERED"
command = "java -Xmx100g  -jar /usr/GenomeAnalysisTK.jar -nt 16 -T CombineVariants -R GRCh38.d1.vd1.fa " + "--variant vcf.list " + options + " -o " + output + ".vcf.gz"

tibanna_args = {
      "args": {
        "language": "shell",
        "command": [ "find VCFS/ -name \"*.gz\" > vcf.list", command]  , 
        "container_image": "broadinstitute/gatk3:3.8-1",
        "output_S3_bucket": bucket,
        "output_target": {
            "file:///data1/shell/" + output + ".vcf.gz" : "PON/" + output + ".vcf.gz",
            "file:///data1/shell/" + output + ".vcf.gz.tbi" : "PON/" + output + ".vcf.gz.tbi"
        },
        "input_files": {
            "file:///data1/shell/VCFS/" : "s3://eo72-4dn/PON_1000",
            "file:///data1/shell/" + "GRCh38.d1.vd1.fa.fai" : {
                   "bucket_name": bucket,
                   "object_key": "FASTA/GRCh38.d1.vd1.fa.fai"
               },
               "file:///data1/shell/" + "GRCh38.d1.vd1.dict" : {
                   "bucket_name": bucket,
                   "object_key": "FASTA/GRCh38.d1.vd1.dict"
               },
               "file:///data1/shell/" + "GRCh38.d1.vd1.fa" : {
                   "bucket_name": bucket,
                   "object_key": "FASTA/GRCh38.d1.vd1.fa"
               }
        }
      },
      "config": {
        "instance_type": "r5.4xlarge",
        "log_bucket": bucket,
        "ebs_size": 60,
        "EBS_optimized" : True,
        "behavior_on_capacity_limit": "wait_and_retry"

      }
      
    }

API().run_workflow(input_json= tibanna_args)  # json file or dictionary object