import boto3
import json
from tibanna.core import API


path = "WGS/"

tumor_folder = "<FOLDER_NAME>"
bucket = "<BUCKET>"



inputlist = "vcf.list"

makelist = "find VCFS/ -name \"*.gz\" >  unsorted"
sortlist = "sort unsorted > " + inputlist

command = "gatk GatherVcfs -I " + inputlist + " -O " + tumor_folder + ".vcf.gz"
index = " gatk IndexFeatureFile -F " + tumor_folder + ".vcf.gz"
print(command)
tibanna_args = {
      "args": {
        "language": "shell",
        "command": [makelist, sortlist, command, index]  , 
        "container_image": "broadinstitute/gatk:latest",
        "output_S3_bucket": bucket,
        "output_target": {
          "file:///data1/shell/" + tumor_folder + ".vcf.gz" : path + tumor_folder + ".vcf.gz",
          "file:///data1/shell/" + tumor_folder + ".vcf.gz.tbi" : path + tumor_folder + ".vcf.gz.tbi"
          
        },
        "input_files": {
            "file:///data1/shell/VCFS/" : "s3://eo72-4dn/" + path + tumor_folder,
        }
      },
      "config": {
        "instance_type": "c5.xlarge",
        "log_bucket": bucket,
        "ebs_size": 100,
        "EBS_optimized" : True,
        "behavior_on_capacity_limit": "wait_and_retry"

      }
      
    }
print(tibanna_args)
API().run_workflow(input_json= tibanna_args)  # json file or dictionary object