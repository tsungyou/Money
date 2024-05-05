import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import os
from datetime import datetime, timedelta
import yfinance as yf
CUR_PATH = os.getcwd()
DIR_PATH = os.path.dirname(os.path.dirname(__file__))
today = datetime.now()

def get_files_under_path(path):
    files = []

    for root, directories, filenames in os.walk(path):
        for filename in filenames:
            file_path = os.path.join(root, filename)
            if os.path.isfile(file_path):
                files.append(file_path)

    return files

# Example usage:
if __name__ == "__main__":
    path_parquet = os.path.join(DIR_PATH, "database")
    files = get_files_under_path(path_parquet)
    for _, file in enumerate(files):
        tick = file.split("/")[-1].split(".")[0]
        ticker = tick.replace("_", ".")
        update_data =  yf.download(ticker, start=today, interval='1d', progress=False)
        
        current_data = pd.read_parquet(file)
        df = pd.concat([current_data, update_data], axis=0)

        table = pa.Table.from_pandas(df)

        df.to_parquet(f"../{tick}.parquet", engine='fastparquet')
        
        if _%100==0:
            print(_)