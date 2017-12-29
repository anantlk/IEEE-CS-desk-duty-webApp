import requests
import json

#api call to get details of the student

def req(username,password):
	response=requests.post(
		'https://api.collegecode.org/student/refresh',
		data={
		'reg_no':username,
		'password':password,
		'campus':'vellore'
		}
	)
	return json.loads(response.text)
	print(json.dumps(data,indent=10))

