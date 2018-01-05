import collections
import re
import interact_database

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
        if (interact_database.check_database(regno,"16")):
			interact_database.insert(details,"16")


			
    if(re.match("17[a-zA-Z]{3}[0-9]{4}", regno)):  # for 2017 batch students
		if (interact_database.check_database(regno,"17")):
			interact_database.insert(details,"17")
			
# storing details of the schedule of the student in the database


def store_time_table(timetable, regno):
	schd = collections.OrderedDict()
	for day in days:
		i = days.index(day)
		schd["regno"]=regno
		schd["day_routine"]=collections.OrderedDict()
		for pos_day_schedule in range(len(timetable[i])):
			schd["day_routine"][str(pos_day_schedule + 1)] = str(timetable[i][pos_day_schedule])
	interact_database.update(day,schd)
