from pprint import pprint
import csv
import re

with open("phonebook_raw.csv", 'r', encoding='utf-8') as f:
	rows = csv.reader(f, delimiter=",")
	contact_list = list(rows)
	pprint(contact_list)

	surname_list = []  # Список для объединения и удаления дубликатов
	for row in range(1, len(contact_list)):

		# Улучшаем ФИО: 3 первых элемента списка объединяем и разделяем, и заполняем список
		fullname = " ".join(contact_list[row][0:3]).split()
		for i in range(len(fullname)):
			contact_list[row][i] = fullname[i]

		# Улучшаем телефон: написал огромный паттерн чтобы учитывать "доб." без условий,
		# но это было так громоздко, что решил сделать с условием
		pattern = r"\+?\d?[\s]?\(?(\d{3}?)\)?[-\s]?(\d{3})[-\s]?(\d{2})[-\s]?(\d{0,2})([\s\(доб.]*(\d{0,4})\)?)"
		if "доб" in contact_list[row][5]:
			repl = r"+7(\1)\2-\3-\4 доб.\6"
		else:
			repl = r"+7(\1)\2-\3-\4"
		contact_list[row][5] = re.sub(pattern, repl, contact_list[row][5])

		# Объединяем дубликаты
		surname = fullname[0]
		surname_list.append(surname)  # Создаем список из фамилий для поиска повторений
		if surname_list.count(surname) > 1:
			# Находим индексы 2х вхождений фамилий
			first_sur = surname_list.index(surname) + 1
			sec_sur = len(surname_list)
			# Объединяем 2 строки из списка контактов по найденным индексам
			contact_list[first_sur] = list(
				map(lambda x, y: y if not x else x, contact_list[first_sur], contact_list[sec_sur]))
			contact_list[sec_sur] = None   # Дубликат обнуляем
	# Удаляем дубликаты
	new_list = [row for row in contact_list if row]
	pprint(new_list)


with open("phonebook.csv", "w") as f:
	datawriter = csv.writer(f, delimiter=',')
	datawriter.writerows(new_list)
