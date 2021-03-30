import requests
import json
import re
import os

file_list = "out_1_getFileList_ByCase.tsv"

with open(file_list, "r") as fh:
    for line in fh:
        #print(line)
        ln = line.rstrip().split("\t")
        # print(ln)
        if ln[0] == "submitter_id": # skip header line
            continue

        file_id = ln[-5]
        # print(file_id)
        data_endpt = "https://api.gdc.cancer.gov/data/{}".format(file_id)
        response = requests.get(data_endpt, headers = {"Content-Type": "application/json"})

        # The file name can be found in the header within the Content-Disposition key.
        response_head_cd = response.headers["Content-Disposition"]

        file_name = re.findall("filename=(.+)", response_head_cd)[0]
        # print(os.getcwd())
        os.chdir('./GDC_DATA/')
        with open(file_name, "wb") as output_file:
            output_file.write(response.content)
        os.chdir('../')
