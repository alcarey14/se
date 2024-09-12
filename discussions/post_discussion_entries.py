#!/usr/bin/env python
# Working as of 2024-04-15

import json,os,csv
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

CSVFileName = "discussion_list.csv" # full path of input CSV (sis_course_id, discussion_id)
domain = "<DOMAIN>.instructure.com"

user1="<SIS USER ID>"
user2="<SIS USER ID>"
user3="<SIS USER ID>"

message1 = "<USER 1 MESSAGE>"
message2 = "<USER 2 MESSAGE>"
message3 = "<USER 3 MESSAGE>"


#######################################################################################
#######################################################################################
################ Don't edit anything past here unless you know what you are doing.

form_data1={'message' : message1}
form_data2={'message' : message2}
form_data3={'message' : message3}

# Leave these alone - just for initial array creation
uri_list1 = []
uri_list2 = []
uri_list3 = []

def canvasReq1(uri):
  result = requests.post(uri, headers=headers, data=form_data1, stream=True)
  return result.status_code

def canvasReq2(uri):
  result = requests.post(uri, headers=headers, data=form_data2, stream=True)
  return result.status_code

def canvasReq3(uri):
  result = requests.post(uri, headers=headers, data=form_data3, stream=True)
  return result.status_code


def buildArray():
  with open(CSVFileName, 'r') as _f:
    discussion_csv = csv.DictReader(_f)
    for disc in discussion_csv:
      course_id = disc['sis_course_id']
      disc_id = disc['discussion_id']
      uri = f"https://{domain}/api/v1/courses/sis_course_id:{course_id}/discussion_topics/{disc_id}/entries?as_user_id=sis_user_id:{user1}"
      uri_list1.append(uri)
      uri = f"https://{domain}/api/v1/courses/sis_course_id:{course_id}/discussion_topics/{disc_id}/entries?as_user_id=sis_user_id:{user2}"
      uri_list2.append(uri)
      uri = f"https://{domain}/api/v1/courses/sis_course_id:{course_id}/discussion_topics/{disc_id}/entries?as_user_id=sis_user_id:{user3}"
      uri_list3.append(uri)

if __name__ == '__main__':
  buildArray()
  processes = []

  with ThreadPoolExecutor(max_workers=10) as executor:
    for uri in uri_list1:
      processes.append(executor.submit(canvasReq1, uri))
    for uri in uri_list2:
      processes.append(executor.submit(canvasReq2, uri))
    for uri in uri_list3:
      processes.append(executor.submit(canvasReq3, uri))

  for task in as_completed(processes):
    print(task.result())
