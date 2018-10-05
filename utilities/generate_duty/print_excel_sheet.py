import csv
import os
place=['SJT','TT']

#printing schedule and no of slots assigned to every person on terminal

def print_desk_duty(table):
	time_slot_sjt = ['SJT','8-9am',' 9-10am',' 10-11am','11am-12pm',' 12-1pm',' 2-3pm',' 3-4pm',' 4-5pm',' 5-6pm',' 6-7pm']
	time_slot_tt = ['TT','8-9am',' 9-10am',' 10-11am','11am-12pm',' 12-1pm',' 2-3pm',' 3-4pm',' 4-5pm',' 5-6pm',' 6-7pm']
	dir_path = os.getcwd()
	print(dir_path);
	if not os.path.isdir(dir_path+'/table'):
		os.mkdir(dir_path + '/table')
	count = 0;
	with open(dir_path+'/table/desk_duty.csv', 'w') as csvFile:
		writer = csv.writer(csvFile)
		writer.writerow(time_slot_sjt)
		for venue in table:
			duty = [];
			duty.append("");
			for slot in table[venue]:
				string = ""
				for per in table[venue][slot]:
					string+=per.split(" ")[0] + ","
				duty.append(string.rstrip(","));
			writer.writerow(duty)
			count += 1
			if(count!=2):
				writer.writerow(time_slot_tt)


	csvFile.close()

def print_free_slots(free_slots):
	print("Hello")
	time_slot = ['8-9am',' 9-10am',' 10-11am','11am-12pm',' 12-1pm',' 2-3pm',' 3-4pm',' 4-5pm',' 5-6pm',' 6-7pm']
	dir_path = os.getcwd()
	print(dir_path);
	if not os.path.isdir(dir_path+'/table'):
		os.mkdir(dir_path + '/table')
	with open(dir_path+'/table/free_slot.csv','w+') as csvFile:
		writer = csv.writer(csvFile)
		for slot in range(len(time_slot)):
			row = []
			print(free_slots)
			print(slot)
			row.append(time_slot[slot]);
			print(row)
			for free_stud in free_slots[slot+1]:
				row.append(free_stud.split(" ")[0])
			print(row)
			writer.writerow(list(set(row)))

	csvFile.close()

