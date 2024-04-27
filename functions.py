import pymongo
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

def get_pq_cols(parquet_file):
    