
import base64
import os
from io import BytesIO

import requests
from bs4 import BeautifulSoup
from PIL import Image

from utilities import interact_database
from utilities.captchaparser import solve_captcha

SEMESTER_ID = os.environ.get("SEMESTER_ID")

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

        main_page = requests.get(
            'https://vtopbeta.vit.ac.in/vtop/',
                        headers=HEADERS,
                        verify=False)
        # session_cookie
        session_cookie = main_page.cookies['JSESSIONID']
        session_cookie = 'JSESSIONID=' + session_cookie
        HEADERS.update({'cookie': session_cookie})

        # captcha solving
        root = BeautifulSoup(main_page.text, "html.parser")
        img_data = root.find_all("img")[1][
            "src"].strip("data:image/png;base64,")

        img = Image.open(BytesIO(base64.b64decode(img_data)))
        captcha_check = solve_captcha(img)

        # user login
        login_data = {
            'uname': regno,
            'passwd': password,
            'captchaCheck': captcha_check}

        login = requests.post(
            'https://vtopbeta.vit.ac.in/vtop/processLogin',
                        headers=HEADERS,
                        data=login_data,
                        verify=False)
        login_response = BeautifulSoup(login.text, "html.parser")

        if ('Invalid Username/Password, Please try again' in login_response.text or 'User does not exist' in login_response.text):
            del HEADERS['cookie']
            return 0
        return 1
    except:
        del HEADERS['cookie']
        return 0


def timetable_scrape():
    timetable = requests.post(
        'https://vtopbeta.vit.ac.in/vtop/processViewTimeTable',
        headers=HEADERS,
        data={'semesterSubId': SEMESTER_ID},
        verify=False)
    root = BeautifulSoup(timetable.text, "html.parser")
    table = root.find_all(class_="table table-responsive table-striped")[0]

    # filters out monday to friday and 8am - 7pm slots
    table_data = [[
        cell.text.split('-')[3] if cell.text.count(
        '-') == 3 else 'none' + cell.text
            for cell in row.find_all("td")
    ][1:]
        for row in table.find_all("tr")
    ][4:-4]

    # filters out 'theory' and 'lunch' occurence
    table_data = [[i for i in j if not i.isalpha()] for j in table_data]

    # remove excess lab slots
    table_data = [[i for i in j if j.index(i) != 5 and j.index(i) < 11]
                  for j in table_data]
    # final filter
    final_table = [[] for i in range(0, 10)]
    for i in range(0, len(table_data), 2):
        for thry, lab in zip(table_data[i], table_data[i + 1]):
            if 'none' in thry and 'none' in lab:
                final_table[i].append('none')
            elif 'none' in thry:
                if table_data[i].index(thry) == 4 or table_data[i].index(thry) == 9:
                    final_table[i][-1] = lab
                final_table[i].append(lab)
            else:
                final_table[i].append(thry)
    # logout
    requests.post('https://vtopbeta.vit.ac.in/vtop/processLogout', verify=False)
    del HEADERS['cookie']
    return [i for i in final_table if i]


def get_timetable(user, password):
    login_result = login_user(user, password)
    if login_result == 1:
        return timetable_scrape()
    else:
        requests.post('https://vtopbeta.vit.ac.in/vtop/processLogout', verify=False)
        return login_result
