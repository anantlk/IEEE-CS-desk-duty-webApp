from pymongo import MongoClient
client=MongoClient('mongodb://localhost:27017');
db=client.StudentDetails
#storing details of the student in the database

def store(regno,mobile,email,branch):
	details={
	"regno":regno,
	"mobile":mobile,
	"email":email,
	"branch":branch
	}
	TimeTable=db.table
	det=db.stud_det
	result=det.insert_one(details)
	print(result.inserted_id);

