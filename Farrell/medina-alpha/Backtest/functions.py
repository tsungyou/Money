import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta
'''
用法:
策略1: volume_surge_price_surge_correction_ma20
    1. df = data_strat1(ticker, start, end)
    2. return_total, winrate, avg_return, \
        trades, last_openposition_date, last_openposition_price = \
        nav_returns_backtest_only(df)
        合併後使用
策略2: price_break_box_volume_surge_MaxMinLimit
    1. df = data_strat2(ticker, start, end)
    2. return_total, winrate, avg_return, \
        trades, last_openposition_date, last_openposition_price = \
        nav_returns_backtest_only(df)
        合併後使用
'''
def read_db_parquet(ticker, start='2023-01-01', end=datetime.now()):
    ticker = ticker.replace(".", "_")
    df = pd.read_parquet(f"../../../tw-stock-screener/database/{ticker}.parquet")
    df = df[(df.index >= start) & (df.index <= end)]
    df['day_count'] = np.arange(0, len(df))
    return df

def data_strat2(ticker, start='2023-01-01', end=datetime.now()):
    '''
    1. 股價超過過去20天的最大值 => 突破箱型區間
    2. 確認過去是不是箱型: 過去20天最大最小收盤價的差必須小於股價的0.12倍
    3. 在價格突破箱型區間的同時交易量也必須破過去一段時間的新高(dafault 20 days)
    '''
    df = read_db_parquet(ticker, start, end)
    # max price - min price ======================================================
    df['max_price_past_20d'] = df['Close'].rolling(window=20, min_periods=1).max()
    df['min_price_past_20d'] = df['Close'].rolling(window=20, min_periods=1).min()

    # price over max20 ============================================================
    df['max_price_past_20d_shift5'] = df['max_price_past_20d'].shift(5)
    df['price_larger_than_max_20'] = df['max_price_past_20d_shift5'] < df['Close']

    # 0.12 of close price, the threshold ==========================================
    df['Close_12per'] = df['Close']*0.12
    df['max_min_20d_diff'] = df['max_price_past_20d'] - df['min_price_past_20d']
    df['max_min_price_less_than_12per'] = df['max_min_20d_diff'] < df['Close_12per']

    # volume surge ================================================================
    df['volume_max20'] = df['Volume'].rolling(window=20).max()
    df['volume_max20_shift5'] = df['volume_max20'].shift(5)
    df['volume_over_max20_shift5'] = df['volume_max20_shift5'] < df['Volume']

    # df['signal_total'] = (df["price_larger_than_max_20"] == True) & ((df["max_min_price_less_than_12per"] == True) & (df["volume_over_max20_shift5"] == True))
    df['price_signal'] = (df["price_larger_than_max_20"] == True) & (df["max_min_price_less_than_12per"] == True)
    df['signal'] = (df["volume_over_max20_shift5"] == True) & (df['price_signal'] == True)

    return df

def data_strat1(ticker, start='2023-01-01', end=datetime.now()):
    """Columns
    day_count, [default]
    price_max20, price_ma20, price_ma60, price_ma20_low, price_ma60_low
    vol_max20, vol_max20_shift5
    """

    price_ma1 = 20
    price_ma2 = 60
    df = read_db_parquet(ticker, start, end)

    df['price_max20'] = df['Close'].rolling(window=20, min_periods=1).max()
    df[f'price_ma{price_ma1}'] = df['Close'].rolling(window=price_ma1).mean()
    df[f'price_ma{price_ma2}'] = df['Close'].rolling(window=price_ma2).mean()
    df[f'price_ma{price_ma1}_low'] = df['Close'] < df[f"price_ma{price_ma1}"]
    df[f'price_ma{price_ma2}_low'] = df['Close'] < df[f"price_ma{price_ma2}"]



    # detact volume surge
    df['vol_max20'] = df['Volume'].rolling(window=15, min_periods=1).max()
    df['vol_max20_shift5'] = df['vol_max20'].shift(5)
    df['vol_max20_shift5_over'] = df['Volume'] > df['vol_max20_shift5']
    df["vol_max20_over3d_past_1m"] = df['vol_max20_shift5_over'].rolling(window=20, min_periods=1).apply(lambda x: any(x == True))

    # 出現超過15天低於15前的最大量，並且還沒出現更大量
    df['vol_under_max20_15d'] = df['vol_max20_shift5_over'].rolling(window=15, min_periods=1).apply(lambda x: all(x == False))

    df['signal_vol'] = (df['vol_under_max20_15d'] == True) & (df['vol_max20_over3d_past_1m'] == True)
    df['signal'] = (df['signal_vol'] == True) & (df[f"price_ma{price_ma1}_low"] == True)
    return df

def plotting_strat2(ticker, start='2023-01-01', end=datetime.now(), holding_days=10):
    df = data_strat2(ticker, start, end)
    fig, ax = plt.subplots(5, 1, figsize=(6, 8))
    ax[0].plot(df['Close'])
    ax[0].plot(df['max_price_past_20d_shift5'])
    ax[0].plot(df['min_price_past_20d'])
    for dates in df[df['price_larger_than_max_20'] == 1].index:
        ax[0].axvline(dates, color="black", alpha=0.3)

    ax[1].plot(df['max_min_20d_diff'])
    ax[1].plot(df['Close_12per'])
    for dates in df[df['max_min_price_less_than_12per'] == 1].index:
        ax[1].axvline(dates, color="black", alpha=0.3)

    ax[2].bar(df.index, df['Volume'])
    ax[2].plot(df['volume_max20'])
    for dates in df[df['volume_over_max20_shift5'] == 1].index:
        ax[2].axvline(dates, color="black", alpha=0.3)

    ax[3].plot(df['Close'])
    for dates in df[df['signal'] == 1].index:
        ax[3].axvline(dates, color="black", alpha=0.3)

    ax[0].set_title("price break max20")
    ax[1].set_title("max-min < 0.1*close")
    ax[2].set_title("volume")
    ax[3].set_title("total signal")

    plt.tight_layout()
    
    nav_returns_subplots(ax[4], df, holding_days=holding_days)
    plt.show()
    return df

def plotting_strat1(ticker='6230.TW', start='2024-01-01', end='2024-04-30', holding_days=10):
    price_ma1 = 20
    price_ma2 = 60
    fig, ax = plt.subplots(5, 1, figsize=(6, 8))
    df = data_strat1(ticker, start, end)

    ax[0].set_title(f"{ticker}--{start}~{end}")
    ax[0].plot(df['day_count'], df['Close'], label='Close')
    ax[0].plot(df['day_count'], df[f'price_ma{price_ma1}'], label='ma1')
    ax[0].plot(df['day_count'], df[f'price_ma{price_ma2}'], label='ma2')
    for dates in df[df[f'price_ma{price_ma1}_low'] == 1]['day_count']:
        ax[0].axvline(dates, color='black', alpha=0.3)
    # ====== volume data
    ax[2].bar(df['day_count'], df['Volume'])
    ax[2].plot(df['day_count'], df['vol_max20_shift5'], color='r')
    for dates in df[df['vol_max20_over3d_past_1m'] == 1]['day_count']:
        ax[2].axvline(dates, color='red', alpha=0.3)  
    ax[2].set_title("volume surged past 1m")

    ax[3].bar(df['day_count'], df['Volume'])
    ax[3].plot(df['day_count'], df['vol_max20_shift5'], color='r')
    for dates in df[df['vol_under_max20_15d'] == 1]['day_count']:
        ax[3].axvline(dates, color='red', alpha=0.3)  
    ax[3].set_title("volume correction")

    
    ax[4].plot(df['day_count'], df['Close'])
    for dates in df[df['signal_vol'] == 1]['day_count']:
        ax[4].axvline(dates, color='red', alpha=0.3)  
    ax[4].set_title("volume signal")

    # ======== Final Signal
    
    
    # ax[1].plot(df['day_count'], df['Close'])
    for dates in df[df['signal'] == 1]['day_count']:
        ax[0].axvline(dates, color='red', alpha=0.6)  
    # ax[1].set_title("signal total") 

    nav_returns_subplots(ax[1], df, holding_days=holding_days)


    plt.tight_layout()
    plt.show()
    return df

# 合併 nav_returns_subplots
def nav_returns_backtest_only(df, ax=None, plot_not_backtest=False, holding_days=10):
    start = 10000.0
    # strat1: signal_vol_ma_final
    # strat2: signal
    cur = pd.Series([0] * len(df))
    cur[0] = start
    open_position = []
    close_position = []
    returns_pertrade = []
    current = start
    holding = False
    df['pct_change'] = df['Close'].pct_change()
    k = 0
    pct_change_all = 0
    for i in range(len(df)):
        if df['signal'].iloc[i] == False and holding == False:
            cur[i] = current
            continue
        else:
            if holding == False:
                buy_price = df['Close'].iloc[i]
                open_position.append([i, buy_price])
                cur[i] = current
                holding = True
            elif holding == True:
                if df['signal'].iloc[i] == True:
                    k = 0
                pct_change = df['pct_change'].iloc[i]
                pct_change_all += pct_change
                current_open = current * (1+pct_change_all)
                # print(current, pct_change, pct_change_all, current_open, i)
                if k == holding_days:
                    close_price = df['Close'].iloc[i]
                    close_position.append([i, close_price])
                    holding = False
                    current = current_open
                    k = 0
                    pct_change_all = 0
                    returns_pertrade.append(close_price/buy_price - 1)
                cur[i] = current_open
                
                k += 1
    if plot_not_backtest:
        ax.plot(df['day_count'], cur, label='returns')
        for index, i in enumerate(open_position):
            if index == 0:
                ax.axvline(i[0], color='r', label='Open')
            else:
                ax.axvline(i[0], color='r')
        for index, i in enumerate(close_position):
            if index == 0:
                ax.axvline(i[0], color='b', label='Close', alpha=0.3)
            else:
                ax.axvline(i[0], color='b')
        
        print("returns: ", returns_pertrade)
        print("avg per trade: ", avg_return)
        print("winrate: ", winrate)
        print(open_position)
        print(close_position)
        print(f"return: {return_total}")
        print(cur[len(df) - 1])
        return None
    else:
        try:
            return_total = cur[len(df)-1]/cur[0] - 1
        except: 
            return 0, 0, 0, 0, 0, 0
        avg_return = np.mean(returns_pertrade)
        try:
            winrate = count_positive_numbers(returns_pertrade)/len(returns_pertrade)
        except:
            return 0, 0, 0, 0, 0, 0
        last_openposition_date = open_position[-1][0]
        last_openposition_price = open_position[-1][1]
        trades = len(open_position)
        return return_total, winrate, avg_return, trades, last_openposition_date, last_openposition_price

# 淘汰
def nav_returns_subplots(ax, df, data_output = True, holding_days=10):
    start = 10000.0
    # ind = df[df['signal_vol_ma_final'] == True].index
    # print(ind)
    cur = pd.Series([0] * len(df))
    cur[0] = start
    open_position = []
    close_position = []
    returns_pertrade = []
    current = start
    holding = False
    df['pct_change'] = df['Close'].pct_change()
    k = 0
    pct_change_all = 0
    for i in range(len(df)):
        if df['signal'].iloc[i] == False and holding == False:
            cur[i] = current
            continue
        else:
            if holding == False:
                buy_price = df['Close'].iloc[i]
                open_position.append([i, df.index[i], buy_price])
                cur[i] = current
                holding = True
            elif holding == True:
                if df['signal'].iloc[i] == True:
                    k = 0
                pct_change = df['pct_change'].iloc[i]
                pct_change_all += pct_change
                current_open = current * (1+pct_change_all)
                # print(current, pct_change, pct_change_all, current_open, i)
                if k == holding_days:
                    close_price = df['Close'].iloc[i]
                    close_position.append([i, df.index[i], close_price])
                    holding = False
                    current = current_open
                    k = 0
                    pct_change_all = 0
                    returns_pertrade.append(close_price/buy_price - 1)
                cur[i] = current_open
                
                k += 1
    # if k != 1:
    #     close_position.append([i, df.index[i], df[k-1].index])

    # data output calculation

    return_total = cur[len(df)-1]/cur[0] - 1
    avg_return = np.mean(returns_pertrade)
    winrate = count_positive_numbers(returns_pertrade)/len(returns_pertrade)
    if data_output:
        ax.plot(df['day_count'], cur, label='returns')
        for index, i in enumerate(open_position):
            if index == 0:
                ax.axvline(i[0], color='r', label='Open')
            else:
                ax.axvline(i[0], color='r')
        for index, i in enumerate(close_position):
            if index == 0:
                ax.axvline(i[0], color='b', label='Close', alpha=0.3)
            else:
                ax.axvline(i[0], color='b')
        
        print("returns: ", returns_pertrade)
        print("avg per trade: ", avg_return)
        print("winrate: ", winrate)
        print(open_position)
        print(close_position)
        print(f"return: {return_total}")
        print(cur[len(df) - 1])
        return None
    else:
        return return_total, winrate, avg_return


def count_positive_numbers(numbers):
    count = 0
    for num in numbers:
        if num > 0:
            count += 1
    return count

if __name__ == "__main__":
    print("functions.py")