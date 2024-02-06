#!/usr/bin/env python
# Working as of 2024-02-06

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

CSVFileName = "input.csv" # full path of input CSV (course_id, assignment_id)
domain = "<DOMAIN>.instructure.com"
file= "test.pdf"
folder="assignments"
studentIDs=[""] # array of student SIS IDs


#######################################################################################
#######################################################################################
################ Don't edit anything past here unless you know what you are doing.

def canvasReq(uri):
  result = requests.post(uri, headers=headers, stream=True)
  return result.ok

def buildArray():
  for student in studentIDs:
    files = {'file':(file, open(file,'rb').read())}
    instfsurl=f"https://{domain}/api/v1/users/self/files?parent_folder_path={folder}&as_user_id=sis_user_id:{student}"
    fileresult = requests.post(instfsurl, headers=headers, files=files)
    fileResponse = fileresult.json()
    upload_url = fileResponse["upload_url"]
    uploadresult = requests.post(upload_url, files=files)
    uploadResponse = uploadresult.json()
    fileID = uploadResponse["id"]
    
    with open(CSVFileName, 'r') as _f:
      record_csv = csv.DictReader(_f)
      for x in record_csv:
        course_id = x['course_id']
        assignment_id = x['assignment_id']
        uri = f"https://{domain}/api/v1/courses/{course_id}/assignments/{assignment_id}/submissions?as_user_id=sis_user_id:{student}&submission[submission_type]=online_upload&submission[file_ids][]={fileID}"
        uri_list.append(uri)

if __name__ == '__main__':
  uri_list = []
  buildArray()
  processes = []

  with ThreadPoolExecutor(max_workers=10) as executor:
    for uri in uri_list:
      processes.append(executor.submit(canvasReq, uri))

  for task in as_completed(processes):
    print(task.result()) 
