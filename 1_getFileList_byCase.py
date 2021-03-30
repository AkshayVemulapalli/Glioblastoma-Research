import requests
import json
import sys

file_type = "htseq" # to filter by file name
vital_status_dead = "Dead"
alive_days = 2700  # Using 2700 which is higher than max Days to Death (2681) found in data so far
outfile = "out_1_getFileList_ByCase.tsv"

out = open(outfile, "w")

# available fields are here -> https://docs.gdc.cancer.gov/API/Users_Guide/Appendix_A_Available_Fields/#case-fields
fields = [
    "project.project_id",
    "submitter_id",
    "case_id",
    "diagnoses.age_at_diagnosis",
    "demographic.vital_status",
    "demographic.days_to_death",
    "demographic.race",
    "demographic.gender",
    "files.file_name",
    "files.file_id"
]

cases_endpt = "https://api.gdc.cancer.gov/cases"


filters = {
    "op": "in",
    "content":{
        "field": "project.project_id",
        "value": ["TCGA-GBM"]
        }
    }



# With a GET request, the filters parameter needs to be converted
# from a dictionary to JSON-formatted string

params = {
    "filters": json.dumps(filters),
    "fields": ",".join(fields),
    "format": "json",
    "size": "10000" # change limit if you want more
    }

response = requests.get(cases_endpt, params = params)
res = response.json()
# print(res)
# print header
out.write("\t".join([ "submitter_id", "case_id", "file_name", "file_id", "days_to_death", "gender", "race", "num_htseq_files" ]))
out.write("\n")

# iterate over the data
for hit in res["data"]["hits"]:
    if hit["project"]["project_id"].startswith("TCGA-GBM"): # For TCGA-GBM cases
        htseqnum=0
        if "files" in hit: #This case has files
            for file in hit["files"]:
                if file_type in file["file_name"]: #For each HTSEQ file found do following. There are cases with multiple HTSEQ files
                    htseqnum += 1
                    if "demographic" in hit: #This case has demographic fields
                        if vital_status_dead in hit["demographic"]["vital_status"]: #patient is DEAD
                            out.write("\t".join([ hit["submitter_id"], hit["case_id"], file["file_name"], file["file_id"], str(hit["demographic"]["days_to_death"]), hit["demographic"]["gender"], hit["demographic"]["race"][0:5], "htseq_filenum="+str(htseqnum) ]))
                            # out.write("\t".join([ hit["submitter_id"], hit["case_id"], file["file_name"], file["file_id"] ]))
                            out.write("\n")
                        else: #patient is ALIVE
                            out.write("\t".join([ hit["submitter_id"], hit["case_id"], file["file_name"], file["file_id"], str(alive_days), hit["demographic"]["gender"], hit["demographic"]["race"][0:5], "htseq_filenum="+str(htseqnum) ]))
                            out.write("\n")
                    # else: #This case does NOT have demographic fields
                    #     out.write("\t".join([ hit["submitter_id"], hit["case_id"], file["file_name"], file["file_id"], "NoData", "NoData", "NoData", "htseq_filenum="+str(htseqnum) ]))
                    #     out.write("\n")
            # if htseqnum < 1: #This case does not have any HTSEQ files
            #     out.write("\t".join([ hit["submitter_id"], hit["case_id"], "No_HTSEQ_file", "No_HTSEQ_file", "Days to Death??", hit["demographic"]["gender"], hit["demographic"]["race"], "htseq_filenum="+str(htseqnum) ]))
            #     out.write("\n")
        # else: #This case does NOT have any files
        #     out.write("\t".join([ hit["submitter_id"], hit["case_id"], "No_FILES", "No_FILES", "Days to Death??" ]))
        #     out.write("\n")

out.close()