#!/usr/bin/env python
# Working as of 2024-04-15

import json,csv,os
import requests
import numpy as np
import pandas as pd

# 1. Import courseIDs from provisioning report into list
# 2. Loop through courseIDs as parameter for URI (/api/v1/courses/:course_id/assignments)
    # a. Output ID and name assign_df (using search_term param)
    # b. Join assign_df to courseIDs to create out_df
# 3. Create CSV via out_df.to_csv("output.csv")

headers = {
    'Authorization': 'Bearer <TOKEN>'
}
CSVFileName = "discussion_list.csv" # The name of the discussions CSV file (headers: sis_course_id, discussion_id)
domain = "<DOMAIN>.instructure.com"


#######################################################################################
#######################################################################################
################ Don't edit anything past here unless you know what you are doing.

per_page = 50
id_list = []
course_list = []
discussion_list = []
user_list = []

with open(CSVFileName, 'r') as _f:
    disc_csv = csv.DictReader(_f)

    for disc in disc_csv:
        sis_course_id = disc['sis_course_id']
        discussion_id = disc['discussion_id']

        uri = f"https://{domain}/api/v1/courses/sis_course_id:{sis_course_id}/discussion_topics/{discussion_id}/entries?per_page={per_page}"

        r = requests.get(uri, headers=headers)
        raw = r.json()
        items = len(raw)
        for i in range(0,items):
            id_list.append(raw[i]['id'])
            course_list.append(sis_course_id)
            discussion_list.append(discussion_id)
            user_list.append(raw[i]['user_name'])

        while 'next' in r.links:
            r = requests.get(r.links['next']['url'], headers=headers)
            raw = r.json()
            items = len(raw)
            for i in range(0,items):
                id_list.append(raw[i]['id'])
                course_list.append(sis_course_id)
                discussion_list.append(discussion_id)
                user_list.append(raw[i]['user_name'])

x = pd.DataFrame({"sis_course_id": course_list, "discussion_id": discussion_list, "entry_id": id_list, "user": user_list })
x.to_csv("entry_list.csv")
