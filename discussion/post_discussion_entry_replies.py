#!/usr/bin/env python
# Working as of 2024-04-17

import json,os, csv
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests

"""
 You will need to edit several variables here at the top of this script. 
 token = the access token from Canvas
 CSVFileName = the full path of CSV file 
 domain = the full domain name you use to access canvas. (i.e. something.instructure.com)
"""

headers = {
    'Authorization': 'Bearer <TOKEN>'
} 

CSVFileName = "entry_list.csv" # full path of input CSV (sis_course_id, discussion_id, entry_id)
domain = "<DOMAIN>.instructure.com"

user1="USER1 SIS ID"
message1 = "<MESSAGE 1>"

#######################################################################################
#######################################################################################
################ Don't edit anything past here unless you know what you are doing.
uri_list1 = []
form_data1={'message' : message1}

def canvasReq1(uri):
  result = requests.post(uri, headers=headers, data=form_data1, stream=True)
  return result.status_code

def buildArray():
  with open(CSVFileName, 'r') as _f:
    entry_csv = csv.DictReader(_f)
    for entry in entry_csv:
      sis_course_id = entry['sis_course_id']
      discussion_id = entry['discussion_id']
      entry_id = entry['entry_id']
      uri = f"https://{domain}/api/v1/courses/sis_course_id:{sis_course_id}/discussion_topics/{discussion_id}/entries/{entry_id}/replies?as_user_id=sis_user_id:{user1}"
      uri_list1.append(uri)

if __name__ == '__main__':
  buildArray()
  processes = []

  with ThreadPoolExecutor(max_workers=10) as executor:
    for uri in uri_list1:
      processes.append(executor.submit(canvasReq1, uri))

  for task in as_completed(processes):
    print(task.result())
