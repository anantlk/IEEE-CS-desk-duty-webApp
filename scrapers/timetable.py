import requests
import os
import re
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
import base64
from pprint import pprint

import sys
sys.path.insert(0, '.\utilities')
print(os.path.abspath(sys.path[0]))
from captchaparser import CaptchaParse
import interact_database

semSubId = 'VL2017185'

headers = {
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64)\
        AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 \
        Safari/537.36'
}


def login_user(regno, password):
    try:
		if(regno[:2]=="16"):
			if(interact_database.check_database(regno,"16")==0):
				return 2
				
		if(regno[:2]=="17"):
			if(interact_database.check_database(regno,"17")==0):
				return 2
				
		main_page = requests.get(
			'https://vtopbeta.vit.ac.in/vtop/',
			headers=headers,
			verify=False)
			
		# session_cookie
		session_cookie = main_page.cookies['JSESSIONID']
		session_cookie = 'JSESSIONID=' + session_cookie
		headers.update({'cookie': session_cookie})

		# captcha solving
		root = BeautifulSoup(main_page.text, "html.parser")
		img_data = root.find_all("img")[1][
			"src"].strip("data:image/png;base64,")

		img = Image.open(BytesIO(base64.b64decode(img_data)))
		captcha_check = CaptchaParse(img)

		# user login
		login_data = {
			'uname': regno,
			'passwd': password,
			'captchaCheck': captcha_check}

		login = requests.post(
			'https://vtopbeta.vit.ac.in/vtop/processLogin',
			headers=headers,
			data=login_data,
			verify=False)
		return 1
    except:
        return 0


def timetable_scrape():
    timetable = requests.post(
        'https://vtopbeta.vit.ac.in/vtop/processViewTimeTable',
        headers=headers,
        data={'semesterSubId': semSubId},
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
    return [i for i in final_table if i]


def get_timetable(user, password):
    login_result=login_user(user,password)
    print(login_result)
    if login_result==1:
        return timetable_scrape()
    else:
        return login_result
