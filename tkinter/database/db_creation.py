# db_init
import requests
from bs4 import BeautifulSoup
import pandas as pd
import yfinance as yf
import pyarrow as pa
a = pd.read_csv("../database/tw_stock_list.csv")
list_with_market = list(a['market'])
df = yf.download(list_with_market)
# delist
delist = ['5281.TWO', '4944.TWO', '2456.TWO', '2823.TWO', '1592.TWO', '3536.TWO', '1787.TWO', '0058.TWO', '5264.TWO', '6131.TWO', '5305.TWO', '1333.TWO', '3642.TWO', '8497.TWO', '3562.TWO', '5259.TWO', '6497.TWO', '0059.TWO', '5102.TWO', '1724.TWO', '6594.TWO', '9188.TWO', '3383.TWO', '1507.TWO', '4947.TWO', '3089.TWO', '4141.TWO', '1902.TWO', '1262.TWO', '8287.TWO', '4180.TWO', '2936.TWO', '8427.TWO', '5820.TWO', '5349.TWO', '2928.TWO', '2841.TWO', '4152.TWO', '6172.TWO', '8934.TWO', '3144.TWO', '6452.TWO', '3698.TWO', '1258.TWO', '3682.TWO', '8406.TWO', '2499.TWO', '8480.TWO', '8418.TWO', '3452.TWO', '1566.TWO', '6247.TWO', '2448.TWO', '9157.TWO', '0054.TWO', '6238.TWO', '5304.TWO', '4725.TWO', '8913.TWO', '4144.TWO', '6289.TWO', "6251.TWO"]

adj_close = df['Adj Close']
adj_close.dropna(axis=1, how='all', inplace=True)
adj_close.to_parquet("Adj_close.parquet")
