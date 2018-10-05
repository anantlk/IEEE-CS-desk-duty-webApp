import re;

def assign(free_slot,schd,place,candidates):
	for i in free_slot:
		candidates[i]=[]
		for name in free_slot[i]:
			if(i>1 and i<10):
				if(re.match("^"+place,schd[name][i+1]) or re.match("^"+place,schd[name][i-1])):
					candidates[i].append(name)
			elif(i==1):
				if(re.match("^"+place,schd[name][i+1])):
					candidates[i].append(name)
			else:
				if(re.match("^"+place,schd[name][i-1])):
					candidates[i].append(name)
	return candidates
