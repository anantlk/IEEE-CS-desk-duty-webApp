from pymongo import MongoClient
import collections
import re

client = MongoClient('mongodb://localhost:27017')
db = client.StudentDetails
days = ["monday", "tuesday", "wednesday", "thursday", "friday"]

# storing details of the student in the database


def store(regno, mobile, email, branch):
    details = {
        "regno": regno,
        "mobile": mobile,
        "email": email,
        "branch": branch
    }
    if(re.match("16[a-zA-Z]{3}[0-9]{4}", regno)):  # for 2016 batch students
        if (db.stud_det_16.find({"regno":regno}).count()==0):
			det = db.stud_det_16
			result = det.insert_one(details)

			
    if(re.match("17[a-zA-Z]{3}[0-9]{4}", regno)):  # for 2017 batch students
        if(db.stud_det_17.find({"regno":regno}).count()==0):
			det = db.stud_det_17
			result = det.insert_one(details)
			
# storing details of the schedule of the student in the database


def store_time_table(timetable, regno):
    time_table = db.table
    if(time_table.find({"schedule.regno":regno}).count()==0):
		schd = collections.OrderedDict()
		for day in days:
			i = days.index(day)
			schd["regno"]=regno
			schd["day_routine"]=collections.OrderedDict()
			for pos_day_schedule in range(len(timetable[i])):
				schd["day_routine"][str(pos_day_schedule + 1)] = str(timetable[i][pos_day_schedule])
			time_table.update_one({"day": day}, {"$push": {"schedule": schd}})

