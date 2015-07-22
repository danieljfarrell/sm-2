import json
import sys
import math

def import_items(file_path):
	return json.loads(open(file_path).read())

def export_items(items, file_path):
	open(file_path, "wb").write(json.dumps(items))
	return True

def get_next_i_interval(item, reset=False):
	"""Get next inter-repetition interval after the n-th repetition"""
	if reset:
		item["i-interval"] = 1
	else:
		last_i_interval = item.get('i-interval', None)
		if last_i_interval:
			if last_i_interval > 2:
				item["i-interval"] = math.ceil(last_i_interval * item["e-factor"])
			item["i-interval"] = 6
		item["i-interval"] = 1
	return item

def get_quality_of_repetition():
	"""
	5 - perfect response
	4 - correct response after a hesitation
	3 - correct response recalled with serious difficulty
	2 - incorrect response; where the correct one seemed easy to recall
	1 - incorrect response; the correct one remembered
	0 - complete blackout.
	"""
	prompt = "Please enter the number that corresponds with your answer\n5 - perfect response\n4 - correct response after a hesitation\n3 - correct response recalled with serious difficulty\n2 - incorrect response; where the correct one seemed easy to recall\n1 - incorrect response; the correct one remembered\n0 - complete blackout.\n\n"
	while (1):
		q = raw_input(prompt)
		if int(q):
			return int(q)

def change_e_factor(item, q):
	# need quality (q) and item
	if q < 3:
		get_next_i_interval(item, reset=True)
	if item["e-factor"] >= 1.3:
		item["e-factor"] = item["e-factor"]+(0.1-(5-q)*(0.08+(5-q)*0.02))
	return item

def main(argv):
	file_path = argv[0]
	items = import_items(file_path)
	for k in items.keys():
		item = items[k]
		answer = raw_input("Question: " + item["question"] +"\n")
		q = get_quality_of_repetition()
		item = change_e_factor(item, q)
		item = get_next_i_interval(item)
		items[k] = item
		export_items(items, file_path)


if __name__ == "__main__":
	main(sys.argv[1:])