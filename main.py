from pprint import pprint
import re
import csv

def get_full_row(contacts_list):
    '''Функция для получения корректных ФИО с остальными данными'''
    full_row = []
    for row in contacts_list:
        full_name = ' '.join(row[:3]).split(' ')
        full_name = [x for x in full_name if x] 
        if len(full_name) < 3:
            full_name.append('')
        result = full_name + row[3:]
        if result not in full_row:
            full_row.append(result)
    return full_row


def update_phone(row):
    '''Функция для обновления номера телефона'''
    if re.search('доб', row, re.IGNORECASE):
        pattern = r'\+?(7|8)\s?\(?(\d{3})\)?[\s|-]?(\d{3})[\s|-]?(\d{2})[\s|-]?(\d{2})\s?\(?(\D{3})?\.?\s?\(?(\d{4})\)?'
        sub_pattern = r'+7(\2)\3-\4-\5 доб.\7'
        result = re.sub(pattern, sub_pattern, row)
    else:
        pattern_2 = r'\+?(7|8)\s?\(?(\d{3})\)?[\s|-]?(\d{3})[\s|-]?(\d{2})[\s|-]?(\d{2})'
        sub_pattern_2 = r'+7(\2)\3-\4-\5'   
        result = re.sub(pattern_2, sub_pattern_2, row)
    return result


def get_full_table(full_row):
    '''Функция для заполнения таблицы обновленным номером'''
    for row in full_row:
        row[5] = update_phone(row[5])
    return full_row


def remove_duplicates(full_row):
    '''Функция удаления дубликатов'''
    contacts_list_new = []
    for first_row in full_row:
        first_name, first_last_name = first_row[0], first_row[1]
        for second_row in full_row:
            new_first_name, new_last_name = second_row[0], second_row[1]
            if first_name == new_first_name and first_last_name == new_last_name:
                for i in range(2, len(first_row)):
                    if first_row[i] == '':
                        first_row[i] = second_row[i]      
        if first_row not in contacts_list_new:
            contacts_list_new.append(first_row)  
    return contacts_list_new


if __name__ == '__main__':
    with open("phonebook_raw.csv", encoding="utf-8") as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list = list(rows)

    contacts_list_new = get_full_table(remove_duplicates(get_full_row(contacts_list)))

    # pprint(contacts_list_new)
    with open("phonebook.csv", "w", encoding="utf-8") as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerows(contacts_list_new)