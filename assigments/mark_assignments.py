#!/usr/bin/env python
# Working as of 2024-04-15

import json,csv,os
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

CSVFileName = "assignment_list.csv" # path of input CSV (sis_course_id, assignment_id)
domain = "<DOMAIN>.instructure.com"
studentIDs=["<ID1>", "<ID2>"] # array of sis_user_ids
markerID = "<ID>" # sis ID of teacher/marker
grade = "<GRADE>" # grade assigned (numeric, 'complete'/'incomplete', etc)
comment = "<TEXT COMMENT>"


#######################################################################################
#######################################################################################
################ Don't edit anything past here unless you know what you are doing.

def canvasReq(uri):
  result = requests.put(uri, headers=headers, data=form_data, stream=True)
  return result.status_code

def buildArray():
  form_data={
  'comment[text_comment]' : comment,
  'submission[posted_grade]' : grade
  }
  uri_list = []
  with open(CSVFileName, 'r') as _f:
    submission_csv = csv.DictReader(_f)
    for submission in submission_csv:
      sis_course_id = submission['sis_course_id']
      assignment_id = submission['assignment_id']
      for student in studentIDs:
        uri = f"https://{domain}/api/v1/courses/sis_course_id:{sis_course_id}/assignments/{assignment_id}/submissions/sis_user_id:{student}?as_user_id=sis_user_id:{markerID}"
        uri_list.append(uri)

if __name__ == '__main__':
  buildArray()
  processes = []

  with ThreadPoolExecutor(max_workers=10) as executor:
    for uri in uri_list:
      processes.append(executor.submit(canvasReq, uri))

  for task in as_completed(processes):
    print(task.result())