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

CSVFileName = "feedback.csv" # path of input CSV (course_id, assignment_id, student_id, grade, feedback)
domain = "<DOMAIN>.instructure.com" 


#######################################################################################
#######################################################################################
################ Don't edit anything past here unless you know what you are doing.

if __name__ == '__main__':
  with open(CSVFileName, 'r') as _f:
    feedback_csv = csv.DictReader(_f)
    for x in feedback_csv:
      course_id = x['course_id']
      assignment_id = x['assignment_id']
      student_id = x['student_id']
      grade = x['grade']
      feedback = x['feedback']

      form_data={
        'comment[text_comment]' : feedback,
        'submission[posted_grade]' : grade
      }
      uri = "https://{0}/api/v1/courses/{1}/assignments/{2}/submissions/sis_user_id:{3}".format(domain, course_id, assignment_id,student_id)
      result = requests.put(uri, headers=headers, data=form_data)
      print(result.json())