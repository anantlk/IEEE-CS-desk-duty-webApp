
import base64
import os
from io import BytesIO

import requests
from bs4 import BeautifulSoup
from PIL import Image

from utilities import interact_database
from utilities.captchaparser import solve_captcha

SEMESTER_ID = os.environ.get(SEMESTER_ID)

HEADERS = {
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64)\
        AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 \
        Safari/537.36'
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
            'https://vtopbeta.vit.ac.in/vtop/', headers=HEADERS, verify=False)
        HEADERS.update({"Cookie": "JSESSIONID=" + res.cookies["JSESSIONID"]})
        root = BeautifulSoup(res.text, "html.parser")
        gsid_index = root.text.find("gsid=")
        gsid = root.text[gsid_index:gsid_index + 12]
        if gsid[-1] == ';':
            gsid = gsid[:-1]
        res = requests.get(
            'https://vtopbeta.vit.ac.in/vtop/executeApp?' + gsid,
            headers=HEADERS,
            verify=False)
        res = requests.post(
            'https://vtopbeta.vit.ac.in/vtop/getLogin',
            headers=HEADERS,
            verify=False)
        # captcha solving
        HEADERS.update({"Cookie": "JSESSIONID=" + res.cookies["JSESSIONID"]})
        root = BeautifulSoup(res.text, "html.parser")
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
            'https://vtopbeta.vit.ac.in/vtop/processLogin',
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


def timetable_scrape():

    timetable = requests.post(
        'https://vtopbeta.vit.ac.in/vtop/processViewTimeTable',
        headers=HEADERS,
        data={'semesterSubId': SEMESTER_ID},
        verify=False)
    schedule = parse_table(timetable)
    
    # logout
    requests.post(
        'https://vtopbeta.vit.ac.in/vtop/processLogout', verify=False)
    del HEADERS['Cookie']
    return schedule


def get_timetable(user, password):
    login_result = login_user(user, password)
    if login_result == 1:
        return timetable_scrape()
    else:
        requests.post(
            'https://vtopbeta.vit.ac.in/vtop/processLogout', verify=False)
        return login_result


if __name__ == "__main__":
    get_timetable("16BCE0979", "Presto412@Priyansh")
