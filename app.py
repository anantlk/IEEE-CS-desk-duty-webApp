import store_details
import api_call
import flask
from flask import Flask,render_template,request

app=Flask(__name__)

@app.route("/")
def main():
	return render_template('index.html')

@app.route("/register",methods=['POST'])
def register():
	RegNo=request.form["regno"]
	Password=request.form["password"]	
	Email=request.form["email"]
	Mobile=request.form["mobile"]
	Branch=request.form["branch"]
	Data=api_call.req(RegNo,Password)
	store_details.store(RegNo,Mobile,Email,Branch)
	return "successfully registered"
	 
if __name__== "__main__":
	print("running..\n\n")
	app.run()
