import sys
import os

sys.path.insert(0,os.path.join(os.getcwd(),'utilities'));

import interact_database

table=[]
def user(regno,name,email,mobile):
	details = {
        "regno": regno,
        "name": name,
        "email": email,
        "mobile": mobile
        }
        return details
 
def create_time_table_schema(days):
	for day in days:
		table.append({"day":day,"schedule":[]})
	interact_database.create_collection(table)
