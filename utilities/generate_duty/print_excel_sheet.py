import csv
place=['SJT','TT']

#printing schedule and no of slots assigned to every person on terminal

def print_desk_duty(table):
	time_slot_sjt = ['SJT','8-9am',' 9-10am',' 10-11am','11am-12pm',' 12-1pm',' 2-3pm',' 3-4pm',' 4-5pm',' 5-6pm',' 6-7pm']
	time_slot_tt = ['TT','8-9am',' 9-10am',' 10-11am','11am-12pm',' 12-1pm',' 2-3pm',' 3-4pm',' 4-5pm',' 5-6pm',' 6-7pm']
	
	count = 0;
	with open('desk_duty.csv', 'w') as csvFile:
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
	for slot in range(len(time_slot)):
		row = []
		row.append(time_slot[slot]);
		print(free_slots[slot])
		for free_stud in free_slots[slot]:
			row.append(free_stud)
		print(row)
		with open('free_slot.csv','w') as csvFile:
			writer = csv.writer(csvFile)
			writer.writerow(row)

	csvFile.close()

