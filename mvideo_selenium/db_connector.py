from pymongo import MongoClient


class DBConnector:
    def __init__(self, host, db):
        self.db_client = MongoClient(host, port=27017)
        self.db = self.db_client[db]

    def add_hit(self, hit):
        collection = self.db.hits
        collection.insert_one(hit)