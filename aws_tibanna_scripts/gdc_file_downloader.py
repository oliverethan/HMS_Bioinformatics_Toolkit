# Ethan Oliver
# Harvard Medical School
# Department of Biomedical Informatics
# Park Lab
# 2019

import requests
import json

fields = [
    "cases.samples.sample_type",
    "type",
    "data_format",
    "data_type",
    "file_name",
    "file_id",
    "access",
    "acl,"
    "experimental_strategy",
    "data_category",
    "state"
    ]

fields = ",".join(fields)
cases_endpt = "https://api.gdc.cancer.gov/files"

filters = {
    "op": "and",
    "content":[
        {
        "op": "in",
        "content":{
            "field": "cases.samples.sample_type",
            "value": ["Blood Derived Normal"]
            }
        },
        {
        "op": "in",
        "content":{
            "field": "data_type",
            "value": ["Aligned Reads"]
            }
        },
        {
        "op": "in",
        "content":{
            "field": "experimental_strategy",
            "value": ["WXS"]
            }
        }
    ]
}

params = {
    "filters": json.dumps(filters),
    "fields": fields,
    "format": "JSON",
    'sort':'file_name:asc',
    "size": 500,
    "from": 1756,
    }

response = requests.get(cases_endpt, params = params)
DATA = response.json()

arr = DATA["data"]["hits"]
print("length: ", len(arr))

bucket = "eo72-4dn"

i = 0
for val in arr:
    file_id = val["id"]
    print(file_id, "Count: ", i )
    i = i+1
    # TIBANNA SECTION
    tibanna_args = {
      "args": {
        "language": "shell",
        "command": ["wget https://gdc.cancer.gov/system/files/authenticated%20user/0/gdc-client_v1.4.0_Ubuntu_x64.zip",
                        "echo \"<TOKEN>\" > TOKEN.txt",
                    "unzip  gdc-client_v1.4.0_Ubuntu_x64.zip", "./gdc-client download -t TOKEN.txt " + file_id ]  , 
        "container_image": "4dndcic/ubuntu16.04-python27-pip19:v1",
        "output_S3_bucket": bucket,
        "output_target": {
          "file:///data1/shell/" + file_id + "/": "output/"
        }
      },
      "config": {
        "instance_type": "t3.nano",
        "log_bucket": bucket,
        "ebs_size": 45,
        "EBS_optimized" : True,
        "behavior_on_capacity_limit": "wait_and_retry"

      },
      "input_files": {
            "file:///data1/shell/token.txt": {
                "bucket_name": bucket,
                "object_key": "token.txt"
            }
        }
    }

    from tibanna.core import API
    API().run_workflow(input_json= tibanna_args)  # json file or dictionary object
