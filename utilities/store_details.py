
import collections
import re

import utilities.interact_database
from models import schema

DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

# storing details of the student in the database


def store(regno, name, email, mobile):
    details = schema.user(regno, name, email, mobile)
    if(re.match("16[a-zA-Z]{3}[0-9]{4}", regno)):  # for 2016 batch students
        if utilities.interact_database.check_database(regno, "16"):
            utilities.interact_database.insert(details, "16")
    if(re.match("17[a-zA-Z]{3}[0-9]{4}", regno)):  # for 2017 batch students
        if utilities.interact_database.check_database(regno, "17"):
            utilities.interact_database.insert(details, "17")

# storing details of the schedule of the student in the database


def store_time_table(timetable, regno):
    schema.create_time_table_schema(timetable.keys())
    schd = {}
    for day in timetable.keys():
        schd["regno"] = regno
        schd["day_routine"] = timetable[day]
        print("day:", day, "schd", schd)
        utilities.interact_database.update(day, schd)
