import csv
import re
from datetime import datetime
import math
from prettytable import PrettyTable, ALL

file = input()
API_HH_dict = {'name': 'Название',
               'description': 'Описание',
               'key_skills': 'Навыки',
               'experience_id': 'Опыт работы',
               'premium': 'Премиум-вакансия',
               'employer_name': 'Компания',
               'salary_from': 'Нижняя граница вилки оклада',
               'salary_to': 'Верхняя граница вилки оклада',
               'salary_gross': 'Оклад указан до вычета налогов',
               'salary_currency': 'Идентификатор валюты оклада',
               'salary': 'Оклад',
               'area_name': 'Название региона',
               'published_at': 'Дата публикации вакансии'}

experience_of_work = {"noExperience": "Нет опыта",
                      "between1And3": "От 1 года до 3 лет",
                      "between3And6": "От 3 до 6 лет",
                      "moreThan6": "Более 6 лет"}

currency = {"AZN": "Манаты",
            "BYR": "Белорусские рубли",
            "EUR": "Евро",
            "GEL": "Грузинский лари",
            "KGS": "Киргизский сом",
            "KZT": "Тенге",
            "RUR": "Рубли",
            "UAH": "Гривны",
            "USD": "Доллары",
            "UZS": "Узбекский сум"}


def formatter(row):
    formatted_row = {}
    for key, value in row.items():
        formatted_value = value
        if value == 'True' or value == 'False':
            formatted_value = re.sub(r'True', 'Да', value)
            formatted_value = re.sub(r'False', 'Нет', value)
        if value in experience_of_work:
            formatted_value = experience_of_work[value]
        if value in currency:
            formatted_value = currency[value]
        if key == 'Оклад указан до вычета налогов':
            formatted_value = 'С вычетом налогов' if formatted_value == 'Нет' else 'Без вычета налогов'
        if key == 'Дата публикации вакансии':
            date = datetime.strptime(value[:10], '%Y-%m-%d')
            formatted_value = date.strftime('%d.%m.%Y')
        formatted_row[key] = formatted_value
    salary = f'{math.trunc(float(formatted_row["Нижняя граница вилки оклада"])):,} - {math.trunc(float(formatted_row["Верхняя граница вилки оклада"])):,} ({formatted_row["Идентификатор валюты оклада"]}) ({formatted_row["Оклад указан до вычета налогов"]})'.replace(
        ',', ' ')
    buf_row = {
        'Название': formatted_row['Название'],
        'Описание': formatted_row['Описание'],
        'Навыки': formatted_row['Навыки'],
        'Опыт работы': formatted_row['Опыт работы'],
        'Премиум-вакансия': formatted_row['Премиум-вакансия'],
        'Компания': formatted_row['Компания'],
        'Оклад': salary,
        'Название региона': formatted_row['Название региона'],
        'Дата публикации вакансии': formatted_row['Дата публикации вакансии'],
    }
    return buf_row


def csv_reader(file_name):
    text = []
    empty_file = [['Пустой файл']]
    with open(file_name, 'r', encoding='utf-8-sig') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            text.append(row)
        if len(text) == 0:
            return empty_file
        else:
            return text


header = csv_reader(file)[0]
header_rus = []
for words in header:
    for keys, values in API_HH_dict.items():
        if words == keys:
            header_rus.append(values)


def csv_filer(reader, list_naming):
    list_of_lists = []
    vacancy_list = []
    list_of_dicts = []
    for i in range(len(reader)):
        flag = True
        for j in range(len(reader[i])):
            if len(reader[i]) != len(header) or reader[i][j] == '':
                flag = False
        if flag is True:
            list_of_lists.append(reader[i])
    for row in list_of_lists:
        vacancy_row = []
        for line in row:
            line = re.sub(r'<[^>]*>', '', line)
            if '\n' in line:
                line = ', '.join(line.split('\n'))
            line = ' '.join(line.split())
            vacancy_row.append(line)
        vacancy_list.append(vacancy_row)
    for i in vacancy_list:
        vacancy_dict = dict(zip(list_naming, i))
        list_of_dicts.append(vacancy_dict)
    return list_of_dicts


def print_table(data_vacancies):
    vacancies_table = PrettyTable()
    vacancies_table.field_names = ['№', 'Название', 'Описание', 'Навыки', 'Опыт работы', 'Премиум-вакансия', 'Компания',
                                   'Оклад', 'Название региона', 'Дата публикации вакансии']
    list_of_tablelists = []
    number = 1
    for dict in data_vacancies[1:]:
        table_list = []
        row = formatter(dict)
        for keys, values in row.items():
            formatted_value = ''
            if keys == 'Навыки':
                splitted_value = values.split(', ')
                for i in splitted_value:
                    formatted_value += i + '\n'
                row['Навыки'] = formatted_value
        for i in row.values():
            if len(i) > 100:
                string = i[0:100] + '...'
                table_list.append(string.strip())
            else:
                table_list.append(i.strip())
        table_list.insert(0, number)
        list_of_tablelists.append(table_list)
        number += 1

    vacancies_table.add_rows(list_of_tablelists)
    vacancies_table.hrules = ALL
    vacancies_table.align = 'l'
    vacancies_table._max_width = {'№': 20, 'Название': 20, 'Описание': 20, 'Навыки': 20, 'Опыт работы': 20,
                                  'Премиум-вакансия': 20, 'Компания': 20, 'Оклад': 20, 'Название региона': 20,
                                  'Дата публикации вакансии': 20}
    if list_of_tablelists == [] and csv_reader(file) != [['Пустой файл']]:
        print('Нет данных')
    elif csv_reader(file) == [['Пустой файл']]:
        print('Пустой файл')
    else:
        print(vacancies_table)


print_table(csv_filer(csv_reader(file), header_rus))
