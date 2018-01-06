import sys
import os

import flask
from flask import Flask, render_template, request

app = Flask(__name__)

sys.path.insert(0, os.path.join(os.getcwd(), 'scrapers'))
sys.path.insert(0, os.path.join(os.getcwd(), 'utilities'))
import timetable
import store_details


@app.route("/")
def main():
    return render_template('index.html')


@app.route("/register", methods=['POST'])
def register():
    print("Got Request")
    reg_no = request.form["regno"]
    password = request.form["password"]
    email = request.form["email"]
    mobile = request.form["mobile"]
    branch = request.form["branch"]
    fetched_tt = timetable.get_timetable(reg_no, password)
    if fetched_tt == 2:
        return 2
    elif fetched_tt == 0:
        return 0
    else:
        store_details.store(reg_no, mobile, email, branch)
        store_details.store_time_table(fetched_tt, reg_no)
        return 1

if __name__ == "__main__":
    app.run()
