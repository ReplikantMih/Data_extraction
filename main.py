from parsers import *
import traceback

try:
    job_title = input('Введите название вакансии: ')
    hh_parser = HHParser(job_title)
    superjob_parser = SuperjobParser(job_title)

    hh_parser.run_loop()
    superjob_parser.run_loop()
except:
    print(traceback.format_exc())