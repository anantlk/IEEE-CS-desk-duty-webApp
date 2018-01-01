import store_details
import api_call
import sys
import os
import flask
from flask import Flask,render_template,request

app=Flask(__name__)

sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'scrapers'))
import timetable

@app.route("/")
def main():
	return render_template('index.html')

@app.route("/register",methods=['POST'])
def register():
	print("Got Request")
	RegNo=request.form["regno"]
	Password=request.form["password"]	
	Email=request.form["email"]
	Mobile=request.form["mobile"]
	Branch=request.form["branch"]
	store_details.store(RegNo,Mobile,Email,Branch)
	timeT=timetable.get_timetable(RegNo,Password)
	store_details.store_time_table(timeT,RegNo)
	return "successfully registered"
	 
if __name__== "__main__":
	app.run()
