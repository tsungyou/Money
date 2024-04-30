from pymongo import MongoClient, InsertOne
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import os
from configs.configs import MongoList
# from handler.base import DBHandler
# from handler.enumeration import DB
# from shared_utils.slack import SlackBot

class Syncer(object):

    def __init__(self):
        self.db_list = MongoList.DB_LIST
        self.main_dir = "financial_statements"
        self.mongo = MongoClient(MongoList.CLOUD_URL)
    def update_all(self, test=True):
        try:
            self.make_dir([f"{self.main_dir}"])
            for db in self.db_list:
                self.make_dir([f"{self.main_dir}/{db.lower()}"])
                mongo_db = self.mongo[db]
                for collection in mongo_db.list_collection_names():
                    if test:
                        data = mongo_db[collection].find({}, {"_id":0}).limit(100000)
                    else:
                        data = mongo_db[collection].find({})

                    df = pd.DataFrame(list(data))
                    parquet_file_path = f"{self.main_dir}/{db.lower()}/{collection}.parquet"
                    pq.write_table(pa.Table.from_pandas(df), parquet_file_path)
                    print(db, collection, "to_parquet done")
                    # requests = [InsertOne(item) for item in data]
                    # result = local_mongo.bulk_write(requests)
            print(f"Syncronize success from database {db}")
        except Exception as e:
            print(f"error when syncronizing database: {e}")
    def make_dir(self, dirs):
        if isinstance(dirs, str):
            dirs = [dirs]
        for dir in dirs: 
            if not os.path.exists(dir):
                os.makedirs(dir)
                print(f"make dir {dir}")
            else:
                print(f"dir {dir} existed")
            return None 

if __name__ == "__main__":
    sync = Syncer()
    # sync.make_dir()
    sync.update_all()