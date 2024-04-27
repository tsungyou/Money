import pymongo
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import os
import json
from configs.configs import MongoList

db_dir = os.path.join(os.getcwd(), MongoList.PARENT_DIR)
cols_list_file = os.path.join(db_dir, "cols_list.json")

def get_pq_cols(parquet_file_path, get='c'):
    table = pq.read_table(parquet_file_path)
    df = table.to_pandas()
    # print(df.head())
    if get == "c":
        return list(df.columns)
    else:
        return df

def create_pq_cols_list():
    
    # if os.path.isfile(os.path.join(db_dir, "cols_list.json")):
    #     print("cols_list.json existed")
    #     return True
    cols_dict = {}
    dbs = [db for db in os.listdir(db_dir) if os.path.isdir(os.path.join(db_dir, db))]
    for db in dbs:
        collection_dir = os.path.join(db_dir, db)
        collection_list = os.listdir(collection_dir)
        for parquet_file in collection_list:
            parquet_file_abspath = os.path.join(collection_dir, parquet_file)
            cols = get_pq_cols(parquet_file_abspath, get="c")
            cols_dict.update({col : f"{db}/{parquet_file}" for col in cols})

    with open(cols_list_file, "w") as f:
        json.dump(cols_dict, f, indent=4)
    return True

# 給定字串，return相關欄位的collection
def get_collections_by_colname(colname):
    with open(cols_list_file, "r") as f:
        data = json.load(f)
    print(data)
    matching_strings = [item for item in data if colname in item]

    sub_dict = {key: data[key] for key in matching_strings if key in data}

    return sub_dict