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
bn = "/usr/local/bin/"

bed = "12878_PON_SUB.bed"
bam = "12878_30x_simulated.right.bam"
model = "50xRFmodel_addRMSK_Refine.rds"
readlevel_outfile = "12878_out"

gzip = "gunzip " + bn + "hs37d5.fa.gz"
mkdir = "mkdir bam"
mv = "mv " + bam + " bam"
mv_index = "mv " + bam + ".bai bam"

readlevel = bn + "ReadLevel_Features_extraction.py " + bed + " "+ readlevel_outfile + " bam " + bn + "hs37d5.fa " + bn + "k24.umap.wg.bw 150 16 "
prediction = "Rscript " + bn + "Prediction.R " + readlevel_outfile + " " + model + " " + readlevel_outfile + "_prediction"

tibanna_args = {
      "args": {
        "language": "shell",
        "command": [gzip, mkdir, mv, mv_index, readlevel, prediction]  , 
        "container_image": "yanmei/mosaicforecast:0.0.1",
        "output_S3_bucket": bucket,
        "output_target": {
          "file:///data1/shell/" + readlevel_outfile : path + readlevel_outfile,
          "file:///data1/shell/" + readlevel_outfile + "_prediction" : path + readlevel_outfile  + "_prediction"         
        },
        "input_files": {
            "file:///data1/shell/" + bam : {
                "bucket_name": bucket,
                "object_key": path + bam
            },
             "file:///data1/shell/" + bam + ".bai" : {
                "bucket_name": bucket,
                "object_key": path + bam + ".bai"
            },
             "file:///data1/shell/" + bed : {
                "bucket_name": bucket,
                "object_key": path + bed
            },
             "file:///data1/shell/" + model : {
                "bucket_name": bucket,
                "object_key": path + model
            }
        }
      },
      "config": {
        "instance_type": "c5.4xlarge",
        "log_bucket": bucket,
        "ebs_size": 100,
        "root_ebs_size": 50,
        "EBS_optimized" : True,
        "behavior_on_capacity_limit": "wait_and_retry"

      }
      
    }
print(json.dumps(tibanna_args, indent = 4))
API().run_workflow(input_json= tibanna_args)  # json file or dictionary object