import os
import sys
path = os.getcwd();
sys.path.insert(0, path)
from pymongo import MongoClient
from .generate_duty import generate_desk_duty

# DB_NAME = os.environ.get("DB_NAME")
# DB_HOST = os.environ.get("DB_HOST")
# DB_PORT = os.environ.get("DB_PORT")
# DB_USER = os.environ.get("DB_USER")
# DB_PASS = os.environ.get("DB_PASS")

DB_NAME = "student_details"
DB_HOST = "ds153841.mlab.com"
DB_PORT = 53841
DB_USER = "ieeecs"
DB_PASS = "ieeecs@123"


# DB_NAME = "student"
# DB_HOST = "localhost"
# DB_PORT = 27017

CONNECTION = MongoClient(DB_HOST, DB_PORT)
db = CONNECTION[DB_NAME]
db.authenticate(DB_USER, DB_PASS)


def create_collection(model):
    collection = db.table
    if(collection.count() == 0):
        collection.insert_many(model)


def check_database(regno, batch):
    if batch == "16":
        if db.stud_det_16.find({"regno": regno}).count() == 0:
            return 1
        return 0
    if batch == "17":
        if db.stud_det_17.find({"regno": regno}).count() == 0:
            return 1
        return 0


def insert(details, batch):
    if batch == "16":
        det = db.stud_det_16
        result = det.insert_one(details)
    if batch == "17":
        det = db.stud_det_17
        result = det.insert_one(details)


def update(day, schd):
    time_table = db.table
    time_table.update_one({"day": day}, {"$push": {"schedule": schd}})

def get_details(day):
    docs = db.table.find()
    stud_names = db.stud_det_17.find()
    result = generate_desk_duty.generate(day,stud_names,docs)
    if(result):
        return True
    else:
        return False