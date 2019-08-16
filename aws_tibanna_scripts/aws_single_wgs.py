import json
from tibanna.core import API



def run_tibanna(region):


        path = "<PATH>"
        bucket = "<BUCKET>"
        format_region = "{:04d}".format(region)
        regionfile = format_region + "-scattered.intervals"


        tumor =  path.split("/")[1]
        out = tumor.split(".")[0] + "_" + format_region


        command = "java -jar /usr/GenomeAnalysisTK.jar -T MuTect2 -R GRCh38_full_analysis_set_plus_decoy_hla.fa -L " + regionfile + " -I:tumor " + tumor + " -o "+  out + ".vcf.gz"
        print(command)
        tibanna_args = {
              "args": {
                "language": "shell",
                "command": command  , 
                "container_image": "broadinstitute/gatk3:3.8-1",
                "output_S3_bucket": bucket,
                "output_target": {
                  "file:///data1/shell/" + out + ".vcf.gz" : "WGS/"+ tumor.split(".")[0]+ "/" + out + ".vcf.gz",
                  "file:///data1/shell/" + out + ".vcf.gz.tbi" : "WGS/"+ tumor.split(".")[0]+ "/" + out + ".vcf.gz.tbi"
                  
                },
                "input_files": {
                    "file:///data1/shell/" + tumor : {
                        "bucket_name": bucket,
                        "object_key": path
                    },
                     "file:///data1/shell/" + tumor + ".bai" : {
                        "bucket_name": bucket,
                        "object_key": path + ".bai"
                    },
                    "file:///data1/shell/" + regionfile: {
                        "bucket_name": bucket,
                        "object_key": "regions/" + regionfile
                    },
                    "file:///data1/shell/" + "GRCh38_full_analysis_set_plus_decoy_hla.fa" : {
                        "bucket_name": bucket,
                        "object_key": "WGS/GRCh38_full_analysis_set_plus_decoy_hla.fa"
                    },
                    "file:///data1/shell/" + "GRCh38_full_analysis_set_plus_decoy_hla.dict" : {
                        "bucket_name": bucket,
                        "object_key": "WGS/GRCh38_full_analysis_set_plus_decoy_hla.dict"
                    },
                    "file:///data1/shell/" + "GRCh38_full_analysis_set_plus_decoy_hla.fa.fai" : {
                        "bucket_name": bucket,
                        "object_key": "WGS/GRCh38_full_analysis_set_plus_decoy_hla.fa.fai"
                    }
                }
              },
              "config": {
                "instance_type": "r4.large",
                "log_bucket": bucket,
                "ebs_size": 150,
                "EBS_optimized" : True,
                "behavior_on_capacity_limit": "wait_and_retry"

              }
              
            }
        print(json.dumps(tibanna_args, indent = 4))
        API().run_workflow(input_json= tibanna_args)

run_tibanna(96)