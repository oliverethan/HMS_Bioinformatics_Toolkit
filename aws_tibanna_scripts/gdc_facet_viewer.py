# Ethan Oliver
# Harvard Medical School
# Department of Biomedical Informatics
# Park Lab
# 2019

import requests
import json

filters = {
    "op": "and",
    "content":[
        {
        "op": "in",
        "content":{
            "field": "experimental_strategy",
            "value": ["WXS"]
            }
        },
        {
        "op": "in",
        "content":{
            "field": "data_type",
            "value": ["Aligned Reads"]
            }
        }
    ]
}

projects_endpt = 'https://api.gdc.cancer.gov/files'
params = {
        "filters": json.dumps(filters),
        'facets':'access',
          'from':0, 'size':0,
          'sort':'program.name:asc'}
response = requests.get(projects_endpt, params = params)
print (json.dumps(response.json(), indent=2))
