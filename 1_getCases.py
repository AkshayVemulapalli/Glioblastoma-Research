import requests
import json
import sys

# available fields are here -> https://docs.gdc.cancer.gov/API/Users_Guide/Appendix_A_Available_Fields/#case-fields
fields = [
    "submitter_id",
    "case_id",
    "primary_site",
    "disease_type",
    "demographic.ethnicity",
    "demographic.gender",
    "demographic.race",
    "demographic.state",
    "demographic.year_of_birth",
    "demographic.year_of_death",
    "diagnoses.age_at_diagnosis",
    "diagnoses.classification_of_tumor",
    "diagnoses.days_to_birth",
    "diagnoses.days_to_death",
    "diagnoses.days_to_recurrence",
    "diagnoses.morphology",
    "diagnoses.primary_diagnosis",
    "diagnoses.prior_malignancy",
    "diagnoses.progression_or_recurrence",
    "diagnoses.site_of_resection_or_biopsy",
    "diagnoses.state",
    "diagnoses.tumor_grade",
    "diagnoses.tumor_stage"
]

outfile = "gbm_cases.tsv"
out = open(outfile, "w")
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
        data = []
        for field in fields:
            if field.startswith("demographic"): # this is a dict
                if "demographic" in hit:
                    d = field.split(".")
                    if d[1] in hit["demographic"]:
                        data.append(str(hit["demographic"][ d[1] ]))
                    else:
                        data.append("NA")
                else:
                    data.append("NA")
            elif field.startswith("diagnoses"): # diagnoses is an array of dicts
                if "diagnoses" in hit:
                    d = field.split(".")
                    if d[1] in hit["diagnoses"][0]:
                        data.append(str(hit["diagnoses"][0][d[1]]))
                    else:
                        data.append("NA")
                else:
                    data.append("NA")
            elif field in hit:
                data.append(str(hit[field]))
            else:
                data.append("NA") # missing data will be NA
        out.write("\t".join(data))
        out.write("\n")

out.close()