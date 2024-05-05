from pymongo import MongoClient
import pandas as pd
import os
import json
CLOUD_URL = "mongodb+srv://doadmin:12VQ3UrM70T695BL@medina-mongo-prod-4d15c7ee.mongo.ondigitalocean.com/admin?tls=true&authSource=admin"
class Syncer(object):

    def __init__(self):
        self.cols_list_file = "cols_list.json"
        self.url = CLOUD_URL
        self.mongo = MongoClient(self.url)
        self.create_list()
    def create_list(self):
        try:
            cols_dict = {}
            db_list = self.mongo.list_database_names()
            for db in db_list:
                mongo_db = self.mongo[db]
                for collection in mongo_db.list_collection_names():
                    data = mongo_db[collection].find({}, {"_id":0}).limit(10)
                    df = pd.DataFrame(list(data))
                    cols = df.columns
                    cols_dict.update({col:f"{db}/{collection}" for col in cols})
            
            with open(self.cols_list_file, "w") as f:
                json.dump(cols_dict, f, indent=4)
            return True
        except Exception as e:
            print(e)
if __name__ == "__main__":
    
    sync = Syncer()