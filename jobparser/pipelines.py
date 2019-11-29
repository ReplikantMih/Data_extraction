from pymongo import MongoClient


class JobparserPipeline(object):
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.jobs

    def process_item(self, item, spider):
        item = dict(item)
        item['salary_from'] = int(item['salary_from']) if item['salary_from'] else None
        item['salary_till'] = int(item['salary_till']) if item['salary_till'] else None
        collection = self.mongo_base[spider.name.split('_')[0]]
        item['source'] = spider.name.split('_')[0]
        collection.insert_one(item)
        return item

class PrintPipline(object):
    def process_item(self, item, spider):
        pass