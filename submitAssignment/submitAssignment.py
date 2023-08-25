#!/usr/bin/env python
# Working as of 2023-08-25

import json,csv,os
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
file="" # file to be submitted
folder="assignments"
studentIDs=[""] # array of student SIS IDs


#######################################################################################
#######################################################################################
################ Don't edit anything past here unless you know what you are doing.

if __name__ == '__main__':
  with open(CSVFileName, 'r') as _f:
    record_csv = csv.DictReader(_f)
    for record in record_csv:
      course_id = record['course_id']
      assignment_id = record['assignment_id']
      for student in studentIDs:
        files = {'file':(file, open(file,'rb').read())}
        instfsurl="https://{0}/api/v1/users/self/files?parent_folder_path={1}&as_user_id=sis_user_id:{2}".format(domain,folder, student)
        fileresult = requests.post(instfsurl, headers=headers, files=files)
        fileResponse = fileresult.json()
        upload_url = fileResponse["upload_url"]
        uploadresult = requests.post(upload_url, files=files)
        uploadResponse = uploadresult.json()
        fileID = uploadResponse["id"]
        form_data={
        
          'submission[submission_type]' : 'online_upload',
          'submission[file_ids][]' : fileID
        }
        uri = "https://{0}/api/v1/courses/{1}/assignments/{2}/submissions?as_user_id=sis_user_id:{3}".format(domain, course_id, assignment_id,student)
        result = requests.post(uri, headers=headers, data=form_data)
        print(result.status_code)