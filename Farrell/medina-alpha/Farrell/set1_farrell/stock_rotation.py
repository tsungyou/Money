import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import statsmodels.api as sm
from sklearn.cluster import KMeans
from factor_analyzer import FactorAnalyzer
import json
import numpy as np

def print_function_name(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print(func.__name__, "....")
        return result
    return wrapper
class Clustering():
    def __init__(self, start_year=2024, top=100, factor=9):
        self.start_year = start_year
        self.top = top
        self.factor = factor

    @print_function_name
    def get_stock_list_by_volume(self):
        SP500_list = list(pd.read_csv("constituents.csv")['Symbol'])
        df_close = yf.download(SP500_list[:500], start=f'{self.start_year}-01-01'
                            , end=pd.to_datetime(f'{self.start_year}-01-01')+timedelta(days=5), progress=False)
        df_close_t = df_close['Volume'].iloc[0, :].T
        df_close_t.columns = ['Volume']
        df_close_t.dropna(inplace=True)
        list_ = df_close_t.sort_values(ascending=False)[:self.top].index.to_list()
        print()
        return list_


    @print_function_name
    def get_stock_price(self):
        stock_list = self.get_stock_list_by_volume()
        df_close = yf.download(stock_list, start=pd.to_datetime(f'{self.start_year}-01-01') - timedelta(days=365*5), end=f'{self.start_year}-01-01', progress=False)['Adj Close']
        spx_close = yf.download("^GSPC", start=pd.to_datetime(f'{self.start_year}-01-01') - timedelta(days=365*5), end=f'{self.start_year}-01-01', progress=False)['Adj Close']
        return df_close, spx_close

    @print_function_name
    def get_data_to_be_factorized(self):
        df_close, spx_close = self.get_stock_price()
        df_close_pct = df_close.pct_change().iloc[1:, :]
        spx_pct = spx_close.pct_change()

        df_close_pct.dropna(inplace=True, axis=1)
        spx_pct.dropna(inplace=True)

        df_close_pct_m = df_close_pct.resample("ME").agg(lambda x: (x+1).prod() - 1)
        spx_pct_m = spx_pct.resample("ME").agg(lambda x: (x+1).prod() - 1)

        return df_close_pct_m, spx_pct_m

    @print_function_name
    def factorize(self):
        df_close_pct_m, spx_pct_m = self.get_data_to_be_factorized()
        res_df = pd.DataFrame()
        alpha_dict = {}
        X = spx_pct_m
        X_sm = sm.add_constant(X)
        for ticker in df_close_pct_m.columns:
            # OLS regression
            close = df_close_pct_m[ticker]
            y = close
            model = sm.OLS(y, X_sm)

            res = model.fit()
            residuals = res.resid
            res_df[ticker] = residuals

            # store alpha
            res_table = res.summary().tables
            alpha = float(res_table[1].data[1][1].strip())
            alpha_dict[ticker] = alpha
        factor_analyzer = FactorAnalyzer(n_factors=self.factor, rotation='promax') # varimax
        factor_analyzer.fit(res_df.corr())

        # Get factor loadings
        factor_loadings = factor_analyzer.loadings_
        df = pd.DataFrame(factor_loadings, index=list(res_df.columns))
        df['Ticker'] = df.index
        # Apply K-means clustering
        kmeans = KMeans(n_clusters=self.factor)
        kmeans.fit(df.iloc[:, :self.factor])

        # Assign cluster labels to tickers
        df['Cluster'] = kmeans.labels_

        # Display the result
        res = df[['Ticker', 'Cluster']]
        res = res.copy()
        # add clustered value to check further
        cluster_value = []
        for i in range(len(res)):
            classification = res.iloc[i, 1]
            cluster_value.append(df.iloc[i, classification])
        res['Cluster_value'] = cluster_value

        sorted_res = res.sort_values(by='Cluster')


        res_dict = {}
        for i in range(self.factor):

            res_dict["class" + str(i)] = list(sorted_res[sorted_res['Cluster'] == i]['Ticker'])
        return res_dict
        # factor == 3比較穩定 但還是不合理

    @print_function_name
    def cluster_to_json(self):
        cluster_dict = self.factorize()
        with open(f"for_{self.start_year}_top{self.top}_cluster{self.factor}.json", "w") as f:
            json.dump(cluster_dict, f, indent=4)
        return None


class Backtesting():
    def __init__(self):
        pass

cluster = Clustering()
cluster.cluster_to_json()


