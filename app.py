
import subprocess
import zipfile
import os
from flask import Flask, render_template, request,send_file,Response
from scrapers import timetable
from utilities import get_free_time, store_details,interact_database

app = Flask(__name__)
    
@app.route("/")
def main():
    return render_template('index.html')


@app.route("/register", methods=['POST'])
def register():
    reg_no = request.form["regno"]
    password = request.form["password"]
    name = request.form["name"]
    email = request.form["email"]
    mobile = request.form["mobile"]
    fetched_tt = timetable.get_timetable(reg_no, password)
    if fetched_tt == 2:
        return "exists"
    elif fetched_tt == 0:
        return "Incorrect"
    else:
        store_details.store(reg_no, name, email, mobile)
        store_details.store_time_table(fetched_tt, reg_no)
        return "success"


@app.route("/get_free_members", methods=['GET'])
def get_free_members():
    # subprocess.call("scripts/get_db_dump.sh")
    free_members = get_free_time.get_free_people_by_day_time_year(
        request.args['day'], request.args['time'], request.args['year'])
    return ''.join(mem + "," for mem in free_members)

@app.route("/get_desk_duty",methods = ["GET"])
def get_desk_duty():
    day = request.args["day"]
    print(day)
    if(interact_database.get_details(day)):
        path = os.getcwd();
        zipf = zipfile.ZipFile('result.zip', 'w', zipfile.ZIP_DEFLATED)
        for root, dirs, files in os.walk(path + "/table"):
            print(root);
            dest_dir = root.replace(os.path.dirname(path), '', 1)
            for file in files:
                zipf.write(os.path.join(root, file), arcname=os.path.join(dest_dir, file))
        zipf.close()
        return send_file(path + '/result.zip',
                     mimetype='text/zip',
                     attachment_filename='result.zip',
                     as_attachment=True)
    else:
        return "Failed"

if __name__ == "__main__":
    app.run()
