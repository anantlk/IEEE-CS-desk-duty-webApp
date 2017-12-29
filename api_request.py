import pymongo
import requests
import json
from pymongo import MongoClient
client=MongoClient('mongodb://localhost:27017');
db=client.StudentDetails

#Schedule structure to be stored in database

response=requests.post(
		'https://api.collegecode.org/student/refresh',
		data={
		'reg_no':'16BCI0093',
		'password':'anant@123',
		'campus':'vellore'
		}
)
#print(response.text)
data=json.loads(response.text)
print(json.dumps(data,indent=10))
details={
"regno":"123",
"name":"asdsad",
"mobile":"1234567890",
"email":"asdad",
"branch":"asdsd"
}



TimeTable=db.table
det=db.stud_det
#result=TimeTable.insert_one(schd)
print("schedule print:")
#print(result.inserted_id);
