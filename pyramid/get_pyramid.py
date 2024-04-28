from pymongo import MongoClient
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import numpy as np
import tqdm
import json

def handling_vacancy(final_pri):
    for i in range(len(final_pri)):
        if i == 0:
            continue
        if final_pri[i] == "":
            final_pri[i] = final_pri[i-1]
def create_tw_1000_db(stockList, update=False):
    outcomes = []
    log = []
    with tqdm.tqdm(total=len(stockList)) as pbar:
        for stock in stockList[100:]:
            try:
                url = f"https://norway.twsthr.info/StockHolders.aspx?stock={stock}"
                c = requests.get(url)
                soup = BeautifulSoup(c.text, "lxml")
                ds = soup.find_all("tr", {"class":"lDS"})
                ls = soup.find_all("tr", {"class":"lLS"})
                title = []
                date_ds = []
                date_ls = []
                price_ds = []
                price_ls = []
                percentage_ls = []
                percentage_ds = []
                total = 166 + 1
                total_ds = 83+1
                total_ls = 83
                
                for cc, i in enumerate(ds):
                    for q, k in enumerate(i):
                        if cc != 0:
                            if q == 2:
                                date_str = k.text[:-1]
                                date_ds.append(f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:]}")
                            if q == 13:
                                percentage_ds.append(k.text)
                            if q == 14:
                                price_ds.append(k.text)

                        else:
                            if q in [2, 13, 14]:
                                title.append(k.text)
                    if cc >= total_ds + 1:
                        break

                for cc, i in enumerate(ls):
                    for q, k in enumerate(i):
                        if q == 2:
                            date_str = k.text[:-1]
                            date_ls.append(f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:]}")
                        if q == 13:
                            percentage_ls.append(k.text)
                        if q == 14:
                            price_ls.append(k.text)
                    if cc >= total_ds + 1:
                        break
                final_per = []
                final_pri = []
                final_dat = []
                for i in range(len(date_ds)): # 85 
                    final_per.append(percentage_ds[i])
                    final_per.append(percentage_ls[i])
                    final_pri.append(price_ds[i])
                    final_pri.append(price_ls[i])
                    final_dat.append(date_ds[i])
                    final_dat.append(date_ls[i])

                dates = [datetime.strptime(date, "%Y-%m-%d") for date in final_dat]

                for i in range(len(final_pri)):
                    
                    if i == 0:
                        continue
                    if final_pri[i] == "":
                        final_pri[i] = final_pri[i-1]

                handling_vacancy(final_pri)
                handling_vacancy(final_per)
                # Convert values to float
                values = [float(value) for value in final_pri]
                percenta = [float(value) for value in final_per]


                if len(final_per) == len(final_pri) == len(final_dat):
                    data = pd.DataFrame({"date":dates[::-1],    
                                    "customA":percenta[::-1],
                                    "price":values[::-1],
                                    "Open":values[::-1],
                                    "High":values[::-1],
                                    "Low":values[::-1],
                                    "Close":values[::-1]}) 
                data[f"pct_1000"] = data['customA'].pct_change()
                
                data['date'] = data['date'].apply(lambda x: x.strftime("%Y-%m-%d"))
                dict_by_index = data.to_dict(orient='index')
                list_ = []
                if not update:
                    for _, values in dict_by_index.items():
                        values.update({'code':stock})
                        list_.append(values)
                else:
                    for _, values in dict_by_index.items():
                        # if key >= datetime.datetime.strptime(latest_date_db, "%Y-%m-%d"):
                        values.update({'code':stock})
                        list_.append(values)
            except Exception as e:
                print(e)    
            pbar.update(1)
if __name__ == '__main__':
    a = {"2":2}
    with open("test.json", "w", encoding="utf-8") as f:
        json.dump(a, f, indent=4)
# create_tw_1000_db(dicts=dicts, update=False)