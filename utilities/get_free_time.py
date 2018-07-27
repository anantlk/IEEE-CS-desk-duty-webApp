import json
import os
from pprint import pprint

time_map = {
    "8": "1",
    "9": "2",
    "10": "3",
    "11": "4",
    "12": "5",
    "2": "6",
    "3": "7",
    "4": "8",
    "5": "9",
    "6": "10"
}

DIR = os.path.join("data")
SCHEDULE_FNAME = os.path.join(DIR, "schedule.json")
STUD_DET_16_FNAME = os.path.join(DIR, "stud_det_16.json")
STUD_DET_17_FNAME = os.path.join(DIR, "stud_det_17.json")

with open(STUD_DET_16_FNAME) as f:
    stud_det_16 = json.load(f)
with open(STUD_DET_17_FNAME) as f:
    stud_det_17 = json.load(f)
with open(SCHEDULE_FNAME) as f:
    records = json.load(f)


def get_name_from_regno(regno):
    """
    returns name for a given registration number
    """
    try:
        year = regno[:2]
        if year == "16":
            all_members = stud_det_16
        else:
            all_members = stud_det_17
        for member in all_members:
            if regno == member["regno"]:
                return member["name"]
    except:
        return ["Check input pls"]


def get_free_people_by_day_time_year(req_day, req_time, year):
    """
    returns the registration number of people who are free
    for a given time
    params: day, time
    accepted day : [Monday, Tuesday, Wednesday, Thursday, Friday]
    accepted time: [8,9,10,11,12,2,3,4,5,6]
    accepted year: [16, 17]
    """
    try:
        db_time = time_map[req_time]
        free_members = []
        for item in records:
            day = item["day"]
            people = item["schedule"]
            if day == req_day:
                for person in people:
                    if db_time not in person["day_routine"]:
                        free_members.append(person["regno"])
        return [get_name_from_regno(member)
                for member in free_members if member[:2] == year]
    except:
        return ["Check input pls"]


if __name__ == '__main__':
    pprint(get_free_people_by_day_time_year("Thursday", "3", "17"))
