import json
import os
from collections import OrderedDict
import re
from .print_excel_sheet import *
import random
from .convenience import *
from random import choice, sample
from collections import OrderedDict
from os.path import join, dirname, abspath


names = []
place = ["SJT", "TT"]
table = {"SJT": {}, "TT": {}}
schd = {}
free_slot = {}
count = {}
# fname = join(dirname(dirname(abspath(__file__))), 'time_table.xlsx')
details = {}

def remove_assigned_members(array, count):
    for name in count:
        if(count[name] == 2):
            for slot in array:
                if(name in array[slot]):
                    array[slot].remove(name)


def allot_duty(slot,i, candidates, venue):
    if(len(candidates) > 0):
        candidates = random.sample(candidates, len(candidates))
        for name in candidates:
            if(count[name] == 2):
                continue
            count[name] += 1
            i += 1
            table[venue][slot].append(name)
            if(i == 2):
                return i, table
    return i, table

def generate(day,stud_names,docs):
    try:
        for doc in stud_names:
            details[doc["regno"]] = doc["name"]
            
        print(details)

        day_schedule = []

        for schedules in docs:
            if(schedules["day"] == day):
                day_schedule = schedules["schedule"]
                break

        for stud_routine in day_schedule:
            regno = stud_routine["regno"]
            if(re.match("^17", regno)):
                name = details[regno]
                names.append(name)
                count[name] = 0
                schd[name] = {}
                for key in range(1,11):
                    if(str(key) in stud_routine["day_routine"].keys()):
                        schd[name][key] = stud_routine["day_routine"][str(key)]
                    else:
                        schd[name][key] = "";

        print("Schedule:\n")
        print(schd)
        print("\n")

        # list of members who are free in there slots

        for i in range(1, 11):
            free_slot[i] = []
            for name in names:
                if(len(schd[name][i]) == 0):
                    free_slot[i].append(name)

        print("Free slots:\n")
        print(free_slot)
        print("\n")

        # print_free_slots(free_slot)
        # chosing candidates from different places so that they have class either before or after there free slots in that place.This is done to assign places according to there convenience

        sjt_candidates = assign(free_slot, schd, 'SJT', {})
        tt_candidates = assign(free_slot, schd, 'TT', {})
        gdn_candidates = assign(free_slot, schd, 'GDN', {})
        mb_candidates = assign(free_slot, schd, 'MB', {})
        smv_candidates = assign(free_slot, schd, 'SMV', {})
        cdmm_candidates = assign(free_slot, schd, 'CDMM', {})
        cbmr_candidates = assign(free_slot, schd, 'CBMR', {})
        hostel_candidates = assign(free_slot, schd, '', {})


        print("TT candidates:\n")
        print(tt_candidates),
        print("\n")
        print("SJT candidates:\n")
        print(sjt_candidates)
        print("\n")

        for slot in tt_candidates:
            i = 0
            global table
            print(table)
            table['TT'][slot] = []
            while(i < 2):
                candidates = list(set(tt_candidates[slot]))
                i, table = allot_duty(slot,i, candidates, 'TT')
                if(i == 2):
                    break
                candidates = list(
                    set(sjt_candidates[slot]+smv_candidates[slot])-set(table['TT'][slot]))
                i, table = allot_duty(slot,i, candidates, 'TT')
                if(i == 2):
                    break
                candidates = list(
                    set(mb_candidates[slot]+cbmr_candidates[slot])-set(table['TT'][slot]))
                i, table = allot_duty(slot,i, candidates, 'TT')
                if(i == 2):
                    break
                candidates = list(
                    set(cdmm_candidates[slot]+gdn_candidates[slot])-set(table['TT'][slot]))
                i, table = allot_duty(slot,i, candidates, 'TT')
                if(i == 2):
                    break
                candidates = list(set(hostel_candidates[slot])-set(table['TT'][slot]))
                i, table = allot_duty(slot,i, candidates, 'TT')
                break


        for array in [sjt_candidates, tt_candidates, mb_candidates, smv_candidates, cbmr_candidates, cdmm_candidates, gdn_candidates, hostel_candidates]:
            remove_assigned_members(array, count)

        for slot in tt_candidates:
            i = 0
            table['SJT'][slot] = []
            while(i < 2):
                candidates = list(set(sjt_candidates[slot])-set(table['SJT'][slot])-set(table['TT'][slot]))
                i, table = allot_duty(slot,i, candidates, 'SJT')
                if(i == 2):
                    break
                candidates = list(set(tt_candidates[slot])-set(table['SJT'][slot])-set(table['TT'][slot]))
                i, table = allot_duty(slot,i, candidates, 'SJT')
                if(i == 2):
                    break
                candidates = list(set(smv_candidates[slot])-set(table['SJT'][slot])-set(table['TT'][slot]))
                i, table = allot_duty(slot,i, candidates, 'SJT')
                if(i == 2):
                    break
                candidates = list(
                    set(cbmr_candidates[slot]+mb_candidates[slot])-set(table['SJT'][slot])-set(table['TT'][slot]))
                i, table = allot_duty(slot,i, candidates, 'SJT')
                if(i == 2):
                    break
                candidates = list(
                    set(cdmm_candidates[slot]+gdn_candidates[slot])-set(table['SJT'][slot])-set(table['TT'][slot]))
                i, table = allot_duty(slot,i, candidates, 'SJT')
                if(i == 2):
                    break
                candidates = list(set(hostel_candidates[slot])-set(table['SJT'][slot])-set(table['TT'][slot]))
                i, table = allot_duty(slot,i, candidates, 'SJT')
                break

        print("Final Table:\n")
        print(table)  # print final table
        print("\n")

        # generate excel sheet

        print_desk_duty(table)

        print("\n\nDesk Duty Generated!! Check Your directory")

        return True
    except:
        return False