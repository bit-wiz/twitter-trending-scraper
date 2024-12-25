#---------------------------------------------------------#
import pymongo
from config import Config
#---------------------------------------------------------#

class SingletonDB:
    _instance = None
    client = pymongo.MongoClient(Config.MONGO_URI)

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

class DB:
    def __init__(self, db_name, collection_name):
        self.db = SingletonDB().client[db_name]
        self.collection = self.db[collection_name]

    async def insert_data(self, data):
        try:
            print('inserting data')
            self.collection.insert_one(data)
        except Exception as e:
            print("MONGO: ", e)
            
twitterTrends = DB("twitter_trends", "trending_topics")