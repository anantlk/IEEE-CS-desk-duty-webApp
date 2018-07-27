import os

from pymongo import MongoClient


DB_NAME = os.environ.get("DB_NAME")
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = int(os.environ.get("DB_PORT"))
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")


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
