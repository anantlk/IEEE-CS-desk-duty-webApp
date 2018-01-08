import collections
import re
import interact_database
import sys
import os

sys.path.insert(0,os.path.join(os.getcwd(),'models'));

import schema
days = ["monday", "tuesday", "wednesday", "thursday", "friday"]

# storing details of the student in the database


def store(regno, name, email, mobile):
	details=schema.user(regno,name,email,mobile)
	if(re.match("16[a-zA-Z]{3}[0-9]{4}", regno)):  # for 2016 batch students
		if (interact_database.check_database(regno,"16")):
			interact_database.insert(details,"16")
	if(re.match("17[a-zA-Z]{3}[0-9]{4}", regno)):  # for 2017 batch students
		if (interact_database.check_database(regno,"17")):
			interact_database.insert(details,"17")
			
# storing details of the schedule of the student in the database


def store_time_table(timetable, regno):
	schema.create_time_table_schema(days)
	schd = collections.OrderedDict()
	for day in days:
		i = days.index(day)
		schd["regno"]=regno
		schd["day_routine"]=collections.OrderedDict()
		for pos_day_schedule in range(len(timetable[i])):
			schd["day_routine"][str(pos_day_schedule + 1)] = str(timetable[i][pos_day_schedule])
		interact_database.update(day,schd)
