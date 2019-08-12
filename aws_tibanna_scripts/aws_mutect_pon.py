# Ethan Oliver
# Harvard Medical School
# Department of Biomedical Informatics
# Park Lab
# 2019

import boto3
import json
from tibanna.core import API

bucket = "eo72-4dn"

path = "FAMILY_BAM/"

tumor = "12878_30x_simulated.right.bam"
normal = "PON_LIFTOVER_DIRECT.vcf"
name = "12878_PON"

command = "java -jar /usr/GenomeAnalysisTK.jar -T MuTect2 -R genome.fa -I:tumor " + tumor +  " --normal_panel "+ normal  + "  -o " + name + ".vcf.gz"

tibanna_args = {
      "args": {
        "language": "shell",
        "command": ["gzip -d PON_100.vcf.gz", command]  , 
        "container_image": "broadinstitute/gatk3:3.8-1",
        "output_S3_bucket": bucket,
        "output_target": {
          "file:///data1/shell/" + name + ".vcf.gz" : path + name + ".vcf.gz",
          "file:///data1/shell/" + name + ".vcf.gz.tbi" : path + name + ".vcf.gz.tbi"
          
        },
        "input_files": {
            "file:///data1/shell/" + tumor : {
                "bucket_name": bucket,
                "object_key": path + tumor
            },
             "file:///data1/shell/" + tumor + ".bai" : {
                "bucket_name": bucket,
                "object_key": path + tumor + ".bai"
            },
             "file:///data1/shell/" + normal : {
                "bucket_name": bucket,
                "object_key": "PON/" + normal
            },
             "file:///data1/shell/" + normal +".idx": {
                "bucket_name": bucket,
                "object_key": "PON/" + normal +".idx"
            },
        "file:///data1/shell/" + "genome.fa.fai" : {
                "bucket_name": bucket,
                "object_key": "FASTA/genome.fa.fai"
            },
            "file:///data1/shell/" + "genome.dict" : {
                "bucket_name": bucket,
                "object_key": "FASTA/genome.dict"
            },
            "file:///data1/shell/" + "genome.fa" : {
                "bucket_name": bucket,
                "object_key": "FASTA/genome.fa"
            }   
        }
      },
      "config": {
        "instance_type": "r5.xlarge",
        "log_bucket": bucket,
        "ebs_size": 70,
        "EBS_optimized" : True,
        "behavior_on_capacity_limit": "wait_and_retry"

      }
      
    }
print(tibanna_args)
API().run_workflow(input_json= tibanna_args)  # json file or dictionary object