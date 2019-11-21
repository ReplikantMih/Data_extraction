from parsers import *
from db_connector import DBConnector
import traceback
from pprint import pprint


class ACTIONS:
    get_info = 'get_info'
    parse = 'parse'


action = ACTIONS.get_info  # ЗДЕСЬ ПЕРЕКЛЮЧАЕТСЯ РЕЖИМ РАБОТЫ ПРИЛОЖЕНИЯ (парсинг / получение информации из базы).


try:
    if action == ACTIONS.parse:
        job_title = input('Введите название вакансии: ')
        hh_parser = HHParser(job_title)
        superjob_parser = SuperjobParser(job_title)

        hh_parser.run_loop()
        superjob_parser.run_loop()
    elif action == ACTIONS.get_info:
        try:
            salary_min = int(input('Введите минимальную зарплату для поиска: '))
        except:
            print('Error: введено не число.')
        db_connector = DBConnector('localhost', 'jobs_parsed')
        pprint(db_connector.get_job_with_salary_more_than(salary_min))
except:
    print(traceback.format_exc())
