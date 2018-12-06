
import base64
import os
from io import BytesIO

import requests
from bs4 import BeautifulSoup
from PIL import Image
import email.utils

from utilities import interact_database
from utilities.captchaparser import solve_captcha

SEMESTER_ID = os.environ.get("SEMESTER_ID")

HEADERS = {
    "cache-control": "no-cache",
    "accept-language": "en-US,en;q=0.9",
    "accept-encoding": "gzip, deflate, br",
    "dnt": "1",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.56 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36"
}


def login_user(regno, password):
    try:
        if regno[:2] == "16":
            if interact_database.check_database(regno, "16") == 0:
                return 2
        if(regno[:2] == "17"):
            if interact_database.check_database(regno, "17") == 0:
                return 2

        res = requests.get(
            'https://vtop.vit.ac.in/vtop', headers=HEADERS, verify=False)
        print(res.cookies.get_dict())
        HEADERS.update({"Cookie": "JSESSIONID=" + res.cookies["JSESSIONID"]})
        res = requests.post(
            'https://vtop.vit.ac.in/vtop/vtopLogin',
            headers=HEADERS,
            verify=False)

        # captcha solving
        root = BeautifulSoup(res.text, "html.parser")
        print(root.prettify())
        img_data = root.find_all("img")[1]["src"].strip(
            "data:image/png;base64,")
        img = Image.open(BytesIO(base64.b64decode(img_data)))
        captcha_check = solve_captcha(img)
        login_data = {
            'uname': regno,
            'passwd': password,
            'captchaCheck': captcha_check
        }
        res = requests.post(
            'https://vtop.vit.ac.in/vtop/doLogin',
            data=login_data,
            headers=HEADERS,
            verify=False)

        login_response = BeautifulSoup(res.text, "html.parser")
        if ('Invalid Username/Password, Please try again' in login_response.text or 'User does not exist' in login_response.text):
            del HEADERS['cookie']
            return 0
        return 1
    except:
        del HEADERS['Cookie']
        return 0


def is_class(cell):
    if cell.count("-") != 3:
        return False
    return True


def get_venue(text):
    return text.strip().split('-')[3]


def parse_table(timetable_html):
    root = BeautifulSoup(timetable_html.text, "html.parser")
    table = root.find_all(class_="table table-responsive table-striped")[0]
    rows = table.find_all("tr")[4:-4]
    theory_map = {
        0: "1",
        1: "2",
        2: "3",
        3: "4",
        4: "5",
        7: "6",
        8: "7",
        9: "8",
        10: "9",
        11: "10"
    }
    lab_map = {
        0: ["1"],
        1: ["1", "2"],
        2: ["3"],
        3: ["3", "4"],
        4: ["4", "5"],
        7: ["6"],
        8: ["6", "7"],
        9: ["8"],
        10: ["8", "9"],
        11: ["9", "10"]
    }
    day_map = {
        0: "Monday",
        1: "Tuesday",
        2: "Wednesday",
        3: "Thursday",
        4: "Friday"
    }
    schedule = {}
    for i in range(0, len(rows), 2):
        row_theory = rows[i]
        row_lab = rows[i + 1]
        # theory row
        day_slots = {}
        theory_cells = row_theory.find_all("td")[2:]
        for theory_cell in theory_cells:
            index = theory_cells.index(theory_cell)
            if is_class(theory_cell.text):
                if index in theory_map.keys():
                    day_slots[theory_map[index]] = get_venue(theory_cell.text)

        lab_cells = row_lab.find_all("td")[1:]
        for lab_cell in lab_cells:
            index = lab_cells.index(lab_cell)
            if is_class(lab_cell.text):
                if index in lab_map.keys():
                    lab_list = lab_map[index]
                    for slot in lab_list:
                        day_slots[slot] = get_venue(lab_cell.text)

        schedule[day_map[i/2]] = day_slots
    return schedule


def timetable_scrape(regno):

    timetable = requests.post(
        'https://vtop.vit.ac.in/vtop/processViewTimeTable',
        headers=HEADERS,
        data={'semesterSubId': SEMESTER_ID, 'authorizedID': regno,
              'x': email.utils.formatdate(usegmt=True)},
        verify=False)
    schedule = parse_table(timetable)

    # logout
    requests.post(
        'https://vtop.vit.ac.in/vtop/processLogout', verify=False)
    del HEADERS['Cookie']
    return schedule


def get_timetable(user, password):
    login_result = login_user(user, password)
    if login_result == 1:
        return timetable_scrape(user)
    else:
        requests.post(
            'https://vtop.vit.ac.in/vtop/processLogout', verify=False)
        return login_result
