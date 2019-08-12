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
normal = "MERGE_NA12891_NA12892.bam"
name = "12878_MERGE_NA12891_NA12892"

command = "java -jar /usr/GenomeAnalysisTK.jar -nct 16 -T MuTect2 -R genome.fa -I:tumor " + tumor + " -I:normal " + normal + "  -o " + name + ".vcf.gz"

tibanna_args = {
      "args": {
        "language": "shell",
        "command": command  , 
        "container_image": "broadinstitute/gatk3:3.8-1",
        "output_S3_bucket": bucket ,
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
                "bucket_name": "eo72-4dn",
                "object_key": path + normal
            },
             "file:///data1/shell/" + normal + ".bai" : {
                "bucket_name": bucket,
                "object_key": path + normal + ".bai"
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
        "instance_type": "c5.9xlarge",
        "log_bucket": "eo72-4dn",
        "ebs_size": 400,
        "EBS_optimized" : True,
        "behavior_on_capacity_limit": "wait_and_retry"

      }
      
    }
print(tibanna_args)
API().run_workflow(input_json= tibanna_args)  # json file or dictionary object
