from pymongo import MongoClient


class DBConnector:
    def __init__(self, host, db):
        self.db_client = MongoClient(host, port=27017)
        self.db = self.db_client[db]

    def add_job(self, job):
        if job['site'] == 'hh.ru':
            collection = self.db.hh
        elif job['site'] == 'superjob.ru':
            collection = self.db.superjob
        collection.insert_one(job)

    def add_unique_job(self, job):
        if job['site'] == 'hh.ru':
            collection = self.db.hh
        elif job['site'] == 'superjob.ru':
            collection = self.db.superjob
        in_db = collection.find({'site_id': job['site_id']})
        if not list(in_db):
            collection.insert_one(job)

    def get_job_with_salary_more_than(self, salary):
        hh_jobs = list(self.db['hh'].find({'salary_from': {'$gt': salary}}))
        superjob_jobs = list(self.db['superjob'].find({'salary_from': {'$gt': salary}}))
        return hh_jobs + superjob_jobs
