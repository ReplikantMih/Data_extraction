from pymongo import MongoClient


class DBConnector:
    def __init__(self, host, db):
        self.db_client = MongoClient(host, port=27017)
        self.db = self.db_client[db]

    def add_letter(self, letter):
        collection = self.db.emails
        collection.insert_one(letter)