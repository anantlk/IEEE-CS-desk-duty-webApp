import os
import json
from pymongo import MongoClient
from collections import OrderedDict
import re

DB_NAME = os.environ.get("DB_NAME")
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")

names = []
place = ["sjt", "tt"]
schd = {}
count = {}

with open("env.json", "r") as fp:
    DB = json.loads(fp.read())
CONNECTION = MongoClient(DB["DB_HOST"], int(DB["DB_PORT"]))
db = CONNECTION[DB["DB_NAME"]]
db.authenticate(DB["DB_USER"], DB["DB_PASS"])


docs = db.table.find()

day = "Monday"
day_schedule = []
for schedules in docs:
    if(schedules["day"] == day):
        day_schedule = schedules["schedule"]
        break
for stud_routine in day_schedule:
    regno = stud_routine["regno"]
    if(re.match("^17", regno)):
        names.append(regno)
        count[regno] = 0
        schd[regno] = {}
        for key in stud_routine["day_routine"]:
            schd[regno][int(key)] = stud_routine["day_routine"][key]

print(schd)
