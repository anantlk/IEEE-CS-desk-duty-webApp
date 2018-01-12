from pymongo import MongoClient
import sys
import os

sys.path.insert(0, os.path.join(os.getcwd(), 'models'))
# client = MongoClient('mongodb://localhost:27017')

DB_NAME = "student_details"
DB_HOST = "ds249737.mlab.com"
DB_PORT = 49737
DB_USER = "ieeecs"
DB_PASS = "ieeecs@vit"
connection = MongoClient(DB_HOST, DB_PORT)
db = connection[DB_NAME]
db.authenticate(DB_USER, DB_PASS)


def create_collection(model):
    collection = db.table
    if(collection.count() == 0):
        collection.insert_many(model)


def check_database(regno, batch):
    if(batch == "16"):
        if(db.stud_det_16.find({"regno": regno}).count() == 0):
            return 1
        return 0
    if(batch == "17"):
        if(db.stud_det_17.find({"regno": regno}).count() == 0):
            return 1
        return 0


def insert(details, batch):
    if(batch == "16"):
        det = db.stud_det_16
        result = det.insert_one(details)
    if(batch == "17"):
        det = db.stud_det_17
        result = det.insert_one(details)


def update(day, schd):
    time_table = db.table
    time_table.update_one({"day": day}, {"$push": {"schedule": schd}})
