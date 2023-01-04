from pprint import pprint
import csv
import re

with open("phonebook_raw.csv", 'r', encoding='utf-8') as pb:
	rows = csv.reader(pb, delimiter=",")
	contact_list = list(rows)
	pprint(contact_list)

	surname_list = []
	for row in range(1, len(contact_list)):

		# Улучшаем ФИО
		fullname = " ".join(contact_list[row][0:3]).split()
		for i in range(len(fullname)):
			contact_list[row][i] = fullname[i]

		# Улучшаем телефон
		pattern = r"\+?\d?[\s]?\(?(\d{3}?)\)?[-\s]?(\d{3})[-\s]?(\d{2})[-\s]?(\d{0,2})([\s\(доб.]*(\d{0,4})\)?)"
		if "доб" in contact_list[row][5]:
			repl = r"+7(\1)\2-\3-\4 доб.\6"
		else:
			repl = r"+7(\1)\2-\3-\4"
		contact_list[row][5] = re.sub(pattern, repl, contact_list[row][5])

		# Удаляем дубликаты
		surname = fullname[0]
		surname_list.append(surname)
		if surname_list.count(surname) > 1:
			first_sur = surname_list.index(surname) + 1
			sec_sur = len(surname_list)
			contact_list[first_sur] = list(
				map(lambda x, y: y if not x else x, contact_list[first_sur], contact_list[sec_sur]))
			contact_list[sec_sur] = None

	new_list = [row for row in contact_list if row]

	pprint(new_list)
