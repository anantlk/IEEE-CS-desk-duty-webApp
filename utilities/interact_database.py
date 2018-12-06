import os
import sys
path = os.getcwd()
sys.path.insert(0, path)
from pymongo import MongoClient
from .generate_duty import generate_desk_duty


DB_NAME = os.environ.get("DB_NAME") or "student_details_3"
DB_HOST = os.environ.get("DB_HOST") or "localhost"
DB_PORT = os.environ.get("DB_PORT") or "27017"
DB_USER = os.environ.get("DB_USER") or ""
DB_PASS = os.environ.get("DB_PASS") or ""


CONNECTION = MongoClient(DB_HOST, int(DB_PORT))
db = CONNECTION[DB_NAME]

if(DB_USER != ""):
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
        det.insert_one(details)
    if batch == "17":
        det = db.stud_det_17
        det.insert_one(details)


def update(day, schd):
    time_table = db.table
    time_table.update_one({"day": day}, {"$push": {"schedule": schd}})


def get_details(day):
    docs = db.table.find()
    stud_names = db.stud_det_17.find()
    result = generate_desk_duty.generate(day, stud_names, docs)
    if(result):
        return True
    else:
        return False
