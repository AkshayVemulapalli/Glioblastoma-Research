import requests
import json
import sys

file_type = "htseq" # to filter by file name
outfile = "gbm_files_byCase.tsv"

out = open(outfile, "w")

# available fields are here -> https://docs.gdc.cancer.gov/API/Users_Guide/Appendix_A_Available_Fields/#case-fields
fields = [
    "submitter_id",
    "case_id",
    "files.file_name",
    "files.file_id"
]

cases_endpt = "https://api.gdc.cancer.gov/cases"

filters = {
    "op": "in",
    "content":{
        "field": "primary_site",
        "value": ["Brain"]
        }
    }

# With a GET request, the filters parameter needs to be converted
# from a dictionary to JSON-formatted string

params = {
    "filters": json.dumps(filters),
    "fields": ",".join(fields),
    "format": "json",
    "size": "1000" # change limit if you want more
    }

response = requests.get(cases_endpt, params = params)
res = response.json()

# print header
out.write("\t".join(fields))
out.write("\n")
# iterate over the data
for hit in res["data"]["hits"]:
    if hit["submitter_id"].startswith("TCGA"): # add filters in elements
        if "files" in hit:
            for file in hit["files"]:
                if file_type in file["file_name"]:
                    out.write("\t".join([ hit["case_id"], file["file_name"], file["file_id"] ]))
                    out.write("\n")

out.close()
