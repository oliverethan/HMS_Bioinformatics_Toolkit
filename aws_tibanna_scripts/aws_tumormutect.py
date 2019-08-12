# Ethan Oliver
# Harvard Medical School
# Department of Biomedical Informatics
# Park Lab
# 2019

import boto3
import json
from tibanna.core import API

client = boto3.client('s3')

bucket = "eo72-4dn"

def get_vcflist():
    vcflist = []
    vcf_response = client.list_objects_v2(
        Bucket='eo72-4dn',
        Delimiter='.tbi',
        EncodingType='url',
        Prefix='GATK3_MUTECT',

    )

    while True:
        for file in vcf_response["Contents"]:
            path = file["Key"]
            file = path.split("/")[1]
            name = file[:-7]
            print(name)
            vcflist.append(name)

        if "NextContinuationToken" in vcf_response.keys():
            print(vcf_response["NextContinuationToken"])
            vcf_response = client.list_objects_v2(
                Bucket= bucket,
                Delimiter='.tbi',
                EncodingType='url',
                Prefix='GATK3_MUTECT',
                ContinuationToken= vcf_response["NextContinuationToken"],
            )
        else:
            break;

    return vcflist


def run_tibanna(file, name):

        command = "java -jar /usr/GenomeAnalysisTK.jar -T MuTect2 -R GRCh38.d1.vd1.fa -I:tumor " + file + " -o "+  name + ".vcf.gz"

        tibanna_args = {
              "args": {
                "language": "shell",
                "command": [ "pwd", "ls /", "ls /gatk/",  command]  , 
                "container_image": "broadinstitute/gatk3:3.8-1",
                "output_S3_bucket": bucket,
                "output_target": {
                  "file:///data1/shell/" + name + ".vcf.gz" : "GATK3_MUTECT/" + name + ".vcf.gz",
                  "file:///data1/shell/" + name + ".vcf.gz.tbi" : "GATK3_MUTECT/" + name + ".vcf.gz.tbi"
                  
                },
                "input_files": {
                    "file:///data1/shell/" + file : {
                        "bucket_name": bucket,
                        "object_key": path
                    },
                     "file:///data1/shell/" + name + ".bai" : {
                        "bucket_name": bucket,
                        "object_key": "output/" + name + ".bai"
                    },
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
                "instance_type": "r4.large",
                "log_bucket": bucket,
                "ebs_size": 60,
                "EBS_optimized" : True,
                "behavior_on_capacity_limit": "wait_and_retry",
                "spot_instance": True

              }
              
            }

        API().run_workflow(input_json= tibanna_args)  # json file or dictionary object

vcflist = get_vcflist()

bam_response = client.list_objects_v2(
    Bucket='eo72-4dn',
    Delimiter='.bai',
    EncodingType='url',
    Prefix='output',
    MaxKeys=700,
    ContinuationToken="1Ed/SZibWPJfuLixUKW59Frw09dFQ/iYpEAutMsmpxMreXf06EjVTi5Me4u+LXZZ/oqG9yiqZDpUMwouKU4+qEIJfbgIsXLJ/MYVaZFl94fo="
)

i = 0
for file in bam_response["Contents"]:
        path = file["Key"]
        file = path.split("/")[1]
        name = file[:-4]
        if name in vcflist:
            print("DUPLICATE FOUND")
            continue
        print(i)
        i+=1
        run_tibanna(file, name )












